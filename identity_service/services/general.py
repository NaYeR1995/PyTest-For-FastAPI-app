from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from fastapi.responses import JSONResponse



async def health_check(db: AsyncSession):
    try:
        await db.execute(text('SELECT 1'))  # Use await and text()
        return {"status": "healthy"}
    except Exception:
        raise HTTPException(status_code=500, detail="Database connection failed")
