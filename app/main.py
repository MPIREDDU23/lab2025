from fastapi import FastAPI
from routers import books

app = FastAPI()
app.include_router(books.router, tags=["books"])
if __name__   == 'main':
    import uvicorn
    uvicorn.app
