from importlib.resources import path
import json
import os
from turtle import title
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import random
import string
from typing import Optional
from parso import parse
from pydantic import BaseModel
from pytest import console_main


class Item(BaseModel):
    id: str
    paste: str
    password: Optional[str] = None
    use_password: bool
    title: str
    code: str
    burn_after_read: bool


pastes_fd = open("pastes.json", "r")
# Reads the pastes json file and loads it into a dict
pastes = json.load(pastes_fd)
pastes_fd.close()


# def random_string(length: int = 10) -> str:
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def sync_pastes_file():
    with open("pastes.json", "w") as pastes_fd:
        json.dump(pastes, pastes_fd, indent=2)


app = FastAPI()

origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def home():
    print(pastes)
    return {"Data": pastes}

@app.get ("/api/pastes")
def pasteroonie():
    return {"Data": pastes}
@app.get("/api/pastes/{paste_id}")
def pastez(paste_id):
        return pastes[paste_id]

@app.get("/api/paste/{path}/{paste}")
def getPaste(path: str, paste: str):
    Dir = f"{path}/{paste}.txt"
    print(Dir)
    with open(Dir) as fp:
        content = fp.read()
    return content


@app.get("/api/pastes/delete/{pasteId}")
def delete(pasteId: str):
    paste_path = f"./pastes/{pasteId}.txt"
    os.remove(paste_path)
    del pastes[pasteId]
    sync_pastes_file()


@app.post("/api/pastepost")
def pastepost(paste: Item):
    # Get post data
    post_data = []
    post_data.append(dict(paste))
    parsed_body = post_data[0]
    paste_content = parsed_body['paste']
    paste_id = parsed_body['id']
    paste_path = f"./pastes/{paste_id}.txt"

    with open(paste_path, "w") as fd:
        fd.write(paste_content)

    pastes.update({
            paste_id: {
                "title": parsed_body['title'],
                "path": paste_path,
                "password": parsed_body['password'],
                "use_password": parsed_body['use_password'],
                "code": parsed_body['code'],
                "burn_after_read": parsed_body['burn_after_read'],
            }
        })
    sync_pastes_file()

    # print(post_data)
    return {"Data": pastes}
