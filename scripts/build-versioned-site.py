#!/usr/bin/env python3

from __future__ import annotations

import argparse
import copy
import fnmatch
import json
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


@dataclass(frozen=True)
class BuildTarget:
    name: str
    label: str
    kind: str
    git_ref: str | None
    base_url: str
    menu_path: str
    destination: Path
    include_in_menu: bool


class BuildError(RuntimeError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build a Hugo site with an auto-generated version menu. "
            "By default this publishes the configured primary branch as the site root "
            "and optional branch/tag builds under versions/<name>/."
        )
    )
    parser.add_argument(
        "--source",
        default=".",
        help="Path to the Hugo site root. Defaults to the current directory.",
    )
    parser.add_argument(
        "--config",
        default="hugo.toml",
        help="Hugo config file to load from the site root. Defaults to hugo.toml.",
    )
    parser.add_argument(
        "--destination",
        default="public",
        help="Output directory for the built site. Defaults to public.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help="Override the site's production base URL.",
    )
    parser.add_argument(
        "--hugo-bin",
        default="hugo",
        help="Hugo executable to use. Defaults to hugo.",
    )
    parser.add_argument(
        "--cache-dir",
        default=None,
        help="Directory for Hugo's cache. Defaults to .hugo-versioned-cache inside the site root.",
    )
    parser.add_argument(
        "--no-minify",
        action="store_true",
        help="Skip Hugo's --minify flag.",
    )
    return parser.parse_args()


def run(
    command: list[str],
    *,
    cwd: Path,
    capture_output: bool = False,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            cwd=cwd,
            check=True,
            text=True,
            capture_output=capture_output,
        )
    except FileNotFoundError as exc:
        raise BuildError(f"Command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        if capture_output:
            output = exc.stderr or exc.stdout or ""
            raise BuildError(output.strip() or f"Command failed: {' '.join(command)}") from exc
        raise BuildError(f"Command failed: {' '.join(command)}") from exc


def lower_keys(value: object) -> object:
    if isinstance(value, dict):
        return {str(key).lower(): lower_keys(child) for key, child in value.items()}
    if isinstance(value, list):
        return [lower_keys(item) for item in value]
    return value


def as_bool(value: object, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def as_str_list(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def normalize_base_url(value: str) -> str:
    if not value:
        return "/"
    parts = urlsplit(value)
    path = parts.path or "/"
    if not path.startswith("/"):
        path = f"/{path}"
    if not path.endswith("/"):
        path = f"{path}/"
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def site_root_path(base_url: str) -> str:
    path = urlsplit(base_url).path or "/"
    if not path.startswith("/"):
        path = f"/{path}"
    if not path.endswith("/"):
        path = f"{path}/"
    return path


def join_url(base_url: str, *parts: str) -> str:
    parsed = urlsplit(normalize_base_url(base_url))
    path = site_root_path(base_url)
    for part in parts:
        cleaned = str(part).strip("/")
        if cleaned:
            path = f"{path.rstrip('/')}/{cleaned}/"
    return urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def join_site_path(root_path: str, *parts: str) -> str:
    path = root_path
    for part in parts:
        cleaned = str(part).strip("/")
        if cleaned:
            path = f"{path.rstrip('/')}/{cleaned}/"
    return path


def git_output(repo_root: Path, *args: str) -> str:
    return run(["git", *args], cwd=repo_root, capture_output=True).stdout.strip()


def detect_git_repo(site_root: Path) -> Path | None:
    try:
        top_level = git_output(site_root, "rev-parse", "--show-toplevel")
    except BuildError:
        return None
    return Path(top_level).resolve()


def current_branch_name(repo_root: Path | None) -> str | None:
    if repo_root is None:
        return None
    try:
        branch = git_output(repo_root, "branch", "--show-current")
    except BuildError:
        return None
    return branch or None


def load_hugo_config(
    site_root: Path,
    config_name: str,
    hugo_bin: str,
    base_url: str | None,
    cache_dir: Path,
) -> dict:
    command = [
        hugo_bin,
        "config",
        "--format",
        "json",
        "--config",
        config_name,
        "--cacheDir",
        str(cache_dir),
    ]
    if base_url:
        command.extend(["--baseURL", base_url])
    raw = run(command, cwd=site_root, capture_output=True).stdout.strip()
    if not raw:
        raise BuildError("Hugo config returned empty output.")
    return lower_keys(json.loads(raw))


def list_branch_refs(repo_root: Path) -> tuple[list[str], dict[str, str]]:
    branch_refs: dict[str, str] = {}

    local_branches = git_output(
        repo_root,
        "for-each-ref",
        "--format=%(refname:short)",
        "refs/heads",
    ).splitlines()
    for name in local_branches:
        branch_refs[name] = f"refs/heads/{name}"

    remote_branches = git_output(
        repo_root,
        "for-each-ref",
        "--format=%(refname:short)",
        "refs/remotes/origin",
    ).splitlines()
    for short_name in remote_branches:
        if short_name in {"origin", "origin/HEAD"}:
            continue
        branch_name = short_name.removeprefix("origin/")
        branch_refs.setdefault(branch_name, f"refs/remotes/{short_name}")

    return sorted(branch_refs), branch_refs


def list_tag_refs(repo_root: Path) -> tuple[list[str], dict[str, str]]:
    tags = git_output(repo_root, "tag", "--sort=-version:refname").splitlines()
    tag_refs = {name: f"refs/tags/{name}" for name in tags}
    return tags, tag_refs


def resolve_named_refs(
    *,
    label: str,
    ref_config: dict,
    available_names: list[str],
    available_refs: dict[str, str],
) -> list[tuple[str, str]]:
    selected: list[str] = []

    for name in as_str_list(ref_config.get("refs")):
        if name not in available_refs:
            raise BuildError(f"Configured {label} ref '{name}' was not found locally.")
        if name not in selected:
            selected.append(name)

    discovered: list[str] = []
    if as_bool(ref_config.get("all")):
        discovered.extend(available_names)
    for pattern in as_str_list(ref_config.get("patterns")):
        discovered.extend(
            name for name in available_names if fnmatch.fnmatchcase(name, pattern)
        )

    for name in discovered:
        if name not in selected:
            selected.append(name)

    return [(name, available_refs[name]) for name in selected]


def slugify_identifier(value: str) -> str:
    characters: list[str] = []
    for char in value.lower():
        if char.isalnum():
            characters.append(char)
        else:
            characters.append("-")
    slug = "".join(characters).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "version"


def remove_managed_version_menu(menu_items: list[dict], menu_identifier: str) -> list[dict]:
    cleaned: list[dict] = []
    for item in menu_items:
        identifier = str(item.get("identifier", ""))
        parent = str(item.get("parent", ""))
        generated = as_bool((item.get("params") or {}).get("hugostylesversioning"))
        if identifier == menu_identifier or parent == menu_identifier or generated:
            continue
        cleaned.append(item)
    return cleaned


def apply_version_menu(config: dict, versioning: dict, menu_items: list[BuildTarget]) -> dict:
    updated = copy.deepcopy(config)
    menus = updated.setdefault("menus", {})
    main_menu = list(menus.get("main") or [])

    menu_identifier = str(versioning.get("menuidentifier") or "versions")
    menu_name = str(versioning.get("menuname") or "Versions")
    menu_weight = int(versioning.get("menuweight") or 70)

    main_menu = remove_managed_version_menu(main_menu, menu_identifier)

    if menu_items:
        main_menu.append(
            {
                "identifier": menu_identifier,
                "name": menu_name,
                "weight": menu_weight,
                "params": {"hugostylesversioning": True},
            }
        )
        for index, item in enumerate(menu_items, start=1):
            main_menu.append(
                {
                    "identifier": f"{menu_identifier}-{slugify_identifier(item.name)}",
                    "name": item.label,
                    "parent": menu_identifier,
                    "url": item.menu_path,
                    "weight": index * 10,
                    "params": {"hugostylesversioning": True},
                }
            )

    menus["main"] = main_menu
    updated["menus"] = menus
    return updated


def write_generated_config(config: dict, target: BuildTarget, directory: Path) -> Path:
    generated = copy.deepcopy(config)
    generated["baseurl"] = target.base_url
    path = directory / f"{slugify_identifier(target.name)}.json"
    path.write_text(json.dumps(generated, indent=2), encoding="utf-8")
    return path


def build_hugo_site(
    *,
    hugo_bin: str,
    config_path: Path,
    site_root: Path,
    destination: Path,
    base_url: str,
    cache_dir: Path,
    minify: bool,
) -> None:
    command = [
        hugo_bin,
        "--config",
        str(config_path),
        "--source",
        str(site_root),
        "--destination",
        str(destination),
        "--baseURL",
        base_url,
        "--cacheDir",
        str(cache_dir),
        "--gc",
    ]
    if minify:
        command.append("--minify")
    run(command, cwd=site_root)


def ensure_within_repo(site_root: Path, repo_root: Path) -> Path:
    try:
        return site_root.relative_to(repo_root)
    except ValueError as exc:
        raise BuildError(
            f"Site root {site_root} must be inside the git repository {repo_root}."
        ) from exc


def resolve_latest_ref(
    *,
    latest_ref_name: str,
    branch_refs: dict[str, str],
    tag_refs: dict[str, str],
) -> str:
    if latest_ref_name in branch_refs:
        return branch_refs[latest_ref_name]
    if latest_ref_name in tag_refs:
        return tag_refs[latest_ref_name]
    raise BuildError(
        f"The primary version ref '{latest_ref_name}' was not found as a local branch, remote branch, or tag."
    )


def resolve_targets(
    *,
    versioning: dict,
    base_url: str,
    destination_root: Path,
    repo_root: Path | None,
    current_branch: str | None,
) -> list[BuildTarget]:
    enable_versioning = as_bool(versioning.get("enable"), default=False)

    latest_cfg = versioning.get("latest") or {}
    latest_enabled = enable_versioning and as_bool(latest_cfg.get("enable"), default=True)
    latest_label = str(latest_cfg.get("label") or "Latest")
    default_branch = str(versioning.get("defaultbranch") or "main")
    latest_ref_name = str(latest_cfg.get("ref") or default_branch)

    targets: list[BuildTarget] = []

    branch_names: list[str] = []
    branch_refs: dict[str, str] = {}
    tag_names: list[str] = []
    tag_refs: dict[str, str] = {}
    if repo_root is not None:
        branch_names, branch_refs = list_branch_refs(repo_root)
        tag_names, tag_refs = list_tag_refs(repo_root)

    root_git_ref: str | None = None
    if enable_versioning and repo_root is not None:
        if current_branch != latest_ref_name:
            root_git_ref = resolve_latest_ref(
                latest_ref_name=latest_ref_name,
                branch_refs=branch_refs,
                tag_refs=tag_refs,
            )

    if enable_versioning:
        targets.append(
            BuildTarget(
                name="latest",
                label=latest_label,
                kind="root",
                git_ref=root_git_ref,
                base_url=normalize_base_url(base_url),
                menu_path="/",
                destination=destination_root,
                include_in_menu=latest_enabled,
            )
        )
    else:
        targets.append(
            BuildTarget(
                name="site",
                label="Site",
                kind="root",
                git_ref=root_git_ref,
                base_url=normalize_base_url(base_url),
                menu_path="/",
                destination=destination_root,
                include_in_menu=False,
            )
        )
        return targets

    if repo_root is None:
        return targets

    selected_branches = resolve_named_refs(
        label="branch",
        ref_config=versioning.get("branches") or {},
        available_names=branch_names,
        available_refs=branch_refs,
    )
    selected_tags = resolve_named_refs(
        label="tag",
        ref_config=versioning.get("tags") or {},
        available_names=tag_names,
        available_refs=tag_refs,
    )

    version_names: set[str] = set()
    for kind, selected in (("branch", selected_branches), ("tag", selected_tags)):
        for ref_name, git_ref in selected:
            if latest_enabled and ref_name == latest_ref_name:
                continue
            if ref_name in version_names:
                raise BuildError(
                    f"Version name collision: '{ref_name}' was selected more than once."
                )
            version_names.add(ref_name)
            targets.append(
                BuildTarget(
                    name=ref_name,
                    label=ref_name,
                    kind=kind,
                    git_ref=git_ref,
                    base_url=join_url(base_url, "versions", ref_name),
                    menu_path=join_site_path("/", "versions", ref_name),
                    destination=destination_root / "versions" / ref_name,
                    include_in_menu=True,
                )
            )

    return targets


def prepare_worktrees(
    *,
    repo_root: Path,
    site_relative_root: Path,
    targets: list[BuildTarget],
    temp_dir: Path,
) -> tuple[dict[str, Path], list[Path]]:
    worktree_roots: dict[str, Path] = {}
    registered_worktrees: list[Path] = []

    for target in targets:
        if target.git_ref is None or target.git_ref in worktree_roots:
            continue
        worktree_root = temp_dir / slugify_identifier(target.name)
        run(
            ["git", "worktree", "add", "--detach", str(worktree_root), target.git_ref],
            cwd=repo_root,
        )
        worktree_roots[target.git_ref] = worktree_root / site_relative_root
        registered_worktrees.append(worktree_root)

    return worktree_roots, registered_worktrees


def main() -> int:
    args = parse_args()
    site_root = Path(args.source).resolve()
    if not site_root.exists():
        raise BuildError(f"Site root does not exist: {site_root}")

    repo_root = detect_git_repo(site_root)
    cache_dir = Path(args.cache_dir).resolve() if args.cache_dir else site_root / ".hugo-versioned-cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    hugo_config = load_hugo_config(
        site_root,
        args.config,
        args.hugo_bin,
        args.base_url,
        cache_dir,
    )
    versioning = hugo_config.get("params", {}).get("versioning") or {}

    configured_base_url = args.base_url or str(hugo_config.get("baseurl") or "")
    base_url = normalize_base_url(configured_base_url)
    destination_root = (site_root / args.destination).resolve()

    targets = resolve_targets(
        versioning=versioning,
        base_url=base_url,
        destination_root=destination_root,
        repo_root=repo_root,
        current_branch=current_branch_name(repo_root),
    )
    menu_targets = [target for target in targets if target.include_in_menu]

    if destination_root.exists():
        shutil.rmtree(destination_root)
    destination_root.mkdir(parents=True, exist_ok=True)

    minify = not args.no_minify
    with tempfile.TemporaryDirectory(prefix="hugo-styles-versioned-") as temp_name:
        temp_dir = Path(temp_name)
        generated_config = apply_version_menu(hugo_config, versioning, menu_targets)

        site_relative_root = Path(".")
        if repo_root is not None:
            site_relative_root = ensure_within_repo(site_root, repo_root)

        worktree_roots: dict[str, Path] = {}
        registered_worktrees: list[Path] = []
        if repo_root is not None:
            worktree_roots, registered_worktrees = prepare_worktrees(
                repo_root=repo_root,
                site_relative_root=site_relative_root,
                targets=targets,
                temp_dir=temp_dir,
            )

        try:
            for target in targets:
                build_root = site_root if target.git_ref is None else worktree_roots[target.git_ref]
                build_root = build_root.resolve()
                target.destination.mkdir(parents=True, exist_ok=True)

                label = f"{target.label} ({target.kind})"
                print(f"Building {label} -> {target.destination}")

                config_path = write_generated_config(generated_config, target, temp_dir)
                build_hugo_site(
                    hugo_bin=args.hugo_bin,
                    config_path=config_path,
                    site_root=build_root,
                    destination=target.destination,
                    base_url=target.base_url,
                    cache_dir=cache_dir,
                    minify=minify,
                )
        finally:
            if repo_root is not None:
                for worktree in reversed(registered_worktrees):
                    try:
                        run(["git", "worktree", "remove", "--force", str(worktree)], cwd=repo_root)
                    except BuildError:
                        pass

    print(f"Finished building versioned site in {destination_root}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BuildError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
