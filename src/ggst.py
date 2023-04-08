import requests
from bs4 import BeautifulSoup
from helpers import getCharDesc, getTwitter, getCharPortrait

core_data_headers = ["Name",
                     "Defense",
                     "Guts",
                     "Prejump",
                     "Weight",
                     "Backdash",
                     "Forward Dash",
                     "Unique movement options",
                     "R.I.S.C. Multiplier",
                     "Movement Tension Gain",
                     ]

jump_data_headers = ["Jump duration",
                     "Jump height",
                     "High Jump duration",
                     "High Jump height",
                     "Earliest airdash",
                     "Earliest air backdash",
                     "Airdash duration",
                     "Air backdash duration",
                     "Airdash cancel",
                     "Air backdash cancel",
                     "Jumping Tension Gain",
                     "Airdash Tension Gain"]


async def getGGSTChar(gameTag, characterTag):

    URL = 'https://dustloop.com/w/{}/{}/Frame_Data'.format(
        gameTag, characterTag)
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
                          "game": gameTag, "thumbnail": img, "twitterTag": twitterTag,  "wikiPath": characterTag, "url": 'https://dustloop.com/wiki/index.php?title={}/{}'.format(
                              gameTag, characterTag)}}
    move_collection = []
    system_data_collection = []
# system data
    system_data = result.find_all("table", class_="cargoTable")

    for table in system_data:
        header = table.find_previous("dl").dt
        colData = []
        rows = table.find("tr")
        cellHeaders = rows.find_all("th")
        cellRows = table.find("tbody").find_all("tr")
        for row in cellRows:
            col = {}
            cellData = row.find_all('td')
            for i in range(0, len(cellData)):
                if cellHeaders[i].text != "":
                    if header.text == "Core Data":
                        col.update({core_data_headers[i]: cellData[i].text})
                    elif header.text == "Jump Data":
                        col.update({jump_data_headers[i]: cellData[i].text})
                    else:
                        col.update({cellHeaders[i].text: cellData[i].text})
            colData.append(col)
            colRow = {"title": header.text, "data": colData}
        system_data_collection.append(colRow)
    data.update({"systemData": system_data_collection})

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
            all_imgs = tr_parse_details.find_all("img")
            hitboxes = []
            for i in all_imgs:
                if "Hitbox" in i['src']:
                    raw = i['src'].split('/thumb')
                    if len(raw) == 1:
                        hitbox = "https://www.dustloop.com" + raw[0]
                    else:
                        path = raw[1].split(".png")
                        hitbox = "https://www.dustloop.com/wiki/images" + \
                            path[0] + ".png"
                    hitboxes.append(hitbox)
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
                    header_text = cellHeaders[i].text.replace("-", "").lower()
                    if "level" in header_text:
                        header_text = "level"
                    if "counter" in header_text:
                        header_text = "counter"
                    if "prorate" in header_text:
                        header_text = "proration"
                    move.update(
                        {header_text: cellData[i].text, "image": img, "hitboxes": hitboxes})
            moves.append(move)
        if header.text == "Supers":
            move_section = {"moveType": "Overdrives", "moveList": moves}
        else:
            move_section = {"moveType": header.text, "moveList": moves}
        move_collection.append(move_section)
    data.update({"moveCollection": move_collection})
    return data
