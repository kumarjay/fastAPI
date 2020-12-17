from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
# from config import PORT
import uvicorn
from pathlib import Path

from pydantic import BaseModel

app = FastAPI()

db = []
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')


# app.mount(
#     "/static",
#     StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
#     name="static",
# )


class City(BaseModel):
    name: str
    timezone: str  # list, datetime, dict


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@app.get('/xyz', response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('abc.html', {'request': request})


@app.get('/cities')
def get_cities():
    return db


@app.get('/cities/{city_id}')
def get_city(city_id: int):
    return db[city_id - 1]


#
@app.post('/cities')
def create_city(city: City):
    db.append(city.dict())
    return db[-1]


#
@app.delete('/cities/{city_id}')
def delete_city(city_id: int):
    db.pop(city_id - 1)
    return {}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
