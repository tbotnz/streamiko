from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from config import config

from backend.netmiko import get_command

import uuid

import re

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("template.html", {"request": request})


@app.websocket("/ws")
async def ws_handler(websocket: WebSocket):
    await websocket.accept()

    
    content = """
<div hx-swap-oob="beforeend:#content" class="accordion bg-dark" id="accordionExample">
  <div class="accordion-item">
    <h2 class="accordion-header" id="headingOne">
      <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#{div_id}" data-bs-theme="dark" aria-expanded="true" aria-controls="{div_id}">
        {comm}
      </button>
    </h2>
    <div id="{div_id}" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-theme="dark" data-bs-parent="#accordionExample">
      <div class="accordion-body">
        <strong>{result}</strong>
      </div>
    </div>
  </div>
</div>
    """

    while True:
        dv_id = f"{uuid.uuid1()}".replace("-","")
        dv_id_clean = re.sub('\d', '', dv_id)
        msg = await websocket.receive_json()
        command_result = get_command(driver="cisco_ios", hostname=msg["host"], command=msg["command"])
        await websocket.send_text(
            content.format(comm=msg["command"], result=command_result, div_id=dv_id_clean)
        )
