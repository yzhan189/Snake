# this class stores information of a player
class Player:
    def __init__(self,name):
        self.name = name
        self.score = 0
        self.avatarFilePath = "./images/"+name+".png"