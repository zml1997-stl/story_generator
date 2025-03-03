from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import os
from utils.ai_handler import generate_story

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/start_story/")
async def start_story(request: Request, genre: str = Form(...), name: str = Form(...)):
    story_intro = await generate_story(genre, name)
    return templates.TemplateResponse("index.html", {"request": request, "story": story_intro, "name": name})
