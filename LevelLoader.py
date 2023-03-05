
class Level:
    def __init__(self, filepath):
        self.loadFile(filepath)

    def loadFile(self, filepath):

        self.mapping = []
        f = open(filepath, "r")
        parseSector = ""

        self.movingPlatformsPosition = []
        self.movingPlatformData = []
        self.laserVGunPositions = []
        self.laserVGunTimers = []
        self.laserVGunDirection = 'none'

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
            elif line == "[laser_vguns]":
                parseSector = "laser_vguns"

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

            elif parseSector == "next_map":
                self.nextLevel = line

            elif parseSector == "moving_platforms":
                dataTokens = line.split(",")
                self.movingPlatformData.append([int(dataTokens[0]), int(dataTokens[1]), dataTokens[2]])
            elif parseSector == "laser_vguns":
                dataTokens = line.split(",")
                self.laserVGunPositions.append([int(dataTokens[0]), int(dataTokens[1])])
                self.laserVGunTimers.append([int(dataTokens[2]), int(dataTokens[3])])
                self.laserVGunDirection = dataTokens[4]