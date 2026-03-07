from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()



app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


posts: list[dict] = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the content of the first post."
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is the content of the second post"
    }
]

@app.get("/", response_class=HTMLResponse, name="home")
@app.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "posts": posts,
            "title": "Home"
        }
    )



@app.get("/posts/{post_id}",  include_in_schema=False)
def get_posts(request: Request, post_id : int):
    for post in posts:
        if post.get("id")==post_id:
            return templates.TemplateResponse(
                "post.html",
                {
                    "request": request,
                    "post": post,
                    "title": post.get("title")
                }
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")