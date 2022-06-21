import math
import random
import pygame
from pygame import mixer

#A clock, image scaling, bullet velocity and hitbox (for difficulty), and a bar that when touched by the enemy ends the game are the modifications made in the game

pygame.init() #Turns on pygame

screen = pygame.display.set_mode((1000, 700)) #display and dimensions of the screen 

#the background of the screen
wallpaper = pygame.image.load("batcave.jpeg") 
wallpaper = pygame.transform.scale(wallpaper, (1000, 700))

mixer.music.load("rafters.flac") #loads flac batman ost 
mixer.music.play(-1) #loops the ost

pygame.display.set_caption("Batcave Battle") #Screen title
icon = pygame.image.load("batsymbol.jpeg") 
pygame.display.set_icon(icon) #makes the bar icon the bat symbol

the_batman = pygame.image.load("batman.jpeg")
the_batman = pygame.transform.scale(the_batman, (100, 100))
batman_x = 370
batman_y = 600
batman_x_mod = 0 #"mod" means the modification of the game

#lists where information of the parademons are appended to
parademons_image = [] 
parademons_x = []
parademons_y = []
parademons_x_mod = []
parademons_y_mod = []
number_parademons = 20 #number of parademons needed to be destroyed

def rotate_image(the_batman):
    the_batman = pygame.transform.rotate.rotozoom(parademons, 20, 1)
    return the_batman

#this for loop determines the number of parademons and embeds them with an x and y position and appends them to their lists
for i in range(number_parademons): 
    parademons = pygame.image.load("parademons.webp")
    parademons = pygame.transform.scale(parademons, (75, 75)) 
    parademons_image.append(parademons) #this is where the append occurs
    parademons_x.append(random.randint(0, 720)) #the random x coordinate
    parademons_y.append(random.randint(50, 100)) #the random x coordinate
    parademons_x_mod.append(10) #mod in the position
    parademons_y_mod.append(20) #mod in the position

batarang_image = pygame.image.load("batarang.jpeg")
batarang_image = pygame.transform.scale(batarang_image, (50, 50)) #Scales the projectile down

batarang_x = 0 #x coordinate of the batarang
batarang_y = 700 #y coordinate of the batarang
batarang_x_mod = 0 #mod where the batarang position doesn"t change
batarang_y_mod = 20 #mod of velocity quantity
batarang_status = "pressed" 

points_counter = 0 #variable for the points counter
font = pygame.font.SysFont("times", 40) #

border = pygame.Rect(0, 340, 1000, 10) #the border

#x and y positions of the words
score_tally_x = 10 
score_tally_y = 10

end_credits_font = pygame.font.SysFont("times", 64) #font for the end credits sentence

#function for the score counter 
def score_counter(x, y):
    score = font.render("Score : " + str(points_counter), True, (255, 255, 255)) #Shows the score in a strong, while true (Always) in white
    screen.blit(score, (x, y))

#function for the end credits after the game ends
def end_credits():
    finished_words = end_credits_font.render("You have been defeated", True, (255, 0, 0))#Shows the score in a strong, while true (Always) in white
    screen.blit(finished_words, (100, 350))

#function of the position of the player
def player(x, y):
    screen.blit(the_batman, (x, y))

#function of the position of the parademons
def parademons_control(x, y, i):
    screen.blit(parademons_image[i], (x, y))

#function of the batarang being thrown
def batarang_toss(x, y):
    global batarang_status
    batarang_status = "shoot" 
    screen.blit(batarang_image, (x+38, y+80)) #bullets initial position

#function of the batarang in contact with the parademons
def batarang_strike(parademons_x, parademons_y, batarang_x, batarang_y):
    distance = math.sqrt(math.pow(parademons_x - batarang_x, 2) + (math.pow(parademons_y - batarang_y, 2))) 
    if distance < 30:
        return True
    else:
        return False

#velocity of the game
fps = pygame.time.Clock() 

playing = True 
while playing: #while loop that determines whether the game is starting
    fps.tick(60)
    screen.fill((0, 0, 0)) #initially fills the screen black to initiate start time
    screen.blit(wallpaper, (0, 0)) 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #if user clicks x the game ends
            playing = False

        #The controls for the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                batman_x_mod = -5
            if event.key == pygame.K_d:
                batman_x_mod = 5
            if event.key == pygame.K_LSHIFT:
                if batarang_status is "pressed": 
                    batarang_sound = mixer.Sound("toss.mp3") #the sound played when shift key is pressed
                    batarang_sound.play()
                    batarang_x = batman_x
                    batarang_toss(batarang_x, batarang_y)

        #this stops batman from moving after player stops pressing moving keys
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d:
                batman_x_mod = 0

    #mod where the player isn"t allowed to move off screen
    batman_x += batman_x_mod 
    if batman_x <= 0:
        batman_x = 0
    elif batman_x >= 890:
        batman_x = 890 

    #the number of parademons are indexed
    for i in range(number_parademons):
        #this if statement ends the game once the parademons cross the border
        if parademons_y[i] > 250: 
            for j in range(number_parademons):
                parademons_y[j] = 501 #the point where the game is lost
            end_credits()
            break

        #mod to prevent the parademons from moving off screen
        parademons_x[i] += parademons_x_mod[i]
        if parademons_x[i] <= 0:
            parademons_x_mod[i] = 4
            parademons_y[i] += parademons_y_mod[i]
        elif parademons_x[i] >= 950:
            parademons_x_mod[i] = -4
            parademons_y[i] += parademons_y_mod[i]

        strike = batarang_strike(parademons_x[i], parademons_y[i], batarang_x, batarang_y)
        if strike:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            batarang_y = 480
            batarang_status = "pressed"
            points_counter += 1
            parademons_x[i] = random.randint(0, 780) #random positioning for the parademons
            parademons_y[i] = random.randint(50, 150)

        parademons_control(parademons_x[i], parademons_y[i], i)

    if batarang_y <= 0:
        batarang_y = 480
        batarang_status = "pressed" 

    if batarang_status == "shoot": #the change in position of the batarangs
        batarang_toss(batarang_x, batarang_y)
        batarang_y -= batarang_y_mod

    player(batman_x, batman_y) #position of batman
    score_counter(score_tally_x, score_tally_y) #coordinates of the score 
    pygame.draw.rect(screen, (0,0,0), border) #the dimensions of the border
    pygame.display.update()
