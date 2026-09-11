"""
Database models (ORM classes).
These define the structure of data in PostgreSQL.

Think of this like a blueprint: "A Trade has these fields and these rules."
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# This "Base" is the foundation for all our models
Base = declarative_base()

class Trade(Base):
    """
    Represents a single trade from the trader's journal.
    
    Columns:
    - id: Unique identifier (auto-incrementing)
    - symbol: Trading pair (e.g., "EURUSD", "GBPUSD")
    - direction: "BUY" or "SELL"
    - entry_price: Price at which trade was opened
    - exit_price: Price at which trade was closed
    - quantity: Amount of units traded
    - open_time: When the trade started
    - close_time: When the trade ended
    - pnl: Profit/Loss (calculated)
    - notes: Free-text journal notes (THIS IS KEY for pattern detection!)
    - emotion: Tagged emotion at trade time (happy, anxious, frustrated)
    - win: True if profitable, False if loss
    - created_at: When this record was created in our system
    """
    
    __tablename__ = "trades"  # This is the table name in PostgreSQL
    
    # Primary key (unique identifier for each trade)
    id = Column(Integer, primary_key=True, index=True)
    
    # Trade details
    symbol = Column(String(20), index=True)  # e.g., "EURUSD"
    direction = Column(String(4))             # "BUY" or "SELL"
    entry_price = Column(Float)
    exit_price = Column(Float)
    quantity = Column(Integer)
    
    # Timing
    open_time = Column(DateTime, index=True)
    close_time = Column(DateTime, index=True)
    
    # Performance
    pnl = Column(Float)  # Profit/Loss
    win = Column(Boolean)  # True = profitable, False = loss
    
    # Journal data (crucial for behavioral pattern detection)
    notes = Column(Text, nullable=True)  # "Entered quickly after stop loss, was frustrated"
    emotion = Column(String(50), nullable=True)  # "anxious", "frustrated", "confident"
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        """How to print a Trade object (for debugging)"""
        return f"<Trade(id={self.id}, symbol={self.symbol}, pnl={self.pnl}, win={self.win})>"


class Pattern(Base):
    """
    Represents a detected behavioral pattern.
    
    Examples:
    - "Oversizing after losses" (you increase position size 2+ times in a row after losses)
    - "Revenge trading" (entering trades quickly after a loss)
    - "Time-of-day bias" (your win rate drops at specific times)
    """
    
    __tablename__ = "patterns"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Pattern details
    name = Column(String(150))  # e.g., "Oversizing After Losses"
    description = Column(Text)  # Full explanation of the pattern
    
    # How confident are we? 0.0 = guess, 1.0 = certainty
    confidence = Column(Float)  # e.g., 0.87 (87% confidence)
    
    # Pattern type (helps categorize)
    pattern_type = Column(String(50))  # "behavioral", "statistical", "timing"
    
    # Evidence (e.g., "Found in 12 out of 50 trades")
    evidence_count = Column(Integer)  # How many trades match this
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Pattern(name={self.name}, confidence={self.confidence})>"


class PatternMatch(Base):
    """
    Represents a specific trade that matches a pattern.
    
    Example: Trade #42 matches Pattern #3 (Revenge Trading)
    """
    
    __tablename__ = "pattern_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys (links to Trade and Pattern)
    pattern_id = Column(Integer, index=True)  # Which pattern?
    trade_id = Column(Integer, index=True)    # Which trade?
    
    # Why does this trade match?
    evidence = Column(Text)  # e.g., "Entered 2 min after previous loss, 2x normal size"
    
    # How strong is the match? 0.0 = weak, 1.0 = definite
    match_strength = Column(Float)  # e.g., 0.92
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PatternMatch(pattern_id={self.pattern_id}, trade_id={self.trade_id})>"
