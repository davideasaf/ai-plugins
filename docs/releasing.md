# 🚢 Release Checklist

Use this checklist for changes to plugin runtime instructions, bundled resources, or public behavior. Documentation-only repository changes that do not affect the installed plugin do not require a plugin version bump.

## Versioning

- Choose the next semantic version.
- Set the same version in the changed plugin's `.codex-plugin/plugin.json` and `.claude-plugin/plugin.json` files.
- Bump `.claude-plugin/marketplace.json` when its catalog or a listed plugin changes.
- Never vendor or pin a copy of `last30days`; keep its installation and updates independent.

## Validation

Run from the repository root:

```bash
PLUGIN_NAME=jev-vercel-gateway

uv run --with pyyaml python \
  "${CODEX_HOME:-$HOME/.codex}/skills/.system/plugin-creator/scripts/validate_plugin.py" \
  "plugins/$PLUGIN_NAME"

uv run --with pyyaml python \
  "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" \
  "plugins/$PLUGIN_NAME/skills/$PLUGIN_NAME"

claude plugin validate .
claude plugin validate "./plugins/$PLUGIN_NAME"
```

Run any plugin-specific behavioral tests as well. For Engineering Weekly Newsletter:

```bash

python3 -m unittest discover \
  -s plugins/engineering-weekly-newsletter/skills/engineering-weekly-newsletter/tests

python3 \
  plugins/engineering-weekly-newsletter/skills/engineering-weekly-newsletter/scripts/validate_newsletter.py \
  plugins/engineering-weekly-newsletter/skills/engineering-weekly-newsletter/examples/expected-newsletter.md \
  --strict

```

Confirm the two plugin manifests report the same version:

```bash
python3 - <<'PY'
import json
from pathlib import Path

for plugin_root in sorted(Path("plugins").iterdir()):
    if not plugin_root.is_dir():
        continue
    paths = [
        plugin_root / ".codex-plugin/plugin.json",
        plugin_root / ".claude-plugin/plugin.json",
    ]
    assert all(path.is_file() for path in paths), paths
    versions = {path: json.loads(path.read_text())["version"] for path in paths}
    assert len(set(versions.values())) == 1, versions
    print(plugin_root.name, next(iter(versions.values())))
PY
```

## Publish and verify

- Commit the scoped changes and push `main`.
- Confirm GitHub Actions passes for the published commit.
- Confirm the raw manifests are publicly accessible.
- Test marketplace refresh and installation when packaging behavior changes.
- Tag a stable public release when consumers need a durable version boundary.
