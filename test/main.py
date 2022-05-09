import json
from turtle import title
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import random
import string
from typing import Optional
from pydantic import BaseModel
class Item(BaseModel):
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


def random_string(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def sync_pastes_file(self):
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
    return {"Data" : pastes}
@app.get("/api/pastes/")
def pastez(paste_id : Optional[str] = None):
    if paste_id == None:
        return {"Data" : pastes}
    else:
        return {"Paste": pastes[paste_id]}

@app.post("/api/pastepost")
def pastepost(paste: Item):
    #Get post data
    post_data = []
    post_data.append(dict(paste))
    return {"Data": post_data}

