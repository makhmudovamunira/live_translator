from fastapi import FastAPI
from another_fastapi_jwt_auth import AuthJWT
from schemas import Settings
from database import Base, engine
from auth_routes import auth_router
from translate_routes import translate_router

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware


templates = Jinja2Templates(directory="templates")



Base.metadata.create_all(bind=engine)

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(translate_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"

    )