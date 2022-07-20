import random
import re
import sys
import time
import asyncio

from unicodedata import name
import requests
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import json
from json import JSONEncoder
from helpers import getCharDesc, getTwitter
from dbfz import getDBFZChar
from ggst import getGGSTChar
from bb import getBBChar
app = Flask(__name__)

# @app.get("/my-first-api")
# def hello():
#     return {"Hello world!"}


def delay() -> None:
    time.sleep(3)
    return None


@app.route('/')
def main():
    delay()
    # new url?
    # URL = "https://www.dustloop.com/w/Main_Page"
    URL = "https://www.dustloop.com/wiki/index.php?title=Main_Page"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    return index(soup)


@app.route("/<game>")
async def getCharacters(game):
    print(game)
    URL = "https://www.dustloop.com/wiki/index.php?title={}".format(game)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    characters = []
    result = soup.body.find(id="fpbottomsection").find_all("dl")
    for col in result:
        row = col.find_all('b')
        for character in row:
            fullPath = character.find_parent()
            path = fullPath['href'].split("w/")
            characters.append({"name": character.text, "path": path[1]})
    return json.dumps(characters)


@app.route("/<gameTag>/<characterTag>")
async def getCharData(gameTag, characterTag):
    if gameTag == "DBFZ":
        data = await getBBChar(gameTag, characterTag)
    elif gameTag == "GGST":
        data = await getGGSTChar(gameTag, characterTag)
        # data = await getBBChar(gameTag, characterTag)
    elif gameTag == "BBCF" or gameTag == "BBTag":
        data = await getBBChar(gameTag, characterTag)
    else:
        data = await getBBChar(gameTag, characterTag)
    return data


if __name__ == '__main__':
    app.run(debug=True, port=8000)
