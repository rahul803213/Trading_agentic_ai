"""
Database connection and session management.

This file handles:
1. Creating a connection string to PostgreSQL
2. Creating a "session" (like a conversation with the database)
3. Making sure sessions are properly closed (cleanup)
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.core.config import settings

# Create the database engine (the connection to PostgreSQL)
# think of this like dialing a phone number to call the database
engine = create_engine(
    settings.database_url,
    # pooling: reuse connections (don't create new one each time)
    pool_pre_ping=True,  # ping database before using connection (check if it's alive)
)

# SessionLocal: a factory that creates new database sessions
# Each request gets its own session (like a transaction)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """
    Dependency injection for FastAPI.
    
    This function:
    1. Creates a new database session
    2. Yields it to the route handler
    3. Automatically closes it when done (finally block)
    
    Usage in FastAPI:
    @app.get("/trades")
    def get_trades(db: Session = Depends(get_db)):
        # db is automatically injected!
        trades = db.query(Trade).all()
        return trades
    """
    db = SessionLocal()
    try:
        yield db  # Give session to the route handler
    finally:
        db.close()  # Always close, even if there's an error

def init_db():
    """
    Create all tables in the database (only if they don't exist).
    
    Run this ONCE at startup.
    """
    from src.db.models import Base
    Base.metadata.create_all(bind=engine)
