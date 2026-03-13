#!/usr/bin/env python3
"""
Simple database initialization script - compatible with older SQLAlchemy
"""
import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

async def test_connection():
    """Test database connection without complex imports."""
    try:
        import asyncpg
        from src.config import settings
        
 