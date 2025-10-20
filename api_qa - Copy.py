from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from pathlib import Path

router = APIRouter(prefix='/api')

class QARequest(BaseModel):
    question: str

DB_PATH = Path(__file__).resolve().parents[1] / 'rice_store.db'

@router.post('/qa')
def answer_question(req: QARequest):
    q = req.question.lower()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT question, answer, keywords FROM faqs')
    rows = cur.fetchall()
    # simple keyword matching: split keywords by comma and check any keyword in question
    for question, answer, keywords in rows:
        if keywords:
            for kw in keywords.split(','):
                kw = kw.strip().lower()
                if kw and kw in q:
                    conn.close()
                    return {'answer': answer, 'source': question}
    # fallback: return first FAQ if exists
    if rows:
        conn.close()
        return {'answer': rows[0][1], 'source': rows[0][0]}
    conn.close()
    raise HTTPException(status_code=404, detail='پاسخی یافت نشد.')