# Contributing to aio-amazon-ads

Thank you for your interest in contributing to aio-amazon-ads!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/avion23/aio-amazon-ads.git
cd aio-amazon-ads
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=aio_amazon_ads

# Run specific test file
pytest tests/unit/test_client.py -v
```

## Code Quality

We use several tools to maintain code quality:

```bash
# Format code with ruff
ruff format src tests

# Check code with ruff
ruff check src tests

# Type checking with mypy
mypy src
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure they pass
5. Run code quality checks
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## CI/CD

The project uses GitHub Actions for:
- **CI**: Runs tests, linting, and type checking on every push and PR
- **Release**: Automatically publishes to PyPI when a version tag is pushed

To release a new version:
1. Update version in `pyproject.toml`
2. Commit and push
3. Create and push a tag: `git tag v0.1.1 && git push origin v0.1.1`
4. GitHub Actions will automatically build and publish to PyPI

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
