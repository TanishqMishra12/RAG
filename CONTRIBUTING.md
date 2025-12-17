# Contributing to Event-Driven RAG Document Assistant

Thank you for considering contributing to this project! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/RAG.git
   cd RAG
   ```
3. Run the setup script:
   ```bash
   ./setup.sh
   ```
4. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Making Changes

1. Make your changes in the appropriate files
2. Test your changes locally
3. Ensure code follows the project style
4. Update documentation if needed

### Testing

Before submitting:
- Test the backend API endpoints
- Test the frontend UI
- Verify document upload and querying works
- Check that Qdrant integration is functional

### Code Style

We use:
- **Black** for Python code formatting
- **isort** for import sorting
- **Type hints** where appropriate

Format your code:
```bash
# Install dev dependencies
pip install black isort

# Format code
black .
isort .
```

## Submitting Changes

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Update documentation as needed

## Areas for Contribution

### Features
- Support for additional document formats (DOCX, TXT, etc.)
- User authentication and authorization
- Document management (delete, update, list)
- Advanced search filters
- Conversation history
- Batch processing

### Improvements
- Performance optimizations
- Better error handling
- Enhanced UI/UX
- Additional tests
- Documentation improvements

### Bug Fixes
- Report bugs via GitHub Issues
- Include steps to reproduce
- Provide system information

## Code Organization

```
backend/app/
├── api/            # API endpoints and routes
├── models/         # Pydantic models and schemas
├── services/       # Business logic and services
├── config.py       # Configuration management
└── main.py         # FastAPI application entry point

frontend/
└── app.py          # Streamlit UI application
```

## Questions?

Feel free to open an issue for:
- Feature requests
- Bug reports
- Questions about the code
- Suggestions for improvements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for your contributions! 🎉
