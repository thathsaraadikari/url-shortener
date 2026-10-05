from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, get_db
from .utils import generate_code, utcnow

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener", version="1.0.0")


def get_unique_code(db: Session) -> str:
    for _ in range(10):
        code = generate_code()
        exists = db.query(models.URL).filter(models.URL.short_code == code).first()
        if not exists:
            return code
    raise HTTPException(status_code=500, detail="Could not generate a unique code")


@app.post("/shorten", response_model=schemas.URLResponse, status_code=201)
def shorten(payload: schemas.URLCreate, request: Request, db: Session = Depends(get_db)):
    code = get_unique_code(db)
    url = models.URL(
        original_url=str(payload.original_url),
        short_code=code,
        expires_at=payload.expires_at,
    )
    db.add(url)
    db.commit()
    return {
        "short_code": code,
        "short_url": str(request.base_url) + code,
        "original_url": url.original_url,
    }


@app.get("/stats/{code}", response_model=schemas.StatsResponse)
def stats(code: str, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter(models.URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="Short link not found")

    total = (
        db.query(func.count(models.Click.id))
        .filter(models.Click.url_id == url.id)
        .scalar()
    )
    recent = (
        db.query(models.Click)
        .filter(models.Click.url_id == url.id)
        .order_by(models.Click.clicked_at.desc())
        .limit(10)
        .all()
    )
    return {
        "short_code": url.short_code,
        "original_url": url.original_url,
        "created_at": url.created_at,
        "total_clicks": total,
        "recent_clicks": recent,
    }


@app.get("/{code}")
def redirect(code: str, request: Request, db: Session = Depends(get_db)):
    url = db.query(models.URL).filter(models.URL.short_code == code).first()
    if not url:
        raise HTTPException(status_code=404, detail="Short link not found")
    if url.expires_at and url.expires_at < utcnow():
        raise HTTPException(status_code=410, detail="This link has expired")

    user_agent = (request.headers.get("user-agent") or "")[:255]
    db.add(models.Click(url_id=url.id, user_agent=user_agent))
    db.commit()
    return RedirectResponse(url.original_url, status_code=302)