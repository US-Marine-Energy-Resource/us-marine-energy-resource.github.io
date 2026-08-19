"""MkDocs hook: inject citation/MathJax <script> tags only on pages that need them.

`extra_javascript` in mkdocs.yml is a single static list injected on every page
by the theme's base template -- MkDocs has no native per-page conditional
mechanism for it. Two of our scripts are expensive and only used by a minority
of pages:

  - docs/javascripts/citation.min.js (~2.7 MB, bundled citation-js) plus
    docs/javascripts/cite.js -- needed only on pages using citation markup
    ([@key], [!@key], [chicago@key]), a `.bibliography` div, or the
    #cite-dataset-widget element.
  - docs/javascripts/mathjax.js (MathJax config) plus the MathJax CDN bundle
    (https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js) -- needed only on pages
    containing math that pymdownx.arithmatex actually recognized.

This hook removes those four entries from the global extra_javascript list
(see mkdocs.yml) and, on `on_post_page`, inspects each page's *rendered* HTML
and injects <script> tags for only the categories that page actually needs,
directly before `</body>`.

Citation detection mirrors docs/javascripts/cite.js's own CITE_RE /
FULL_CITE_RE / CHICAGO_INLINE_RE / .bibliography / #cite-dataset-widget
checks so server-side injection and the client-side script never disagree
about which pages have citations.

Math detection keys off the `class="arithmatex"` marker that
pymdownx.arithmatex (configured with `generic: true`, see mkdocs.yml
markdown_extensions) emits around every math expression/block it actually
recognized. This is deliberately *not* a raw regex for \\(, \\[, or $$ on the
HTML: those delimiters also appear inside fenced code blocks that merely
document the math syntax (see docs/getting-started/contributing.md, which
uses $$ and \\( only inside fenced code blocks and correctly produces zero
`arithmatex` elements) -- matching the class instead of the delimiters avoids
loading MathJax on pages that don't actually contain live math.

No on_files handling is required to keep these scripts landing in site/:
MkDocs's own file-collection step (mkdocs.structure.files.get_files) walks
the entire docs_dir and copies every non-Markdown file to site_dir
unconditionally. Membership in extra_javascript only controls whether a
<script> tag is emitted by the base template -- it has no bearing on whether
the underlying file is copied. So docs/javascripts/citation.min.js, cite.js,
and mathjax.js keep landing in site/javascripts/ exactly as before, even
after being dropped from extra_javascript.
"""

import logging
import re
from pathlib import Path

from mkdocs.utils import get_relative_url, normalize_url

log = logging.getLogger("mkdocs.hooks.conditional_page_scripts")

_REPO_ROOT = Path(__file__).resolve().parent.parent
_JS_DIR = _REPO_ROOT / "docs" / "javascripts"

# Mirrors docs/javascripts/cite.js's CITE_RE / FULL_CITE_RE / CHICAGO_INLINE_RE.
_CITE_RE = re.compile(r"\[@[a-zA-Z0-9_:.-]+(?:\s*;\s*@[a-zA-Z0-9_:.-]+)*\]")
_FULL_CITE_RE = re.compile(r"\[!@[a-zA-Z0-9_:.-]+(?:\s*;\s*!@[a-zA-Z0-9_:.-]+)*\]")
_CHICAGO_INLINE_RE = re.compile(r"\[chicago@[a-zA-Z0-9_:.-]+\]")
_BIBLIOGRAPHY_DIV_RE = re.compile(r'class="[^"]*\bbibliography\b[^"]*"')
_CITE_WIDGET_RE = re.compile(r'id="cite-dataset-widget"')

# pymdownx.arithmatex (generic: true) wraps every math expression/block it
# actually recognized in an element carrying this class.
_ARITHMATEX_RE = re.compile(r'class="[^"]*\barithmatex\b[^"]*"')

_CITATION_SCRIPTS = ("javascripts/citation.min.js", "javascripts/cite.js")
_MATHJAX_SCRIPTS = (
    "javascripts/mathjax.js",
    "https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js",
)


def _needs_citation_scripts(html: str) -> bool:
    """Return True if the rendered page contains any citation markup."""
    return bool(
        _CITE_RE.search(html)
        or _FULL_CITE_RE.search(html)
        or _CHICAGO_INLINE_RE.search(html)
        or _BIBLIOGRAPHY_DIV_RE.search(html)
        or _CITE_WIDGET_RE.search(html)
    )


def _needs_mathjax(html: str) -> bool:
    """Return True if pymdownx.arithmatex rendered any math on this page."""
    return bool(_ARITHMATEX_RE.search(html))


def _script_tag(src: str, page_url: str) -> str:
    """Build a deferred <script> tag, relative to page_url for local assets."""
    if src.startswith("http://") or src.startswith("https://"):
        url = src
    else:
        url = get_relative_url(normalize_url(src), page_url)
    return f'<script src="{url}" defer></script>'


def on_pre_build(config, **kwargs) -> None:
    """Fail fast if a script this hook depends on has gone missing.

    These files are no longer listed in extra_javascript, so MkDocs itself
    has no reason to notice if one is deleted or renamed -- the page would
    just silently render without citations/math with no build-time signal.
    """
    missing = [
        name
        for name in ("citation.min.js", "cite.js", "mathjax.js")
        if not (_JS_DIR / name).is_file()
    ]
    if missing:
        raise SystemExit(
            "\nERROR: conditional_page_scripts: missing required script(s) in "
            f"{_JS_DIR}: {', '.join(missing)}\n"
            "These are injected per-page by hooks/conditional_page_scripts.py "
            "instead of via extra_javascript; restore the file(s) or update "
            "this hook and mkdocs.yml together.\n"
        )


def on_post_page(output, page, config, **kwargs):
    """Inject citation/MathJax <script> tags only on pages that use them."""
    tags = []

    if _needs_citation_scripts(output):
        tags.extend(_script_tag(src, page.url) for src in _CITATION_SCRIPTS)
        log.debug("conditional_page_scripts: citation scripts -> %s", page.file.src_uri)

    if _needs_mathjax(output):
        tags.append('<link rel="preconnect" href="https://unpkg.com" />')
        tags.extend(_script_tag(src, page.url) for src in _MATHJAX_SCRIPTS)
        log.debug("conditional_page_scripts: MathJax scripts -> %s", page.file.src_uri)

    if not tags:
        return output

    injected = "\n".join(tags)
    if "</body>" in output:
        return output.replace("</body>", f"{injected}\n</body>", 1)

    log.warning(
        "conditional_page_scripts: %s has no </body> tag; appending scripts at end.",
        page.file.src_uri,
    )
    return output + "\n" + injected
