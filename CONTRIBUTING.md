# Contributing to Composer Trade Python SDK

Thank you for your interest in contributing to the Composer Trade Python SDK! We welcome contributions from the community.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/composer-trade/composer-trade-py.git
cd composer-trade-py
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Code Style

We use the following tools to maintain code quality:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Run the following commands before submitting a PR:

```bash
# Format code
black composer examples

# Run linter
ruff check composer examples

# Type check
mypy composer
```

## Testing

Run the test suite:

```bash
pytest
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure code quality checks pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

## Questions?

Feel free to open an issue if you have any questions or need clarification.
