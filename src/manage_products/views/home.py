import fastapi

router = fastapi.APIRouter()


@router.get("/")
def index():
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the Manage Products API </h1>"
        "<div>"
        "Check out the <a href='/docs'>API Docs</a>"
        "</div>"
        "</body>"
        "</html>"
    )
    return fastapi.responses.HTMLResponse(content=body)
