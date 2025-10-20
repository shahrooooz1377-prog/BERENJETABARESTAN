from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

DB_PATH = Path(__file__).resolve().parents[1] / "rice_store.db"

@router.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@router.get('/register', response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

@router.post('/register', response_class=HTMLResponse)
def register_customer(request: Request, name: str = Form(...), phone: str = Form(...), city: str = Form(...)):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT UNIQUE,
        city TEXT
    )""")
    try:
        cur.execute('INSERT INTO customers (name, phone, city) VALUES (?, ?, ?)', (name, phone, city))
        conn.commit()
        msg = f"✅ {name} با موفقیت ثبت شد!"
    except sqlite3.IntegrityError:
        msg = f"⚠️ شماره {phone} قبلاً ثبت شده است."
    finally:
        conn.close()
    return templates.TemplateResponse('index.html', {'request': request, 'message': msg})