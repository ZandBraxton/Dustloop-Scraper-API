import json
from bs4 import BeautifulSoup
import requests
import re


def getCharDesc(gameTag, characterTag):
    # new url?
    # URL = 'https://dustloop.com/w/{}/{}'.format(
    #     gameTag, characterTag)

    URL = 'https://dustloop.com/wiki/index.php?title={}/{}'.format(
        gameTag, characterTag)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.body.find(id="mf-home")
    rawTextCheck = result.select("#fptopsection > div > div:nth-child(2)")
    desc = []
    for i in rawTextCheck[0]:
        if i.name is None or i.name == "span" or i.name == "p" or i.name == "b":
            desc.append(i.text.strip("\n"))
    extractedDesc = "".join(desc)
    print(extractedDesc)
    if extractedDesc == "":
        info = result.select(
            "#fptopsection > div > div:nth-child(2) > table > tbody > tr:nth-child(1) > td")
        extractedDesc = info[0].text.strip()

    if extractedDesc is not None or extractedDesc == "":
        return extractedDesc
    else:
        return "None"


def getCharPortrait(gameTag, characterTag):
    # new url?
    # URL = 'https://dustloop.com/w/{}/{}'.format(
    #     gameTag, characterTag)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    result = soup.body.find(id="fpflexsection")
    find_image = result.find("img")
    if find_image is not None:
        raw = find_image['src'].split('/thumb')
        if len(raw) == 1:
            img = "https://www.dustloop.com" + raw[0]
        else:
            path = raw[1].split(".png")
            img = "https://www.dustloop.com/w/images" + \
                path[0] + ".png"
    else:
        img = ""
    return img


def getTwitter(gameTag, characterTag):
    # new url?
    # URL = 'https://dustloop.com/w/{}/{}/Resources'.format(
    #     gameTag, characterTag)
    URL = 'https://dustloop.com/wiki/index.php?title={}/{}/Resources'.format(
        gameTag, characterTag)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    twitter = soup.find_all(string=re.compile("^#"))
    if twitter is not None:
        return twitter
    else:
        return "None"


def getImage(url):
    URL = url
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    try:
        img_path = soup.find(class_="fullImageLink").find("a")
    except:
        print("uh oh")
    if img_path is not None:
        img = "https://www.dustloop.com" + img_path['href']
    else:
        img = ""
    return img
