from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import customers, festivals, admin, qa, api_qa

app = FastAPI(title="فروشگاه برنج طبرستان حاج محمد یوسفی - فول")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(customers.router)
app.include_router(festivals.router)
app.include_router(qa.router)
app.include_router(admin.router)
app.include_router(api_qa.router)