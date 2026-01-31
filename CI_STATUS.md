# CI/CD Status

## ✅ CI/CD is Working!

**Repository:** https://github.com/avion23/aio-amazon-ads

### Continuous Integration (CI)

**Status:** ✅ PASSING

**What it does:**
- Runs on every push to `main`/`develop` branches
- Runs on all pull requests to `main`
- Tests across Python 3.10, 3.11, 3.12, 3.13, 3.14
- Performs:
  1. **Linting** with ruff (code style and import sorting)
  2. **Type checking** with mypy
  3. **Testing** with pytest + coverage
  4. **Coverage reporting** to Codecov

**Latest Run:** ✅ All 5 Python versions passing

### Release Workflow

**Status:** ✅ CONFIGURED

**What it does:**
- Triggers on version tags (e.g., `v0.1.0`)
- Builds package
- Publishes to PyPI automatically
- Creates GitHub Release

**To release a new version:**

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Commit and push
4. Create and push a tag:
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```
5. GitHub Actions will automatically:
   - Build the package
   - Publish to PyPI
   - Create a GitHub Release

**Setup required:**
- Add `PYPI_API_TOKEN` secret to GitHub repository settings

### Development Dependencies

All required for CI:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-httpx` - HTTP client mocking
- `pytest-cov` - Coverage reporting
- `respx` - HTTP mocking for tests
- `mypy` - Type checking
- `ruff` - Linting and formatting

### Current Status

- ✅ CI: PASSING (all Python versions)
- ✅ Tests: 13 passing
- ✅ Linting: Clean
- ✅ Type checking: Clean
- ✅ Coverage: Reporting to Codecov
