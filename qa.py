from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')
DB_PATH = Path(__file__).resolve().parents[1] / 'rice_store.db'

@router.get('/qa', response_class=HTMLResponse)
def qa_list(request: Request):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS faqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        answer TEXT,
        keywords TEXT
    )""")
    cur.execute('SELECT id, question, answer FROM faqs ORDER BY id DESC')
    rows = cur.fetchall()
    faqs = [{'id': r[0], 'question': r[1], 'answer': r[2]} for r in rows]
    conn.close()
    return templates.TemplateResponse('qa_list.html', {'request': request, 'faqs': faqs})