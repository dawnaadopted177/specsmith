# Release Workflow

specsmith uses **gitflow** branching with **SemVer** versioning and **Keep a Changelog** format.

## Branches

- **`main`** — Production. Every commit is a released version. Tags trigger PyPI publish.
- **`develop`** — Integration. Features merge here first. When ready for release, merge to main.
- **`feature/*`** — Branch from `develop`, merge back to `develop` via PR.
- **`hotfix/*`** — Branch from `main` for urgent fixes, merge to **both** `main` and `develop`.
- **`release/*`** — Optional. Branch from `develop` for release prep, merge to `main` + `develop`.

## Feature Release (minor/patch)

When features on `develop` are ready for release:

```bash
# 1. Ensure develop is clean
git checkout develop
pytest tests/ -q && ruff check src/ tests/ && mypy src/

# 2. Bump version in ALL places
#    - pyproject.toml (version)
#    - src/specsmith/__init__.py (__version__)
#    - src/specsmith/config.py (spec_version default)
#    - tests/test_smoke.py (version assertion)
#    - tests/test_cli.py (version assertion + upgrade test)

# 3. Update CHANGELOG.md
#    - Move [Unreleased] items into new [X.Y.Z] - YYYY-MM-DD section
#    - Update comparison links at bottom

# 4. Update docs if needed
#    - docs/site/*.md (remove any alpha/pre-release references)
#    - README.md (install command, version references)

# 5. Commit on develop
git add -A && git commit -m "release: vX.Y.Z"

# 6. Merge develop → main
git checkout main
git merge develop --no-edit

# 7. Tag on main
git tag -a vX.Y.Z -m "vX.Y.Z — description"

# 8. Merge back to develop (so develop has the version bump)
git checkout develop
git merge main --no-edit

# 9. Push everything
git push origin main develop --tags

# 10. Verify
#     - CI passes on main
#     - Release workflow: build ✓, pypi-publish ✓, github-release ✓
#     - pip index versions specsmith → shows new version
#     - RTD rebuilds with updated docs
```

## Hotfix Release

For urgent fixes (security vulnerabilities, critical bugs) that can't wait for the next feature release:

```bash
# 1. Branch from main
git checkout -b hotfix/description main

# 2. Apply fix (or cherry-pick from develop if already fixed there)
git cherry-pick <commit>

# 3. Bump PATCH version (X.Y.Z → X.Y.Z+1) in all 5 places

# 4. Add ### Security or ### Fixed section to CHANGELOG.md

# 5. Commit
git add -A && git commit -m "release: vX.Y.Z+1 — hotfix description"

# 6. Merge to main + tag
git checkout main
git merge hotfix/description --no-edit
git tag -a vX.Y.Z+1 -m "vX.Y.Z+1 — hotfix"

# 7. Merge to develop
git checkout develop
git merge hotfix/description --no-edit

# 8. Delete hotfix branch
git branch -d hotfix/description

# 9. Push everything
git push origin main develop --tags
```

## Version Locations (5 places)

Every release must update version in ALL of these:

1. `pyproject.toml` → `version = "X.Y.Z"`
2. `src/specsmith/__init__.py` → `__version__ = "X.Y.Z"`
3. `src/specsmith/config.py` → `spec_version` Field default
4. `tests/test_smoke.py` → version assertion
5. `tests/test_cli.py` → version output assertion + upgrade test version

## CHANGELOG Format

Follow [Keep a Changelog](https://keepachangelog.com/):

```markdown
## [Unreleased]

## [X.Y.Z] - YYYY-MM-DD

### Added      ← new features
### Changed    ← changes to existing features
### Deprecated ← soon-to-be removed features
### Removed    ← removed features
### Fixed      ← bug fixes
### Security   ← vulnerability fixes
```

## Automated Publishing

When a tag matching `v*` is pushed to `main`, the release workflow automatically:

1. **Builds** sdist + wheel
2. **Publishes to PyPI** via OIDC trusted publishing (no tokens needed)
3. **Creates GitHub Release** with auto-generated notes and artifacts
