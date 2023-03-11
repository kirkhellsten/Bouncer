
class Level:
    def __init__(self, filepath):
        self.loadLevel(filepath)

    def loadLevel(self, levelFileName):
        self.loadFile("levels/" + levelFileName)

    def loadFile(self, filepath):

        self.mapping = []
        f = open(filepath, "r")
        parseSector = ""

        self.movingPlatformsPosition = []
        self.movingPlatformData = []
        self.laserGunPositions = []
        self.laserGunTimers = []
        self.laserGunDirection = 'none'
        self.laserGunData = []
        self.lastlevel = False

        for line in f:

            line = line.replace("\n", "")
            if line == "":
                continue

            if line == "[tiles]":
                parseSector = "tiles"
            elif line == "[bouncer_position]":
                parseSector = "bouncer_position"
            elif line == "[exitdoor_position]":
                parseSector = "exitdoor_position"
            elif line == "[next_map]":
                parseSector = "next_map"
            elif line == "[moving_platforms]":
                parseSector = "moving_platforms"
            elif line == "[laser_guns]":
                parseSector = "laser_guns"
            elif line == "[main_music]":
                parseSector = "main_music"
            elif line == "[lastlevel]":
                parseSector = "lastlevel"

            if line.find("[") != -1 and line.find("]") != -1:
                continue

            if parseSector == "tiles":
                dataTokens = line.split(",")
                datastream = []
                for data in dataTokens:
                    datastream.append(int(data))
                self.mapping.append(datastream)

            elif parseSector == "bouncer_position":
                dataTokens = line.split(",")
                self.bouncerPosition = (int(dataTokens[0]), int(dataTokens[1]))

            elif parseSector == "exitdoor_position":
                dataTokens = line.split(",")
                self.exitdoorPosition = (int(dataTokens[0]), int(dataTokens[1]))
            elif parseSector == "lastlevel":
                self.lastlevel = bool(line)
            elif parseSector == "next_map":
                self.nextLevel = line

            elif parseSector == "moving_platforms":
                dataTokens = line.split(",")
                self.movingPlatformData.append([int(dataTokens[0]), int(dataTokens[1]), dataTokens[2]])
            elif parseSector == "laser_guns":
                dataTokens = line.split(",")
                self.laserGunPositions.append([int(dataTokens[0]), int(dataTokens[1])])
                self.laserGunTimers.append([int(dataTokens[2]), int(dataTokens[3])])
                self.laserGunDirection = dataTokens[4]
                self.laserGunData.append([int(dataTokens[0]), int(dataTokens[1]), int(dataTokens[2]), int(dataTokens[3]), dataTokens[4]])
            elif parseSector == "main_music":
                dataTokens = [int(line)]
                self.main_music = dataTokens[0]