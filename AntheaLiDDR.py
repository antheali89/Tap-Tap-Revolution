import pygame
from pygame.locals import *
import random

# initialize the game
pygame.init() # command that initializes the game
width, height = 700, 500 
screen=pygame.display.set_mode((width, height)) # set the dimensions of the window
score = 0
leftarrows = []  # 4 arrays of arrows for each direction
uparrows = [] 
downarrows = []
rightarrows = []
arrows = [] # all the arrows
arrowtimer = 20 # countdown timer to space out the spawning of the arrows
speedtimer = 1000 # countdown timer for incrementing speed 
paused = False # boolean value for pausing
jobtext = None # the name for the messages that show up telling how accurate you were with your key pressing
jobtimer = 40 # timer for the messages
exitcode = 0 # variable that keeps track of whether the game is over

# load images
background = pygame.image.load("images/background.jpg")
pause = pygame.image.load("images/pause.png")

# arrow class
class Arrow:
    # constructor for the Arrow class
    def __init__(self, direction, isEmpty): # isEmpty tells whether the arrow is a moving arrow or stationary arrow
                                            # (empty as in not colored in like the moving arrows)
        self.direction = direction # direction is the direction of the arrow
        self.speed = 3 # keeps track of the speed of the arrow
        if isEmpty == False: # if the arrow is a moving colored arrow
            if self.direction == 1: # left
                self.x = 300 # initializing x-values of which the arrows are printed on the screen
                self.image = pygame.image.load("images/leftarrow.gif")
                leftarrows.append(self)
            elif self.direction == 2: # up
                self.x = 375
                self.image = pygame.image.load("images/uparrow.gif")
                uparrows.append(self)
            elif self.direction == 3: # down
                self.x = 450
                self.image = pygame.image.load("images/downarrow.gif")
                downarrows.append(self)
            elif self.direction == 4: # right
                self.x = 525
                self.image = pygame.image.load("images/rightarrow.gif")
                rightarrows.append(self)
            self.y = 500 # one constant y value for all moving arrows at the beginning before they begin moving
        elif isEmpty == True:
            if self.direction == 1: # left
                self.x = 300
                self.image = pygame.image.load("images/emptyleftarrow.png")
                leftarrows.append(self)
            elif self.direction == 2: # up
                self.x = 375
                self.image = pygame.image.load("images/emptyuparrow.png")
                uparrows.append(self)
            elif self.direction == 3: # down
                self.x = 450
                self.image = pygame.image.load("images/emptydownarrow.png")
                downarrows.append(self)
            elif self.direction == 4: # right
                self.x = 525
                self.image = pygame.image.load("images/emptyrightarrow.png")
                rightarrows.append(self)
            self.y = 100 # one constant  y value for all stationary arrows
            
    # modifier methods
    def changeY(self):
        self.y -= self.speed
        return self.y
    
    def changeSpeed(self):
        self.speed += 0.05
        
    def delete(self): # delete the arrow from its respective direction array
        if self.direction == 1:
            leftarrows.remove(self)
        elif self.direction == 2:
            uparrows.remove(self)
        elif self.direction == 3:
            downarrows.remove(self)
        elif self.direction == 4:
            rightarrows.remove(self)
        arrows.remove(self)

# initialize empty arrows
emptyLeftArrow = Arrow(1, True)
emptyUpArrow = Arrow(2, True)
emptyDownArrow = Arrow(3, True)
emptyRightArrow = Arrow(4, True)

# loop
while 1:
    # event listener for pausing with space bar
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                if paused == False:
                    paused = True
                else:
                    paused = False
    
    screen.fill((0, 0, 0)) # reset the screen before printing everything on it over again
    # decrement all timers
    arrowtimer -= 1 
    speedtimer -= 1
    jobtimer -= 1

    # print background image and stationary arrows onto screen
    screen.blit(background, (0, 0))
    screen.blit(emptyLeftArrow.image, (emptyLeftArrow.x, emptyLeftArrow.y))
    screen.blit(emptyUpArrow.image, (emptyUpArrow.x, emptyUpArrow.y))
    screen.blit(emptyDownArrow.image, (emptyDownArrow.x, emptyDownArrow.y))
    screen.blit(emptyRightArrow.image, (emptyRightArrow.x, emptyRightArrow.y))

    # print the score
    scorefont = pygame.font.Font("fonts/halo.ttf", 42)
    scoretext = scorefont.render(str(score), True, (255, 160, 122))
    screen.blit(scoretext, (10, 450))

    # print messages showing your accuracy
    if jobtimer >= 0 and jobtext != None: # blit "great" etc. messages if timer hasn't run out
        screen.blit(jobtext, (385, 50))
        
    # print arrows
    for arr in arrows: # blit arrows that already exist 
        screen.blit(arr.image, (arr.x, arr.y))

    ################################### main game loop #####################################
    if paused == False and exitcode == 0: # if game isn't paused and isn't over
        if arrowtimer <= 0 and random.randrange(0, 1000) < 20: # decide randomly if an arrow spawns, but only if the timer
            arrow = Arrow(random.randint(1, 4), False)         # has run out 
            arrows.append(arrow)
        # delete arrows when they go off the screen
        arrows[:] = [arr for arr in arrows if not arr.y <= 0] # list comprehension!! remove all items in the list that don't
        for arr in arrows:                                    # pass the if statement  
            # print arrows onto screen
            if speedtimer <= 0: # if the speed timer has run out, change the speed of the arrow
                arr.changeSpeed()
            arr.changeY() # increment arrow's y-value so it "moves" across the screen with each frame

        # 30 second timer
        font = pygame.font.Font("fonts/astronboyvideo.ttf", 36)
        survivedtext = font.render(str((30000-pygame.time.get_ticks())/60000)+":"+
                                   str((30000-pygame.time.get_ticks())/1000%60).zfill(2),
                                   True, (216, 191, 216))
        textRect = survivedtext.get_rect()
        textRect.topright=[635,5]
        screen.blit(survivedtext, textRect)
        if pygame.time.get_ticks() >= 30000: # if timer has gone to 0, end game
            exitcode = 1
            
        # event checking
        jobfont = pygame.font.Font("fonts/Gasalt-Black.ttf", 36) # font for accuracy messages
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_LEFT: # if user has pressed the left arrow key
                    for arr in arrows:
                        if(arr.direction == 1): # only modify the left arrows in the arrows array
                            # the following if statements are for printing out the accuracy messages, each one testing
                            # if the arrow is within some distance to the empty stationary arrow
                            if(emptyLeftArrow.y - 10 <= arr.y <= emptyLeftArrow.y + 10):
                                score += 20
                                jobtext = jobfont.render("AWESOME!!!!!", True, (221, 160, 221))
                            elif(emptyLeftArrow.y - 25 <= arr.y <= emptyLeftArrow.y + 25):
                                score += 15
                                jobtext = jobfont.render("great!!!!", True, (152, 251, 152))
                            elif(emptyLeftArrow.y - 50 <= arr.y <= emptyLeftArrow.y + 50):
                                score += 10
                                jobtext = jobfont.render("better!", True, (176, 224, 230))
                            elif(emptyLeftArrow.y - 100 <= arr.y <= emptyLeftArrow.y + 100):
                                score += 5
                                jobtext = jobfont.render("what", True, (238, 233, 233))
                            else:
                                continue
                            jobtimer = 40 # reset the timer for displaying accuracy messages
                    # removing the arrows that have a key has been pressed down for from both arrays
                    leftarrows[:] = [arr for arr in leftarrows if not (arr.y <= emptyLeftArrow.y + 50)]
                    arrows[:] = [arr for arr in arrows if arr in leftarrows or arr.direction != 1]
                # same idea as above but for the rest of the arrow keys
                elif event.key == K_UP:
                    for arr in arrows:
                        if(arr.direction == 2):
                            if(emptyUpArrow.y - 10 <= arr.y <= emptyUpArrow.y + 10):
                                score += 20
                                jobtext = jobfont.render("AWESOME!!!!!", True, (221, 160, 221))
                            elif(emptyUpArrow.y - 25 <= arr.y <= emptyUpArrow.y + 25):
                                score += 15
                                jobtext = jobfont.render("great!!!!", True, (152, 251, 152))
                            elif(emptyUpArrow.y - 50 <= arr.y <= emptyUpArrow.y + 50):
                                score += 10
                                jobtext = jobfont.render("can do better", True, (176, 224, 230))
                            elif(emptyUpArrow.y - 100 <= arr.y <= emptyUpArrow.y + 100):
                                score += 5
                                jobtext = jobfont.render("what", True, (238, 233, 233))
                            else:
                                continue
                            jobtimer = 40
                    uparrows[:] = [arr for arr in uparrows if not (arr.y <= emptyUpArrow.y + 50)]
                    arrows[:] = [arr for arr in arrows if arr in uparrows or arr.direction != 2]
                elif event.key == K_DOWN:
                    for arr in arrows:
                        if(arr.direction == 3):
                            if(emptyDownArrow.y - 10 <= arr.y <= emptyDownArrow.y + 10):
                                score += 20
                                jobtext = jobfont.render("AWESOME!!!!!", True, (221, 160, 221))
                            elif(emptyDownArrow.y - 25 <= arr.y <= emptyDownArrow.y + 25):
                                score += 15
                                jobtext = jobfont.render("great!!!!", True, (152, 251, 152))
                            elif(emptyDownArrow.y - 50 <= arr.y <= emptyDownArrow.y + 50):
                                score += 10
                                jobtext = jobfont.render("better!", True, (176, 224, 230))
                            elif(emptyDownArrow.y - 100 <= arr.y <= emptyDownArrow.y + 100):
                                score += 5
                                jobtext = jobfont.render("what", True, (238, 233, 233))
                            else:
                                continue
                            jobtimer = 40
                    downarrows[:] = [arr for arr in downarrows if not (arr.y <= emptyDownArrow.y + 50)]
                    arrows[:] = [arr for arr in arrows if arr in downarrows or arr.direction != 3]
                elif event.key == K_RIGHT:
                    for arr in arrows:
                        if(arr.direction == 4):
                            if(emptyRightArrow.y - 10 <= arr.y <= emptyRightArrow.y + 10):
                                score += 20
                                jobtext = jobfont.render("AWESOME!!!!!", True, (221, 160, 221))
                            elif(emptyRightArrow.y - 25 <= arr.y <= emptyRightArrow.y + 25):
                                score += 15
                                jobtext = jobfont.render("great!!!!", True, (152, 251, 152))
                            elif(emptyRightArrow.y - 50 <= arr.y <= emptyRightArrow.y + 50):
                                score += 10
                                jobtext = jobfont.render("better!", True, (176, 224, 230))
                            elif(emptyRightArrow.y - 100 <= arr.y <= emptyRightArrow.y + 100):
                                score += 5
                                jobtext = jobfont.render("what", True, (238, 233, 233))
                            else:
                                continue
                            jobtimer = 40
                    rightarrows[:] = [arr for arr in rightarrows if not (arr.y <= emptyRightArrow.y + 50)]
                    arrows[:] = [arr for arr in arrows if arr in rightarrows or arr.direction != 4]
                # if space button was pressed, pause the game
                elif event.key == K_SPACE:
                    if paused == False:
                        paused = True
                    else:
                        paused = False
    # if the game timer has run out and the game is over
    elif exitcode == 1:
        # print "GAME OVER" message
        gameoverfont = pygame.font.Font("fonts/prstart.ttf", 72)
        gameovertext = gameoverfont.render("GAME OVER", True, (255, 0, 0))
        screen.blit(gameovertext, (30, 200))
        # print user's score
        scorefont = pygame.font.Font("fonts/prstart.ttf", 40)
        scoretext = scorefont.render("Score: " + str(score), True, (255, 160, 122))
        screen.blit(scoretext, (160, 350))
    # if game is paused, print pause symbol on screen
    elif paused == True:
        screen.blit(pause, (100, 25))
    
    pygame.display.flip()
