from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
from pathlib import Path

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')
DB_PATH = Path(__file__).resolve().parents[1] / 'rice_store.db'

# NOTE: Very simple admin auth for local use. Username/password are in README. Not secure for production.
def is_admin(request: Request):
    return request.cookies.get('admin') == '1'

@router.get('/admin/login', response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse('admin_login.html', {'request': request})

@router.post('/admin/login')
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # default credentials: admin / password123  (change in production!)
    if username == 'admin' and password == 'password123':
        response = RedirectResponse(url='/admin/dashboard', status_code=302)
        response.set_cookie(key='admin', value='1', httponly=True)
        return response
    return templates.TemplateResponse('admin_login.html', {'request': request, 'error': 'نام کاربری یا رمز عبور اشتباه است'})

@router.get('/admin/logout')
def logout():
    response = RedirectResponse(url='/', status_code=302)
    response.delete_cookie('admin')
    return response

@router.get('/admin/dashboard', response_class=HTMLResponse)
def dashboard(request: Request):
    if not is_admin(request):
        return RedirectResponse(url='/admin/login')
    # basic stats
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM customers')
    customers = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM festivals')
    festivals = cur.fetchone()[0]
    cur.execute('SELECT COUNT(*) FROM faqs')
    faqs = cur.fetchone()[0]
    conn.close()
    return templates.TemplateResponse('admin_dashboard.html', {'request': request, 'customers': customers, 'festivals': festivals, 'faqs': faqs})

@router.get('/admin/customers', response_class=HTMLResponse)
def admin_customers(request: Request):
    if not is_admin(request):
        return RedirectResponse(url='/admin/login')
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, name, phone, city FROM customers ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return templates.TemplateResponse('admin_customers.html', {'request': request, 'customers': rows})

@router.get('/admin/festivals', response_class=HTMLResponse)
def admin_festivals(request: Request):
    if not is_admin(request):
        return RedirectResponse(url='/admin/login')
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, title, date FROM festivals ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return templates.TemplateResponse('admin_festivals.html', {'request': request, 'festivals': rows})

@router.get('/admin/faqs', response_class=HTMLResponse)
def admin_faqs(request: Request):
    if not is_admin(request):
        return RedirectResponse(url='/admin/login')
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('SELECT id, question, answer FROM faqs ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return templates.TemplateResponse('admin_faqs.html', {'request': request, 'faqs': rows})

@router.post('/admin/add-festival')
def admin_add_festival(request: Request, title: str = Form(...), description: str = Form(...), image_url: str = Form(''), date: str = Form(...)):
    if not is_admin(request):
        return RedirectResponse(url='/admin/login')
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO festivals (title, description, image_url, date) VALUES (?, ?, ?, ?)', (title, description, image_url, date))
    conn.commit()
    conn.close()
    return RedirectResponse(url='/admin/festivals', status_code=302)

@router.post('/admin/add-faq')
def admin_add_faq(request: Request, question: str = Form(...), answer: str = Form(...), keywords: str = Form('')):
    if not is_admin(request):
        return RedirectResponse(url='/admin/login')
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('INSERT INTO faqs (question, answer, keywords) VALUES (?, ?, ?)', (question, answer, keywords))
    conn.commit()
    conn.close()
    return RedirectResponse(url='/admin/faqs', status_code=302)