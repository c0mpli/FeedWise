# FeedWise Backend Development Scripts
.PHONY: dev init-db test clean install lint format

# Development server
dev:
	@echo "🚀 Starting development server..."
	python app.py

# Initialize database
init-db:
	@echo "🗄️ Initializing database..."
	python init_database.py


# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

# Clean cache and temp files
clean:
	@echo "🧹 Cleaning cache files..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	find . -name ".pytest_cache" -type d -exec rm -rf {} + 2>/dev/null || true

# Lint code
lint:
	@echo "🔍 Linting code..."
	flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 app/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Format code
format:
	@echo "✨ Formatting code..."
	black app/
	isort app/

# Reset database (clean + init)
reset-db: clean init-db
	@echo "🔄 Database reset complete!"

# Full setup (install + init-db)
setup: install init-db
	@echo "✅ Project setup complete!"

# Show help
help:
	@echo "FeedWise Backend Development Commands:"
	@echo ""
	@echo "  make dev        - Start development server"
	@echo "  make init-db    - Initialize database"
	@echo "  make test       - Run API tests"
	@echo "  make install    - Install dependencies"
	@echo "  make clean      - Clean cache files"
	@echo "  make lint       - Lint code"
	@echo "  make format     - Format code"
	@echo "  make reset-db   - Clean cache + reinit database"
	@echo "  make setup      - Install deps + init database"
	@echo "  make help       - Show this help"