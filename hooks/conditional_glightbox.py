"""MkDocs hook: skip the mkdocs-glightbox plugin's per-page cost on pages with no images.

The mkdocs-glightbox plugin (configured in mkdocs.yml's `plugins:` list)
unconditionally injects its own CSS link, JS script tag, and a
`GLightbox(...)` init script into *every* page's `on_post_page` output, and
wraps every `<img>` it finds in `on_page_content`. That's real, unnecessary
work (plus a second, independent GLightbox instance -- see
docs/javascripts/glightbox-init.js, which builds its own instance and
stopPropagation()s clicks to neutralize the plugin's) on the ~75 of 83 pages
in this repo that have no images at all.

Verified directly against the installed plugin source
(.venv/lib/python3.11/site-packages/mkdocs_glightbox/plugin.py): both
`on_page_content` (image-wrapping) and `on_post_page` (CSS/JS/init-script
injection) start with the identical guard:

    if "glightbox" in page.meta and page.meta.get("glightbox", True) is False:
        return output

So setting `page.meta["glightbox"] = False` on a page fully and correctly
disables *both* behaviors for that page -- there's no other supported config
path. In particular, the plugin's `manual: true` config option was
considered and rejected: it only changes `_should_skip_img`'s default
(whether an image needs an explicit `on-glb` class / `glightbox: true` meta
to get wrapped) -- it has no effect on `on_post_page`'s unconditional
CSS/JS/init-script injection, so it would not remove any of the per-page
cost this hook targets, and applying it without also annotating every image
site-wide would silently break lightbox entirely.

This hook implements `on_page_markdown` (the earliest per-page hook stage,
running on each page's raw Markdown source before snippet expansion or
rendering) and sets `page.meta["glightbox"] = False` whenever that raw
source contains neither `![` (Markdown image syntax) nor `<img` (raw HTML
`<img>` tag).

Why raw Markdown, not rendered HTML: `on_page_markdown` runs before
`pymdownx.snippets` expands any `--8<--` transclusion, so in principle an
image reaching a page only via a transcluded snippet would be missed here.
A full-repo scan confirmed this doesn't happen: no file under docs/includes/
contains `![` or `<img` (`grep -rlE '!\\[|<img' docs/includes/` -> no
matches), and exactly 8 pages repo-wide contain an image at all. So
raw-Markdown substring detection is safe here and needs no hardcoded page
list -- it stays correct automatically as pages gain or lose images.

Why `on_page_markdown` specifically (as opposed to, say, `on_page_content`,
which would let us check rendered HTML instead): MkDocs's build pipeline
completes the `on_page_markdown` stage for a given page -- across all
plugins and hooks, in whatever order they're registered -- before that same
page's `on_page_content` and `on_post_page` stages begin. So mutating
`page.meta` here is guaranteed to be visible to mkdocs-glightbox's own
checks in both of its later stages, regardless of where this hook sits
relative to the glightbox plugin in mkdocs.yml's `plugins:`/`hooks:` order.

Net effect: the 8 pages with images are left completely untouched (both
plugin stages still run there, same as today); the remaining ~75 pages skip
the plugin's CSS/JS/init-script injection and image-wrapping entirely.
"""

import logging

log = logging.getLogger("mkdocs.hooks.conditional_glightbox")

_IMAGE_MARKERS = ("![", "<img")


def on_page_markdown(markdown: str, page, config, files, **kwargs) -> str:
    """Disable mkdocs-glightbox for pages whose raw Markdown has no image."""
    if not any(marker in markdown for marker in _IMAGE_MARKERS):
        page.meta["glightbox"] = False
        log.debug(
            "conditional_glightbox: no images found, disabling glightbox -> %s",
            page.file.src_uri,
        )
    return markdown
