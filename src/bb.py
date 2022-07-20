from gettext import find
import requests
from bs4 import BeautifulSoup
from helpers import getCharDesc, getImage, getTwitter, getCharPortrait


async def getBBChar(gameTag, characterTag):

    URL = 'https://dustloop.com/wiki/index.php?title={}/{}/Frame_Data'.format(
        gameTag, characterTag)
    # desc = getCharDesc(gameTag, characterTag)
    desc = "N/A"
    twitterTag = getTwitter(gameTag, characterTag)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    result = soup.body.find(class_="mw-parser-output")
    char_label = result.find(class_="charaLabel")
    char_name = result.find("b")
    if char_name.text == "Disclaimer":
        char_name = char_name.findNext("b")

    find_image = char_label.a.img
    # find_image = result.find("img")
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

    # if find_image is not None:
    #     img = "https://www.dustloop.com" + \
    #         find_image['src'].strip("&amp;")
    # else:
    #     img = ""

    data = {"character": {"name": char_name.text, "description": desc,
                          "game": gameTag, "thumbnail": img, "twitterTag": twitterTag, "wikiPath": characterTag, "url": 'https://dustloop.com/wiki/index.php?title={}/{}'.format(
                              gameTag, characterTag)}}
    move_collection = []
    system_data_collection = []
# system data
    system_data = result.find_all("table", class_="cargoTable")

    for table in system_data:
        colData = []
        rows = table.find("tr")
        cellHeaders = rows.find_all("th")
        cellRows = table.find("tbody").find_all("tr")
        for row in cellRows:
            col = {}
            cellData = row.find_all('td')
            for i in range(0, len(cellData)):
                if cellHeaders[i].text != "":
                    col.update(
                        {cellHeaders[i].text.capitalize(): cellData[i].text})
            colData.append(col)
            colRow = {"title": "System Data", "data": colData}
        system_data_collection.append(colRow)
    data.update({"systemData": system_data_collection})

    all_tables = result.find_all("table", class_="display")
    for table in all_tables:
        for sib in table.previous_siblings:
            if sib.name == "h3":
                header = sib
                break
            elif sib.name == "h2":
                header = sib
                break
        rows = table.find("tr")
        cellHeaders = rows.find_all("th")
        cellRows = table.find("tbody").find_all("tr")
        moves = []
        for row in cellRows:
            tr_parse_details = BeautifulSoup(
                row['data-details'], "html.parser")
            find_image = tr_parse_details.find("img")
            # find_url = tr_parse_details.find("a")
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
                # takes too long
            # if find_url is not None:
            #     img = getImage("https://www.dustloop.com" +
            #                    find_url['href'])
            # if find_image is not None:
            #     img = "https://www.dustloop.com" + \
            #           find_image['src'].strip("&amp;")
            # else:
            #     img = ""
            move = {}
            cellData = row.find_all("td")
            for i in range(0, len(cellData)):
                if cellHeaders[i].text != "":
                    header_text = cellHeaders[i].text.replace("-", "").lower()
                    move_text = cellData[i].text
                    if header_text == "attribute":
                        if move_text == "H":
                            move_text = "Head"
                        elif move_text == "B":
                            move_text = "Body"
                        elif move_text == "F":
                            move_text = "Foot"
                        elif move_text == "T":
                            move_text = "Throw"
                        elif move_text == "D":
                            move_text = "Doll"
                        elif "P" in move_text:
                            if len(move_text) == 2:
                                move_text = "Projectile: Lvl " + move_text[1]
                            else:
                                move_text = "Projectile"

                    move.update(
                        {header_text: move_text, "image": img})
            moves.append(move)
            move_section = {"moveType": header.text, "moveList": moves}
        move_collection.append(move_section)
    data.update({"moveCollection": move_collection})
    return data


def find_headers(tag):
    return
