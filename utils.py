import random
import string
import pydenticon
import hashlib
from Player import *
import json
import os
from database import firebaseApp


AVATAR_SIZE = 40
AVATAR_BLOCK_NUM = 5

SCORE_PATH = "./data/score.json"
IMAGE_DIR = "./images/"

# block color
foreground = [ "rgb(128,0,0)",
               "rgb(255,127,80)",
               "rgb(250,128,114)",
               "rgb(0,128,128)",
               "rgb(64,224,208)",
               "rgb(123,104,238)",
               "rgb(70,130,180)",
               "rgb(123,104,238)",
               "rgb(255,250,205)" ]
# background colour
background = "rgb(224,224,224)"

# generator creating 5x5 block avatar
generator = pydenticon.Generator(AVATAR_BLOCK_NUM, AVATAR_BLOCK_NUM, digest=hashlib.sha1,
                                 foreground=foreground, background=background)
# generate avatar
def generateAvatar(name):
    # set up padding size
    pad = int (AVATAR_SIZE/10)
    padding = (pad, pad, pad, pad)

    # create a printable version in terminal
    icon_ascii = generator.generate(name, AVATAR_SIZE, AVATAR_SIZE,
                                   padding=padding, output_format="ascii")

    icon_png = generator.generate(name, AVATAR_SIZE, AVATAR_SIZE,
                                   padding=padding, output_format="png")

    # write image to file
    filePath = "./images/temp.png"
    f = open(filePath, "wb")
    f.write(icon_png)
    f.close()
    return filePath


# randomly generate name consisting of uppercase and lowercase letters
# and numbers of length 7
def generateName ():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))


# add new player info: avatar rename and add score data
def addPlayerData(name):

    # now player game is decided, store temp avatar file.
    if "temp.png" in os.listdir(IMAGE_DIR):
        os.rename(IMAGE_DIR+"temp.png",IMAGE_DIR+name+".png")

    newPlayer = Player(name)

    # store player score
    with open(SCORE_PATH, 'r') as f:
        score_data = json.load(f)

    # add a new entry of player information
    score_data[newPlayer.name] = newPlayer.__dict__

    with open(SCORE_PATH, 'w') as f:
        json.dump(score_data, f, indent=4)


# update score
def updatePlayerData(name,score):
    # store player score
    with open(SCORE_PATH, 'r') as f:
        score_data = json.load(f)

    score_data[name]["score"] = score

    with open(SCORE_PATH, 'w') as f:
        json.dump(score_data, f, indent=4)


# update remote data, and clear local data
def setData():
    with open(SCORE_PATH, 'r') as f:
        score_data = json.load(f)

    # store data on firebase
    firebaseApp.post('',score_data)

    # delete all local avatar image
    for file in os.listdir(IMAGE_DIR):
        os.remove(IMAGE_DIR+file)

    # empty local json file
    with open(SCORE_PATH, 'w') as f:
        f.write("{}")

