import pygame
import csv
import pandas as pd
import configparser  # https://stackoverflow.com/questions/8884188/how-to-read-and-write-ini-file-with-python3

debug = False


def pygameInit():
    pygame.init()
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    global groundColor
    groundColor = (62, 79, 38)
    global backgroundColor
    backgroundColor = (96, 96, 96)

    # defines gameDisplay, including size and background color
    global gameDisplay
    gameDisplay = pygame.display.set_mode(((boardWidth + 6) * tileSize, boardHeight * tileSize))
    gameDisplay.fill((backgroundColor))
    pygame.display.set_caption('Untitled RPG Project')


# PYGAME: how to draw rectangles
# pygame.draw.rect(gameDisplay, groundColor, (0, 0, 50, 50))


class Cell():
    # Uses a default name parameter of ""
    def __init__(self, id, terrain, name="wilderness"):
        self.id = id
        self.name = name
        print("Instantiating cell... id: " + str(id) + ", name: " + name)
        self.terrain = terrain
        cells.append(self)
        self.entities = []

    def addEntity(self, entity, entityCoords):
        self.entities.append([entity, [entityCoords[0], entityCoords[1]]])

    def getTileContents(self, x, y):
        print("Getting tile contents for " + str(x) + ", " + str(y))

        # FIXME
        return "stuff"

def coordsInBounds(x, y):
    if (x >= 0 and x < boardWidth * tileSize) and (y >= 0 and y < boardHeight * tileSize):
        return True

class Tree():
    def __init__(self, image):
        self.image = image


class Entity():
    def __init__(self, image, impassable, description=''):
        self.image = image
        self.impassable = True
        self.description = description


# cell0.entities.append(Tree(pygame.image.load('tree1.png')), (5, 5))


# player position is stored as grid coordinates
class Player():
    def __init__(self, startingCellId, pcOriginX, pcOriginY):
        self.cell = startingCellId
        self.posX = pcOriginX
        self.posY = pcOriginY
        self.facing = "RIGHT"
        print("Instantiating player character in cell " + str(self.cell) + " at " + str(pcOriginX) + ", " + str(
            pcOriginY))
        self.nextFootRight = True

    def move(self, direction):
        print("Moving player " + str(direction))

        # check if the player is on the edge of the cell
        # FIXME: building this assuming all cells are 16*16. Will need to alter this for different sized cells.

        if (direction == "UP"):
            self.posY -= tileSize
        elif (direction == "DOWN"):
            self.posY += tileSize
        elif (direction == "LEFT"):
            if self.posX <= 0.0:
                loadCell(getCell(player.cell.id - 1))
                self.posX = 750.0
            else:
                self.posX -= tileSize
                self.facing = "LEFT"
        elif (direction == "RIGHT"):
            if self.posX >= 750.0:
                loadCell(getCell(player.cell.id + 1))
                self.posX = 0.0
            else:
                self.posX += tileSize
                self.facing = "RIGHT"
        playWalkSound()
        print("Player new position: " + str(self.posX) + ", " + str(self.posY))


# returns a Cell with the provided ID
def getCell(id):
    for cell in cells:
        if cell.id == id:
            return cell


def loadCell(cell):
    # df = pd.read_csv('map1.csv', header=None)  # Had to add header=None, it was auto-generating headers
    print("Loading cell " + str(cell))
    player.cell = cell
    initialRender()


def renderTerrain():
    # render map
    cell = player.cell
    print("Rendering cell " + str(cell) + "... ")
    # print("Using terrain map " + str(cell.terrain))

    df = pd.read_csv(player.cell.terrain, header=None)  # Had to add header=None, it was auto-generating headers
    for i in range(0, boardWidth * boardHeight):
        x = i % boardWidth
        y = i // boardHeight
        terrainType = df.iloc[x, y]
        if debug:
            print("square " + str(i) + " coords: " + str(x) + ", " + str(y) + " value: " + str(terrainType))

        if terrainType == 0:
            terrainImg = pygame.image.load('water2.png')
        elif terrainType == 1:
            terrainImg = pygame.image.load('water1.png')
        elif terrainType == 2:
            terrainImg = pygame.image.load('dirt1.png')
        elif terrainType == 3:
            terrainImg = pygame.image.load('grass1.png')
        else:
            terrainImg = pygame.image.load('defaultTexture.png')

        gameDisplay.blit(terrainImg, (y * tileSize, x * tileSize))
        # playerImg = pygame.transform.scale(pygame.image.load('playerCharacter.png'), (tileSize, tileSize))
        # gameDisplay.blit(playerImg, (player.posX, player.posY))
        # testImg = pygame.transform.scale(pygame.image.load('playerCharacter.png'), (tileSize, tileSize))


def renderEntities():
    # cell = player.cell
    print("Rendering entities in cell " + str(player.cell.id))
    print(str(player.cell.entities))
    # render things on the map

    df = pd.read_csv('Entities.csv')  # Had to add header=None, it was auto-generating headers
    print(df.iloc[0])
    print(df.iloc[0].image)
    print("number of entities in this cell: " + str(len(player.cell.entities)))
    for x in player.cell.entities:
        if debug:
            print(x)
            print(x[0])
            print(x[1])
            print(x[1][0])
            print(x[1][1])

        entityImg = pygame.image.load(df.iloc[int(x[0])].image)
        gameDisplay.blit(entityImg, (x[1][0] * tileSize, x[1][1] * tileSize))


def renderActors():
    # render player characters and NPCs
    if player.facing == "RIGHT":
        playerImg = pygame.transform.scale(pygame.image.load('playerCharacter.png'), (tileSize, tileSize))
    elif player.facing == "LEFT":
        playerImg = pygame.transform.scale(pygame.image.load('playerCharacter-left.png'), (tileSize, tileSize))
    gameDisplay.blit(playerImg, (player.posX, player.posY))


def renderLabels():
    if debug:
        print("Rendering labels...")
    global backgroundColor

    labelLeftPadding = 5

    # redraw the background to prevent overlapping text
    pygame.draw.rect(gameDisplay, backgroundColor, ((boardWidth * tileSize), 0, (6 * tileSize), (boardHeight * tileSize)))

    # FIXME: add ability to center text automatically
    GAME_FONT_0.render_to(gameDisplay, (800 + labelLeftPadding, 0 + 9), "Hello World!", (255, 255, 255), None)

    # update squareContentsString. If it's off the map, string is "".
    pos = pygame.mouse.get_pos()
    if not coordsInBounds(pos[0], pos[1]):
        squareContentsString = ""
    else:
        squareContentsString = str(pos) + " - " + str(player.cell.getTileContents(pos[0], pos[1]))

    GAME_FONT_3.render_to(gameDisplay, (800 + labelLeftPadding, 750 + 19), squareContentsString, (255, 255, 255), None)
    # pygame.display.flip()
    pygame.display.update()

# initial render
def initialRender():
    renderTerrain()
    renderEntities()
    renderActors()
    renderLabels()
    pygame.display.flip()


# FIXME: debugging
# print("cell 0 entities: " + str(cell0.entities))
# print("cell 1 entities: " + str(cell1.entities))
# print(cells[0].entities)
# print(cells[1].entities)

# print("Player cell: " + str(player.cell.id))
# cell0.addEntity(0, [5, 5])  # add entity id 0 to square 5,5
# cell0.entities.append([2, [9, 9]])

# STARTS THE GAME
def initGame():
    loadCell(getCell(0))

    parseConfig()
    # test whether we can access Config from elsewhere
    print("Music: " + str(config['DEFAULT']['Music']))
    # print("Default HP: " + str(config['DEFAULT']['PlayerHp']))
    # print(str(config['DEFAULT']['Music']))
    # print(config['DEFAULT']['Music'])

    # if config['DEFAULT']['Music']:
    #     music = True
    #
    # if music:
    #     playMusic()

    # FIXME: fix ability to shut off music. Currently it always plays.
    if config['DEFAULT']['Music']:
        playMusic()

    pygameLoop()


def playMusic():
    print("Playing music...")
    # https://www.geeksforgeeks.org/how-to-add-music-playlist-in-pygame/
    exploreMusic = ['music/mx_explore_1.mp3', 'music/mx_explore_2.mp3', 'music/mx_explore_3.mp3',
                    'music/mx_explore_4.mp3', 'music/mx_explore_5.mp3', 'music/mx_explore_6.mp3',
                    'music/mx_explore_7.mp3']
    # for song in exploreMusic:
    #     # pygame.mixer.music.load(song)
    #     pygame.mixer.music.queue(song)
    # pygame.mixer.music.load()
    # pygame.mixer.music.play()

    # Adding songs file in our playlist
    playList = []
    for song in exploreMusic:
        playList.append(song)

    # Loading first audio file into our player
    pygame.mixer.music.load(playList[0])

    # Removing the loaded song from our playlist list
    playList.pop(0)

    # Playing our music
    pygame.mixer.music.play()

    # Queueing next song into our player
    pygame.mixer.music.queue(playList[0])
    playList.pop(0)

    # setting up an end event which host an event after the end of every song
    # pygame.mixer.music.set_endevent(pygame.MUSIC_END)


def parseConfig():
    # try to read the config file
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

    # try:
    #     print("Checking for config.ini...")
    #     print("Music: " + str(config['DEFAULT']['Music']))
    #     print("Default HP: " + str(config['DEFAULT']['PlayerHp']))
    # except:
    #     ("Config.ini not found. Generating default config file...")
    #     config['DEFAULT'] = {'Music': 'True', 'PlayerHp': '20'}
    #     with open('config.ini', 'w') as configfile:
    #         config.write(configfile)


global running
running = True


def pygameLoop():
    global running
    while running:
        for event in pygame.event.get():
            # what is the mouse hovering over?
            mousePos = pygame.mouse.get_pos()
            if debug:
                print("mousePos: " + str(mousePos))

            # FIXME: this could cause performance issues
            renderLabels()


            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()





            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print("mouse click at " + str(pos))

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print("mouse release at " + str(pos))

            # Movement Modifier keys (ctrl to run, etc): https://www.pygame.org/docs/ref/key.html

            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                # if event.type == pygame.KEYDOWN:
                # FIXME: used for testing
                # if event.type == pygame.KEYDOWN:
                #     print ("Key pressed")
                # if event.type == pygame.KEYUP:
                #     print ("Key released")

                # print("w: " + str(pygame.K_w))
                # print("a: " + str(pygame.K_a))
                # print("s: " + str(pygame.K_s))
                # print("d: " + str(pygame.K_d))
                #
                # if pygame.K_w:
                #     print("w pressed")
                # elif pygame.K_a:
                #     print("a pressed")
                # elif pygame.K_s:
                #     print("s pressed")
                # elif pygame.K_d:
                #     print("d pressed")

                # PYGAME get the status of an individual key
                if debug:
                    print("Keys pressed (W A S D): \n\t", end="")
                    print(str(pygame.key.get_pressed()[pygame.K_w]), end=", ")
                    print(str(pygame.key.get_pressed()[pygame.K_a]), end=", ")
                    print(str(pygame.key.get_pressed()[pygame.K_s]), end=", ")
                    print(str(pygame.key.get_pressed()[pygame.K_d]))
                # print("w pressed: " + str(pygame.key.get_pressed()[pygame.K_w]), end=", ")
                # print("a pressed: " + str(pygame.key.get_pressed()[pygame.K_w]), end=", ")
                # print("s pressed: " + str(pygame.key.get_pressed()[pygame.K_w]), end=", ")
                # print("d pressed: " + str(pygame.key.get_pressed()[pygame.K_w]), end=", ")

                # update player position according to which keys are pressed
                if pygame.key.get_pressed()[pygame.K_w]:
                    player.move("UP")
                elif pygame.key.get_pressed()[pygame.K_s]:
                    player.move("DOWN")
                elif pygame.key.get_pressed()[pygame.K_a]:
                    if player.facing == "LEFT":
                        player.move("LEFT")
                    elif player.facing == "RIGHT":
                        player.facing = "LEFT"
                elif pygame.key.get_pressed()[pygame.K_d]:
                    if player.facing == "RIGHT":
                        player.move("RIGHT")
                    elif player.facing == "LEFT":
                        player.facing = "RIGHT"
                # other player actions
                elif pygame.key.get_pressed()[pygame.K_f]:
                    player.interact()

                # PYGAME: updates the entire screen. Faster than update() due to OpenGL acceleration.
                # pygame.display.flip()
                # PYGAME: updates a portion, defined by arguments, of the screen
                # pygame.display.update()

                renderTerrain()
                renderEntities()
                renderActors()
                renderLabels()


                pygame.display.flip()

                print("Player cell: " + str(player.cell.id))

        # gameDisplay


def playWalkSound():
    print("[footstep]" + str(player.nextFootRight))
    if player.nextFootRight:
        pygame.mixer.Sound(sound_walkRight)
        player.nextFootRight = False
    else:
        pygame.mixer.Sound(sound_walkLeft)
        player.nextFootRight = True

    # FIXME: left sound, right sound...
    pygame.mixer.Sound.play(sound_walkRight)

pygame.font.init()
font = pygame.font.SysFont(None, 32)

# def displayMessage(message, color):
#     screen_text = font.render(message, True, color)
#     gameDisplay.blit(screen_text, [800, 50])

####

pygame.mixer.init()
nextFootRight = True
sound_walkLeft = pygame.mixer.Sound("sounds/LEFTWK1.wav")
sound_walkRight = pygame.mixer.Sound("sounds/RIGHTWK1.wav")

cells = []
cell0 = Cell(0, "cell0-terrain.csv")
cell1 = Cell(1, "cell1-terrain.csv")

print("cell0 info: " + str(cell0.terrain))
print("cell1 info: " + str(cell1.terrain))

global tileSize
tileSize = 50
global boardWidth
global boardHeight
boardWidth = 16
boardHeight = 16

pygameInit()

groundImg = pygame.image.load('grass2.png')
gameDisplay.blit(groundImg, (0, 0))
gameDisplay.blit(groundImg, (50, 0))

pygame.freetype.init()
GAME_FONT_0 = pygame.freetype.Font("fonts/LiberationMono-Bold.ttf", 32)
GAME_FONT_1 = pygame.freetype.Font("fonts/LiberationMono-Regular.ttf", 24)
GAME_FONT_2 = pygame.freetype.Font("fonts/LiberationMono-Regular.ttf", 16)
GAME_FONT_3 = pygame.freetype.Font("fonts/LiberationMono-Regular.ttf", 12)
# running = True

# # render grassy background
# for x in range (0, boardWidth):
#     for y in range (0, boardHeight):
#         gameDisplay.blit(groundImg, (x * tileSize, y * tileSize))


pcOriginX = (boardWidth / 2) * tileSize
pcOriginY = (boardHeight / 2) * tileSize
# gameDisplay.blit(testImg, (pcOriginX, pcOriginY))
player = Player(cell0, pcOriginX, pcOriginY)

cell0.addEntity(0, [5, 5])  # add entity id 0 to square 5,5
cell0.entities.append([2, [9, 9]])

initGame()


# test comment.