#!/usr/bin/python3

#
# Copyright (C) 2022 lifehackerhansol
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from base64 import b64decode
from io import BytesIO

import requests
from fastapi import FastAPI, HTTPException, Form, Response
from fastapi.responses import StreamingResponse
# needed to work around some weird shit going on in FastAPI.Form()
from pydantic.fields import Undefined
from PIL import Image


app = FastAPI()


gametdbregions = {
    'D': "DE",
    'E': "US",
    'F': "FR",
    'H': "NL",
    'I': "IT",
    'J': "JA",
    'K': "KO",
    'R': "RU",
    'S': "ES",
    'T': "US",
    'U': "AU",
    '#': "HB"
}


@app.post("/api")
async def get_boxart(Filename: str = Form(default=Undefined),
                     Sha1: str = Form(default=Undefined),
                     Header: str = Form(default=Undefined),
                     BoxartWidth: str = Form(default=Undefined),
                     BoxartHeight: str = Form(default=Undefined),
                     KeepAspectRatio: str = Form(default=Undefined),
                     BoxartBorderStyle: str = Form(default=Undefined),
                     BoxartBorderColor: str = Form(default=Undefined),
                     BoxartBorderThickness: str = Form(default=Undefined)):
    print(Filename)
    extension = Filename[-3:].lower()
    header = b64decode(Header)
    gamecode: str = None
    if extension in ["dsi", "nds"]:
        gamecode = header[0xC:0x10].decode('ascii')
    elif extension == "gba":
        gamecode = header[0xAC:0xB0].decode('ascii')
    artwork = None
    if extension in ["dsi", "nds"]:
        region = gametdbregions[gamecode[3]] if gamecode[3] in gametdbregions else "EN"
        artwork = requests.get(f'https://art.gametdb.com/ds/coverDS/{region}/{gamecode}.bmp')
        if artwork.status_code != 200:
            artwork = requests.get(f'https://art.gametdb.com/ds/coverDS/EN/{gamecode}.bmp')
    if artwork.status_code != 200:
        raise HTTPException(status_code=404)
    response = BytesIO(artwork.content)
    if extension in ["dsi", "nds"]:
        if not KeepAspectRatio or BoxartWidth != "115" or BoxartHeight != "128":
            img = Image.open(response)
            img.resize((int(BoxartWidth), int(BoxartHeight)))
            img.save(response, format='PNG')
        response.seek(0)
        return StreamingResponse(content=response, media_type="image/png")
    raise HTTPException(status_code=404)
