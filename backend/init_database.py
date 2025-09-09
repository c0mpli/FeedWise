#!/usr/bin/env python3
"""
Initialize/recreate database with current schema
"""
from app import create_app
from app.db.database import db
import os

def init_database():
    """Initialize database with current schema"""
    app = create_app()
    
    with app.app_context():
        # Import all models to ensure they're registered
        from app.models import Account, PostsSeen, FollowingRecommendation
        
        # Print model info for debugging
        print("🔍 Loaded models:")
        print(f"  Account columns: {[col.name for col in Account.__table__.columns]}")
        
        # Get database file path
        db_path = app.config.get('SQLALCHEMY_DATABASE_URI', '').replace('sqlite:///', '')
        
        print(f"🗄️  Database file: {db_path}")
        
        # Remove existing database file if it exists
        if db_path and os.path.exists(db_path):
            print(f"🗑️  Removing existing database: {db_path}")
            os.remove(db_path)
        
        # Create all tables with current schema
        print("🏗️  Creating database tables...")
        db.create_all()
        
        # Verify tables were created
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        print("✅ Created tables:")
        for table in tables:
            columns = inspector.get_columns(table)
            print(f"  📋 {table}:")
            for col in columns:
                print(f"    - {col['name']} ({col['type']})")
        
        print("\n🎉 Database initialized successfully!")

if __name__ == "__main__":
    init_database()