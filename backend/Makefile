# FeedWise Backend Development Scripts
.PHONY: dev init-db clean install reset-db setup

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

# Reset database (clean + init)
reset-db: clean init-db
	@echo "🔄 Database reset complete!"

# Full setup (install + init-db)
setup: install init-db
	@echo "✅ Project setup complete!"
