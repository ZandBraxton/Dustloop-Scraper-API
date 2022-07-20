

import requests
from bs4 import BeautifulSoup
from helpers import getCharDesc, getTwitter, getCharPortrait


async def getDBFZChar(gameTag, characterTag):
    print(gameTag)
    print(characterTag)
    URL = 'https://dustloop.com/wiki/index.php?title={}/{}/Frame_Data'.format(
        gameTag, characterTag)
    print(URL)
    # desc = getCharDesc(gameTag, characterTag)
    desc = "N/A"
    twitterTag = getTwitter(gameTag, characterTag)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    result = soup.body.find(class_="mw-parser-output")
    char_name = result.find("b")
    find_image = result.find("img")
    if find_image is not None:
        raw = find_image['src'].split('/thumb')
        if len(raw) == 1:
            img = "https://www.dustloop.com" + raw[0]
        else:
            path = raw[1].split(".png")
            img = "https://www.dustloop.com/wiki/images" + \
                path[0] + ".png"
    else:
        img = ""

    data = {"character": {"name": char_name.text, "description": desc,
                          "game": gameTag, "thumbnail": img,  "twitterTag": twitterTag, "wikiPath": characterTag, "url": 'https://dustloop.com/wiki/index.php?title={}/{}'.format(
                              gameTag, characterTag)}}
    move_collection = []

    all_tables = result.find_all("table", class_="display")
    for table in all_tables:

        header = table.find_previous("h2")
        rows = table.find("tr")
        cellHeaders = rows.find_all("th")
        cellRows = table.find("tbody").find_all("tr")
        moves = []
        for row in cellRows:
            tr_parse_details = BeautifulSoup(
                row['data-details'], "html.parser")
            find_image = tr_parse_details.find("img")
            if find_image is not None:
                raw = find_image['src'].split('/thumb')
                if len(raw) == 1:
                    img = "https://www.dustloop.com" + raw[0]
                else:
                    path = raw[1].split(".png")
                    img = "https://www.dustloop.com/wiki/images" + \
                        path[0] + ".png"
            else:
                img = ""
            move = {}
            cellData = row.find_all("td")
            for i in range(0, len(cellData)):
                if cellHeaders[i].text != "":
                    move.update(
                        {cellHeaders[i].text.lower(): cellData[i].text, "image": img})
            moves.append(move)
        move_section = {"moveType": header.text, "moveList": moves}
        move_collection.append(move_section)
    data.update({"moveCollection": move_collection})
    return data
