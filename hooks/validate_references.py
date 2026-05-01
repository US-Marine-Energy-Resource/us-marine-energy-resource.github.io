"""MkDocs hook: validate BibTeX keywords against locations.json.

For every docs/assets/*.bib file, extract all `keywords` values and verify
each tag is defined in docs/assets/locations.json.  Fails the build if any
tag is missing; warns (log only) for tags defined in locations.json that have
no corresponding BibTeX entries.

We intentionally avoid BibTeX parsing libraries and use a targeted regex
instead, because we own the bib files and enforce a simple format:
    keywords = {tag1, tag2}
No nested braces, no string concatenation.
"""

import json
import logging
import re
from pathlib import Path

log = logging.getLogger("mkdocs.hooks.validate_references")

_DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
_BIB_DIR = _DOCS_DIR / "assets"
_LOCATIONS_FILE = _BIB_DIR / "locations.json"

_KEYWORDS_RE = re.compile(r"keywords\s*=\s*\{([^}]+)\}", re.IGNORECASE)


def _extract_keywords_from_bib(bib_path: Path) -> set[str]:
    """Return the set of all location tags used in a .bib file."""
    content = bib_path.read_text(encoding="utf-8")
    tags: set[str] = set()
    for match in _KEYWORDS_RE.finditer(content):
        for tag in match.group(1).split(","):
            tag = tag.strip()
            if tag:
                tags.add(tag)
    return tags


def on_pre_build(config, **kwargs):
    """Validate all BibTeX keywords against locations.json."""

    if not _LOCATIONS_FILE.exists():
        raise SystemExit(
            f"\nERROR: {_LOCATIONS_FILE} not found.\n"
            "Create docs/assets/locations.json with a {tag: 'Display Name'} mapping.\n"
        )

    locations: dict = json.loads(_LOCATIONS_FILE.read_text(encoding="utf-8"))
    known_tags = {k: v for k, v in locations.items() if not k.startswith("_")}

    bib_files = sorted(_BIB_DIR.glob("*.bib"))
    if not bib_files:
        log.warning("No .bib files found in %s", _BIB_DIR)
        return

    all_used_tags: set[str] = set()
    errors: list[str] = []

    for bib_path in bib_files:
        used = _extract_keywords_from_bib(bib_path)
        all_used_tags |= used
        missing = used - set(known_tags)
        for tag in sorted(missing):
            errors.append(f"  '{tag}' in {bib_path.name} is not defined in locations.json")

    if errors:
        raise SystemExit(
            "\nERROR: BibTeX keywords reference undefined location tags.\n\n"
            + "\n".join(errors)
            + "\n\nAdd the missing tags to docs/assets/locations.json, e.g.:\n"
            '  "tag_name": "Human Readable Location Name"\n'
        )

    unused_tags = set(known_tags) - all_used_tags
    for tag in sorted(unused_tags):
        log.warning(
            "Location tag '%s' (%s) is defined in locations.json but not used in any .bib file",
            tag,
            known_tags[tag],
        )

    log.info(
        "References valid: %d tag(s) across %d .bib file(s)",
        len(all_used_tags),
        len(bib_files),
    )
