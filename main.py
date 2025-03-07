from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount the static folder to serve CSS, JS, etc.
app.mount("/static", StaticFiles(directory=r"static"), name="static")

# Set up the templates folder
templates = Jinja2Templates(directory="templates")

# Route to render the index.html
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
