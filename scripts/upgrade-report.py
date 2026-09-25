#!/usr/bin/env python3
"""Describe a lesson upgrade using guidance shipped in the target module.

Requires Python 3.11+. Uses only the standard library. Only assign-release changes
upgrade-note source files, and only their pending release metadata.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tomllib
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path


REPOSITORY = "https://github.com/oer-particle-physics/hugo-styles"
NOTE_DIRECTORY = Path("content/docs/upgrades")
SECTIONS = ("Who is affected", "What changes", "What to do", "How to verify")
VALIDATION_MARKER = "<!-- hugo-styles-upgrade-validation -->"
MANIFEST = ".release-please-manifest.json"
FRONT_MATTER = re.compile(r"\+\+\+\n(.*?)\n\+\+\+\n(.*)", flags=re.S)


def markdown_lines(text: str) -> Iterator[tuple[str, bool]]:
    """Identify fenced/indented code before inspecting or shifting headings."""
    fence = ""
    for line in text.splitlines(keepends=True):
        if fence:
            yield line, True
            if re.fullmatch(rf" {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*", line):
                fence = ""
            continue
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if opening and not (opening[1][0] == "`" and "`" in opening[2]):
            fence = opening[1]
            yield line, True
        else:
            yield line, line.startswith(("    ", "\t"))


def literal_shortcodes(text: str, *, remove: bool = False) -> str:
    """Hugo's escaped examples render as literal shortcode calls on GitHub too."""
    for opening, closing in (("<", ">"), ("%", "%")):
        pattern = r"{{" + re.escape(opening) + r"/\*(.*?)\*/" + re.escape(closing) + r"}}"
        text = re.sub(
            pattern,
            lambda match: "" if remove else "{{" + opening + match[1] + closing + "}}",
            text,
            flags=re.S,
        )
    return text


def validate_body(body: str, path: Path) -> None:
    # Headings in examples or comments cannot satisfy the required sections.
    visible = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line, code in markdown_lines(visible):
        heading = re.match(r"^(#{1,2})\s+(.+?)\s*$", line) if not code else None
        if heading:
            current = heading[2] if heading[1] == "##" else None
            if current and current in sections:
                raise ValueError(f"{path}: duplicate section {current!r}")
            if current:
                sections[current] = []
        elif current:
            if code or not re.match(r"^#{3,6}\s", line):
                sections[current].append(line)
        if not code and re.search(r"\bTODO:|^\s*TBD\s*$", line, flags=re.I):
            raise ValueError(f"{path}: replace scaffold placeholders before review")
    for section in SECTIONS:
        if section not in sections:
            raise ValueError(f"{path}: missing '## {section}' section")
        content = "".join(sections[section])
        content = re.sub(r"(?m)^\s*(?:`{3,}|~{3,}).*$", "", content)
        if not content.strip():
            raise ValueError(f"{path}: section {section!r} must contain guidance")
    if re.search(r"{{[<%]", literal_shortcodes(body, remove=True)):
        raise ValueError(
            f"{path}: escape literal shortcode examples as {{{{</* name */>}}}} "
            "or {{%/* name */%}}; executable shortcodes are not supported"
        )


def render_note_body(body: str) -> str:
    return "".join(
        line if code else re.sub(r"^(#{1,4}) ", r"##\1 ", line)
        for line, code in markdown_lines(literal_shortcodes(body))
    )


def release_version(value: str) -> tuple[int, int, int] | None:
    """Only order stable releases. Report other refs explicitly as uncertain."""
    match = re.fullmatch(r"v?(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", value)
    return tuple(map(int, match.groups())) if match else None


@dataclass(frozen=True)
class Finding:
    title: str
    message: str


def legacy_authors(site: Path) -> Finding | None:
    if not (site / "AUTHORS").is_file():
        return None
    # Check standard content locations, including multilingual homepages. This is
    # deliberately a source check, not an attempt to interpret Hugo configuration.
    uses_authors = False
    for page in (site / "content").rglob("_index*.md"):
        source = re.sub(r"<!--.*?-->", "", page.read_text(encoding="utf-8"), flags=re.S)
        if re.search(r"{{[<%]\s*lesson/authors(?:\s|[>%])", source):
            uses_authors = True
            break
    if not uses_authors:
        return None
    citation = site / "CITATION.cff"
    has_data = citation.is_file() and any(
        line.strip() and not line.lstrip().startswith("#")
        for line in citation.read_text(encoding="utf-8").splitlines()
    )
    if not has_data:
        return Finding(
            "Action required: migrate author information",
            "This lesson uses `lesson/authors` and contains `AUTHORS`, but has no "
            "non-empty `CITATION.cff`. The authors table will disappear even if "
            "the Hugo build passes. Transfer the contributors before merging.",
        )
    return Finding(
        "Review required: reconcile contributor information",
        "This lesson uses `lesson/authors` and contains both `AUTHORS` and "
        "`CITATION.cff`. Only the citation file supplies the table. Check that it "
        "contains every intended contributor; the report does not compare names "
        "or validate the CFF schema.",
    )


CHECKS = {"legacy-authors": legacy_authors}


@dataclass(frozen=True)
class Note:
    path: Path
    title: str
    release: str
    severity: str
    check: str | None
    body: str


def read_notes(module: Path, *, require_released: bool = False) -> list[Note]:
    notes = []
    for path in sorted((module / NOTE_DIRECTORY).glob("*.md")):
        if path.name == "_index.md":
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONT_MATTER.fullmatch(text)
        if not match:
            raise ValueError(f"{path}: expected TOML front matter and Markdown body")
        metadata = tomllib.loads(match[1])
        params = metadata.get("params", {})
        fields = params.get("upgrade", {}) if isinstance(params, dict) else None
        if not isinstance(fields, dict):
            raise ValueError(f"{path}: expected a [params.upgrade] table")
        if metadata.get("draft"):
            raise ValueError(f"{path}: upgrade notes must not be draft pages")
        title = metadata.get("title")
        release = fields.get("release")
        severity = fields.get("severity")
        check = fields.get("check")
        if not isinstance(title, str) or not title.strip() or "\n" in title:
            raise ValueError(f"{path}: title must be a non-empty, single-line string")
        if not isinstance(release, str) or not (
            release_version(release) or release == "unreleased"
        ):
            raise ValueError(f"{path}: release must be a stable version or 'unreleased'")
        if require_released and release == "unreleased":
            raise ValueError(f"{path}: assign the release version before publishing")
        if severity not in ("breaking", "deprecation", "action"):
            raise ValueError(f"{path}: severity must be breaking, deprecation, or action")
        if check is not None and (not isinstance(check, str) or check not in CHECKS):
            raise ValueError(f"{path}: unknown check {check!r}")
        body = match[2].strip()
        validate_body(body, path)
        notes.append(Note(path.relative_to(module), title, release, severity, check, body))
    return notes


def render_note(note: Note, site: Path | None) -> str:
    lines = [f"### {note.title} ({note.release}, {note.severity})", ""]
    finding = CHECKS[note.check](site) if note.check and site else None
    if finding:
        lines += [f"**{finding.title}.** {finding.message}", ""]
    elif site is None:
        lines += ["Applicability has not been checked against a lesson.", ""]
    elif note.check:
        lines += ["The automated check found no legacy usage in the standard content "
                  "locations. Review the affected cases below if you use custom layouts "
                  "or content locations.", ""]
    else:
        lines += ["**Review required:** this change has no automatic applicability check.", ""]
    lines += [render_note_body(note.body), ""]
    return "\n".join(lines)


def build_preview(module: Path, site: Path | None = None, release: str | None = None) -> str:
    if not (module / NOTE_DIRECTORY).is_dir():
        raise ValueError(f"Upgrade-note directory not found: {module / NOTE_DIRECTORY}")
    if site is not None and not site.is_dir():
        raise ValueError(f"Lesson directory not found: {site}")
    if release is not None and release_version(release) is None:
        raise ValueError("Preview release must be a stable version")
    notes = [note for note in read_notes(module) if note.release == "unreleased" or (
        release is not None and release_version(note.release) == release_version(release)
    )]
    lines = ["# Upgrade guidance preview", "",
             "Review of pending guidance" + (f" and notes for {release}." if release else "."),
             "This is an authoring preview, not a completed lesson upgrade or build verification.", ""]
    if not notes:
        lines.append("No notes matched this preview. Use --release VERSION to include assigned notes.")
    for note in notes:
        lines.append(render_note(note, site))
    return "\n".join(lines) + "\n"


def git(module: Path, *arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=module, check=True, capture_output=True, text=True
    ).stdout


def manifest_version(text: str) -> str:
    manifest = json.loads(text)
    value = manifest.get(".") if isinstance(manifest, dict) else None
    if not isinstance(value, str) or release_version(value) is None:
        raise ValueError("The release manifest must contain a stable root version")
    return "v" + ".".join(map(str, release_version(value)))


def tag_exists(module: Path, version: str) -> bool:
    return bool(git(module, "tag", "--list", version).strip())


def check_release(notes: list[Note], version: str) -> None:
    for note in notes:
        if note.release == "unreleased":
            raise ValueError(f"{note.path}: assign the release version before publishing")
        if release_version(note.release) > release_version(version):
            raise ValueError(f"{note.path}: note version is newer than the release manifest {version}")


def assign_release(module: Path) -> list[Path]:
    """Assign pending notes from the release PR's manifest; preserve old notes."""
    version = manifest_version((module / MANIFEST).read_text(encoding="utf-8"))
    notes = read_notes(module)
    pending = [note for note in notes if note.release == "unreleased"]
    if not pending:
        return []
    if tag_exists(module, version):
        raise ValueError(
            f"{version} is already tagged. Run assign-release on the release PR branch "
            "after release-please has updated the manifest."
        )
    check_release([note for note in notes if note.release != "unreleased"], version)
    changes = []
    for note in pending:
        path = module / note.path
        text = path.read_text(encoding="utf-8")
        match = FRONT_MATTER.fullmatch(text)
        front = match[1]
        table = re.search(r"(?ms)^\[params\.upgrade\][ \t]*\n(.*?)(?=^\[|\Z)", front)
        if table is None:
            raise ValueError(f"{path}: use a [params.upgrade] table for version assignment")
        updated, count = re.subn(
            r'''(?m)^(release\s*=\s*)(["'])unreleased\2([ \t]*(?:\#.*)?)$''',
            lambda match: match[1] + '"' + version + '"' + match[3], table[1],
        )
        if count != 1:
            raise ValueError(f"{path}: expected one release = \"unreleased\" line")
        front = front[:table.start(1)] + updated + front[table.end(1):]
        changes.append((path, text[:match.start(1)] + front + text[match.end(1):]))
    # Validate every planned edit before writing any note.
    for path, text in changes:
        path.write_text(text, encoding="utf-8")
    return [path for path, _ in changes]


def check_publication(module: Path) -> bool:
    if not (module / NOTE_DIRECTORY).is_dir():
        raise ValueError("Upgrade-note directory is missing")
    notes = read_notes(module)
    version = manifest_version((module / MANIFEST).read_text(encoding="utf-8"))
    if tag_exists(module, version):
        # Development commits may contain pending notes. Explicitly prevent the
        # following Release Please step from publishing any release in this case.
        return False
    check_release(notes, version)
    return True


def declares_breaking(text: str) -> bool:
    return bool(re.search(
        r"(?m)^[a-z][a-z0-9-]*(?:\([^\n)]+\))?!:|^BREAKING[ -]CHANGE:\s*\S", text
    ))


def check_pr(
    module: Path, base: str, title: str = "", body: str = "",
    github_output: Path | None = None,
) -> str:
    """Validate a PR against its base, returning a release version for preview."""
    if not (module / NOTE_DIRECTORY).is_dir():
        raise ValueError("Upgrade-note directory is missing")
    notes = read_notes(module)
    before = manifest_version(git(module, "show", f"{base}:{MANIFEST}"))
    after = manifest_version((module / MANIFEST).read_text(encoding="utf-8"))
    release = ""
    if before != after:
        if release_version(after) <= release_version(before):
            raise ValueError("The release manifest version must increase")
        release = after
    # Preview all notes for the proposed version even when assignment is missing.
    # This output is informational; publication has its own strict gate.
    if github_output:
        with github_output.open("a", encoding="utf-8") as handle:
            handle.write(f"release-version={release}\n")
    if release:
        check_release(notes, release)
    commits = git(module, "log", "--format=%B", f"{base}..HEAD")
    prose = "".join(line for line, code in markdown_lines(body) if not code)
    if declares_breaking(title) or declares_breaking(prose) or declares_breaking(commits):
        added = set(git(
            module, "diff", "--name-only", "--no-renames", "--diff-filter=A", "-z",
            base, "HEAD", "--", str(NOTE_DIRECTORY),
        ).split("\0"))
        if not any(
            str(note.path) in added and note.severity == "breaking" and (
                note.release == "unreleased" or
                release_version(before) < release_version(note.release) <= release_version(after)
            ) for note in notes
        ):
            raise ValueError(
                "This PR declares a breaking change; add a new breaking upgrade note "
                "in content/docs/upgrades/ with release = \"unreleased\"."
            )
    return release


def changed_files(site: Path) -> list[str]:
    paths: set[str] = set()
    for args in (
        ["diff", "--name-only", "--relative", "-z", "HEAD", "--", "."],
        ["ls-files", "--others", "--exclude-standard", "-z", "--", "."],
    ):
        result = subprocess.run(
            ["git", *args], cwd=site, check=True, capture_output=True, text=True
        )
        paths.update(path for path in result.stdout.split("\0") if path)
    vendor = [path for path in paths if path.startswith("_vendor/")]
    paths.difference_update(vendor)
    # Quote unusual filenames so they cannot create headings or workflow commands.
    items = [f"- `{path.replace('`', '').replace(chr(10), ' ')}`" for path in sorted(paths)]
    if vendor:
        items.append(f"- `_vendor/` ({len(vendor)} changed files)")
    return items


def changelog_entries(module: Path, old: tuple | None, new: tuple | None) -> str:
    changelog = module / "CHANGELOG.md"
    if not changelog.is_file() or old is None or new is None:
        return "Release highlights could not be selected automatically; review the release links above."
    sections = re.split(r"(?=^## )", changelog.read_text(encoding="utf-8"), flags=re.M)
    selected = []
    for section in sections:
        match = re.match(r"## \[?(v?\d+\.\d+\.\d+)(?:\]|\s)", section)
        version = release_version(match[1]) if match else None
        if version and old < version <= new:
            selected.append(section.strip())
    if not selected:
        return "No changelog entries were found for this version range. Review the release links above."
    text = "\n\n".join(selected)
    # Keep room for migration guidance within GitHub's PR body limit.
    if len(text) > 12000:
        text = text[:12000].rsplit("\n", 1)[0] + "\n\n… See the full changelog for remaining entries."
    return f"<details>\n<summary>Changes in the included releases</summary>\n\n{text}\n\n</details>"


def build_report(
    site: Path, module: Path, old_version: str, new_version: str,
    *, title: str = "", extra_body: str = "",
) -> tuple[str, str]:
    for value in (old_version, new_version):
        if not re.fullmatch(r"[A-Za-z0-9.+-]+", value):
            raise ValueError(f"Invalid module version: {value!r}")
    old, new = release_version(old_version), release_version(new_version)
    if old and new and old > new:
        raise ValueError("The target version is older than the installed version; this is not an upgrade")
    title = title or (
        f"chore: update hugo-styles from {old_version} to {new_version}"
        if old_version != new_version else f"chore: refresh hugo-styles {new_version}"
    )
    if "\n" in title or "\r" in title:
        raise ValueError("PR title must be a single line")
    lines = [f"Update **hugo-styles {old_version} → {new_version}**.", ""]
    if new:
        tag = "v" + ".".join(map(str, new))
        lines.append(f"[Target release]({REPOSITORY}/releases/tag/{tag}) · "
                     f"[Full changelog]({REPOSITORY}/blob/{tag}/CHANGELOG.md)")
        if old and old != new:
            old_tag = "v" + ".".join(map(str, old))
            lines.append(f"[Compare versions]({REPOSITORY}/compare/{old_tag}...{tag})")
    else:
        lines.append(f"[Releases and changelogs]({REPOSITORY}/releases)")
    lines += ["", "## Maintainer actions", ""]
    if old is None or new is None:
        lines += [
            "> Version range could not be determined for a non-stable version or unknown "
            "ref. Review the guidance below; some changes may already be applied or "
            "may not apply to this ref.", "",
        ]
    notes = read_notes(module)
    if not (module / NOTE_DIRECTORY).is_dir():
        lines += ["> This module does not provide structured upgrade notes. "
                  "Review its release notes for required changes.", ""]
    if any(note.release == "unreleased" for note in notes):
        lines += ["> This module contains unassigned upgrade notes. "
                  "Its migration guidance may be incomplete; contact the hugo-styles maintainers.", ""]
    selected = []
    for note in notes:
        version = release_version(note.release)
        if version is None or (new and version > new):
            continue
        finding = CHECKS[note.check](site) if note.check else None
        if old is None or new is None or old < version or finding:
            selected.append((note, finding))
    selected.sort(key=lambda item: (item[1] is None, release_version(item[0].release), item[0].path.name))
    for note, _ in selected:
        lines.append(render_note(note, site))
    if not selected and old and new and (module / NOTE_DIRECTORY).is_dir() and not any(
        note.release == "unreleased" for note in notes
    ):
        lines += ["No applicable upgrade notes or unresolved migrations were detected. "
                  "This does not replace reviewing the release notes and rendered lesson.", ""]
    lines += ["## Release highlights", "", changelog_entries(module, old, new), "",
              "## Updated files", ""]
    lines += changed_files(site) or ["No file changes detected."]
    lines += ["", "Managed workflows, module metadata, and `_vendor/` are refreshed together. "
              "Review the rendered lesson before merging.", ""]
    if extra_body.strip():
        lines += ["## Additional context", "", extra_body.strip(), ""]
    lines += [VALIDATION_MARKER, "## Validation", "", "Build verification has not completed.", ""]
    return title, "\n".join(lines)


def finalize_report(path: Path, validation: str, summary: Path | None) -> None:
    messages = {
        "success": "The configured build verification passed. This does not confirm that "
                   "contributor information or other lesson behavior was preserved.",
        "failure": "**Build verification failed.** Resolve the errors and required changes "
                   "before merging. The updater will not create a PR in this run.",
        "skipped": "Build verification was not run. Review and build the lesson before merging.",
        "cancelled": "Build verification was cancelled; its result is unknown.",
    }
    text = path.read_text(encoding="utf-8")
    if VALIDATION_MARKER not in text:
        raise ValueError("Upgrade report has no validation marker")
    text = text.split(VALIDATION_MARKER)[0] + (
        f"{VALIDATION_MARKER}\n## Validation\n\n{messages[validation]}\n"
    )
    path.write_text(text, encoding="utf-8")
    if summary:
        with summary.open("a", encoding="utf-8") as handle:
            handle.write(text + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report", help="Generate a downstream upgrade PR description")
    report.add_argument("--site-root", type=Path, default=Path("."))
    report.add_argument("--module-root", type=Path, required=True)
    report.add_argument("--old-version", required=True)
    report.add_argument("--new-version", required=True)
    report.add_argument("--output", type=Path, required=True)
    report.add_argument("--github-output", type=Path)
    report.add_argument("--title", default="")
    report.add_argument("--extra-body", default="")
    finalize = commands.add_parser("finalize", help="Record verification and publish the job summary")
    finalize.add_argument("--report", type=Path, required=True)
    finalize.add_argument("--validation", choices=("success", "failure", "skipped", "cancelled"), required=True)
    finalize.add_argument("--summary", type=Path)
    check = commands.add_parser("check-notes", help="Validate maintainer upgrade notes")
    check.add_argument("--module-root", type=Path, default=Path(__file__).resolve().parents[1])
    check.add_argument("--require-released", action="store_true")
    preview = commands.add_parser("preview", help="Preview pending guidance without a lesson checkout")
    preview.add_argument("--module-root", type=Path, default=Path(__file__).resolve().parents[1])
    preview.add_argument("--site-root", type=Path)
    preview.add_argument("--release", help="Also include notes assigned to this version")
    preview.add_argument("--output", type=Path, help="Write Markdown here instead of stdout")
    preview.add_argument("--summary", type=Path, help="Also append to an Actions job summary")
    assign = commands.add_parser("assign-release", help="Assign pending notes the release PR's manifest version")
    assign.add_argument("--module-root", type=Path, default=Path(__file__).resolve().parents[1])
    publication = commands.add_parser("check-publication", help="Gate release publication while allowing development notes")
    publication.add_argument("--module-root", type=Path, default=Path(__file__).resolve().parents[1])
    publication.add_argument("--github-output", type=Path)
    pr = commands.add_parser("check-pr", help="Check breaking-change and release-PR requirements")
    pr.add_argument("--module-root", type=Path, default=Path(__file__).resolve().parents[1])
    pr.add_argument("--base-ref", required=True)
    pr.add_argument("--title", default="")
    pr.add_argument("--body", default="")
    pr.add_argument("--github-output", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "check-notes":
            if not (args.module_root / NOTE_DIRECTORY).is_dir():
                raise ValueError("Upgrade-note directory is missing")
            notes = read_notes(args.module_root, require_released=args.require_released)
            print(f"Validated {len(notes)} upgrade notes")
        elif args.command == "preview":
            body = build_preview(args.module_root, args.site_root, args.release)
            if args.output:
                args.output.write_text(body, encoding="utf-8")
            else:
                print(body, end="")
            if args.summary:
                with args.summary.open("a", encoding="utf-8") as handle:
                    handle.write(body + "\n")
        elif args.command == "assign-release":
            paths = assign_release(args.module_root)
            print("\n".join(map(str, paths)) if paths else "No pending notes to assign")
        elif args.command == "check-publication":
            ready = check_publication(args.module_root)
            if args.github_output:
                with args.github_output.open("a", encoding="utf-8") as handle:
                    handle.write(f"publication-ready={str(ready).lower()}\n")
            print("Release guidance is complete" if ready else "Development commit: update release PRs only")
        elif args.command == "check-pr":
            check_pr(args.module_root, args.base_ref, args.title, args.body, args.github_output)
            print("Upgrade-note policy passed")
        elif args.command == "finalize":
            finalize_report(args.report, args.validation, args.summary)
        else:
            title, body = build_report(
                args.site_root, args.module_root, args.old_version, args.new_version,
                title=args.title, extra_body=args.extra_body,
            )
            args.output.write_text(body, encoding="utf-8")
            if args.github_output:
                with args.github_output.open("a", encoding="utf-8") as handle:
                    handle.write(f"title={title}\n")
            print(title)
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Upgrade report failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
