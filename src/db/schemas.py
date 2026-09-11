"""
Pydantic schemas for request/response validation.

These are DIFFERENT from SQLAlchemy models:
- Schemas: Validate API input/output (what the user sends/receives)
- Models: Store data in the database (what PostgreSQL sees)

Think of it like this:
- SQLAlchemy models = database structure
- Pydantic schemas = API contract
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

# ================== TRADE SCHEMAS ==================

class TradeBase(BaseModel):
    """Common fields for trade requests."""
    symbol: str = Field(..., min_length=1, max_length=20)
    direction: str = Field(..., regex="^(BUY|SELL)$")  # Only BUY or SELL
    entry_price: float = Field(..., gt=0)  # Must be > 0
    exit_price: float = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    open_time: datetime
    close_time: datetime
    notes: Optional[str] = None
    emotion: Optional[str] = None

class TradeCreate(TradeBase):
    """Schema for creating a trade (POST request)."""
    pass

class TradeUpdate(BaseModel):
    """Schema for updating a trade (PUT request)."""
    notes: Optional[str] = None
    emotion: Optional[str] = None

class TradeResponse(TradeBase):
    """Schema for returning a trade (GET response)."""
    id: int
    pnl: float
    win: bool
    created_at: datetime
    
    class Config:
        from_attributes = True  # Convert SQLAlchemy model to dict

# ================== PATTERN SCHEMAS ==================

class PatternBase(BaseModel):
    """Common fields for patterns."""
    name: str = Field(..., min_length=1, max_length=150)
    description: str
    confidence: float = Field(..., ge=0.0, le=1.0)  # Between 0 and 1
    pattern_type: str  # "behavioral", "statistical", "timing"

class PatternCreate(PatternBase):
    """Schema for creating a pattern."""
    evidence_count: int = Field(..., ge=1)

class PatternResponse(PatternBase):
    """Schema for returning a pattern."""
    id: int
    evidence_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ================== ANALYSIS SCHEMAS ==================

class AnalyzeRequest(BaseModel):
    """Schema for POST /analyze endpoint."""
    trades: List[TradeCreate] = Field(..., min_items=1)  # At least 1 trade
    # Optional: provide recent trades for context

class AnalyzeResponse(BaseModel):
    """Response from /analyze endpoint."""
    patterns_found: List[PatternResponse]
    total_trades_analyzed: int
    analysis_summary: str  # Human-readable summary from Claude
