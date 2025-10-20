from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

DB_PATH = Path(__file__).resolve().parents[1] / "rice_store.db"

@router.get('/festivals', response_class=HTMLResponse)
def list_festivals(request: Request):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS festivals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        image_url TEXT,
        date TEXT
    )""")
    cur.execute('SELECT id, title, description, image_url, date FROM festivals ORDER BY id DESC')
    rows = cur.fetchall()
    festivals = [{'id': r[0], 'title': r[1], 'description': r[2], 'image_url': r[3], 'date': r[4]} for r in rows]
    conn.close()
    return templates.TemplateResponse('festivals.html', {'request': request, 'festivals': festivals})