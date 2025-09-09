# FeedWise Backend

FeedWise is a browser-use powered tool that cleans and personalizes social media feeds.  
This backend handles accounts, preferences, recommendations, and feed cleaning with a streamlined onboarding flow.

## Setup

### Prerequisites

- Python 3.8+
- pip

### Quick Start

1. **Install dependencies:**

   ```bash
   make install
   # or: pip install -r requirements.txt
   ```

2. **Initialize database:**

   ```bash
   make init-db
   # or: python init_database.py
   ```

3. **Start development server:**
   ```bash
   make dev
   # or: python app.py
   ```

The server will start at `http://127.0.0.1:5000`

## Available Scripts

Use the Makefile for common development tasks:

```bash
make dev        # Start development server
make init-db    # Initialize database
make install    # Install dependencies
make clean      # Clean cache files
make reset-db   # Clean cache + reinit database
make setup      # Install deps + init database
```

## Database

SQLite database is automatically created when you run `make init-db`. The database includes:

- Accounts (username, password, platform, preferences)
- Posts Seen (tracking viewed content)
- Following Recommendations (with follow status)

## TODO

- [ ] Create user model (1 user has multiple accounts)
- [ ] Add authentication middleware
- [ ] Support multiple platforms per user
- [ ] Implement JWT token-based auth
- [ ] Add user registration/login endpoints
- [ ] Update onboarding flow for multi-account support
- [ ] Add account switching functionality
- [ ] Add API rate limiting
