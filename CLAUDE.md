# Orchestra

## Plugin version

Bump `version` in `.claude-plugin/plugin.json` in the same change whenever anything under `skills/`, `agents/`, `hooks/` or `cli/` changes. `cli/pyproject.toml` carries the same version, bumped together, because `orchestra setup` compares the two. Use a minor bump for new capability and a patch bump for fixes and refinements.
