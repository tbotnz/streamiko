from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import config

from backend.netmiko import get_command

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("template.html", {"request": request})


@app.websocket("/ws")
async def ws_handler(websocket: WebSocket):
    await websocket.accept()

    content = """
<div hx-swap-oob="beforeend:#content" class="accordion" id="accordionExample">
  <div class="accordion-item">
    <h2 class="accordion-header" id="headingOne">
      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
        {comm}
      </button>
    </h2>
    <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#accordionExample">
      <div class="accordion-body">
        <strong>{result}</strong>
      </div>
    </div>
  </div>
</div>
    """

    while True:
        msg = await websocket.receive_json()
        command_result = get_command(driver="cisco_ios", hostname=msg["host"], command=msg["command"])
        await websocket.send_text(
            content.format(comm=msg["command"], result=command_result)
        )
