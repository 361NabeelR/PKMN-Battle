from pygame import *
import random
import math
import sys


#saves score from game into a new file.
def save(file,score1,score2):
    try:
        #opening file in write mode to store information on it
        File = open(file+".txt","w")
        #each line is dedicated to a single player's score
        File.write(f"{score1}\n{score2}")
        File.close()
    except:
        print("Error Saving Game:\n File Not Found")


#load function which finds your previous highscore
def load(file):
    try:
       File = open(file+".txt","r")
       #reads the first two lines where the score for each player is stored
       P1score = int(File.readline())
       P2score = int(File.readline())
       
    except FileNotFoundError: #if the file we're looking for doesn't exist
        P1score = 0
        P2score = 0

    return (P1score,P2score) #a tuple containing the player's scores






class Game():
    #counts time in milliseconds since last time ball bounced on something    
    LastBounce = 1000

    def __init__(self,WindowSize,P1score,P2score):
        #Main window is created upon which all other classes will share
        self.Window = display.set_mode(WindowSize)

        #variables to count players' scores
        self.P1score = P1score
        self.P2score = P2score
    
        #game objects created by using classes
        self.ball = Ball(self)
        self.P1paddle = Paddle(self,1)
        self.P2paddle = Paddle(self,2)

        self.ScoreBoard = ScoreBoard(self)
        
    def bounce(self,Object):
        #used when object collides with the ball and determines how the ball will move from there
        #mostly change to direction of motion

        #when ball hit from the top or bottom
        if Object.x <= self.ball.x <=Object.x+Object.width:
            self.ball.velY *= -1
        #when ball hits from the sides
        elif Object.y <= self.ball.y <= Object.y + Object.length:
            self.ball.velX *= -1
        #when ball hits a corner
        else:
            #math.copysign allows you take the value of one number and the sign of another which works
            #well here as it perfectly reflectes the change in the components of velocity. Thier values
            #switch and become the negative of each other.
            vx = math.copysign(self.ball.velY,-self.ball.velX)
            vy = math.copysign(self.ball.velX,-self.ball.velY)
            
    def draw(self):
        #drawing all game objects by calling the draw functions in each class
        self.ball.draw()
        self.P1paddle.draw()
        self.P2paddle.draw()
        self.ScoreBoard.draw(self.P1score, self.P2score)
        #field outline
        draw.rect(self.Window, "white",(-50,150,1300,645), width = 10)
        
    def update(self,dt,keys):
        self.ball.update(dt)#updates ball position based on time and speed
        self.P1paddle.update(dt,keys)#updates p1 paddles postion based on time and keys pressed
        self.P2paddle.update(dt,keys)#the same but for p2

        #if the hit box for the ball collides with the paddle hitbox and hasn't
        #bounced in the last 0.2 seconds
        if self.ball.rect.colliderect(self.P1paddle.rect) and self.LastBounce > 200:
            self.bounce(self.P1paddle)
            self.LastBounce = 0
        else:
            self.LastBounce += dt

        
        if self.ball.rect.colliderect(self.P2paddle.rect) and self.LastBounce > 200:
            self.bounce(self.P2paddle)
            self.LastBounce = 0
        else:
            self.LastBounce += dt
    
        
#displays score and title above
class ScoreBoard(): 
    #class variables

    Title = "MLG PONG"
    backgroundColour = "Gray60"
    TitleFont = 40
    ScoreFont = 30

    def __init__(self,game):
        #setting game window and font types used
        self.Window = game.Window
        self.FontT = font.SysFont("Arial",self.TitleFont)
        self.FontS = font.SysFont("Arial", self.ScoreFont)
        
    def draw(self,P1score, P2score):
        rect = (0,0,self.Window.get_width(),150)
        draw.rect(self.Window,self.backgroundColour,rect)

        #rendering Title text then placing it centered
        self.placeText(self.makeText(self.Title,"black", title = True),600,50,centered = True)

        #rendering and placing Score texts
        self.placeText(self.makeText(f"P1 Score: {P1score}","Blue"), 10,80)
        self.placeText(self.makeText(f"P2 Score: {P2score}","Red"), 1000,80)

    #makes text object containing colour of text and the text itself
    #I added the title paramter do differentiate between the title fonts and the score fonts
    def makeText(self,text,textColour,title = False):
        if title:
            return self.FontT.render(text,True,textColour,self.backgroundColour)
        else:
            return self.FontS.render(text,True,textColour,self.backgroundColour)

    # draws text object at given coordinates, which will either be centered or top left, based on choice
    def placeText(self, text, x,y,centered = False):

        #get the make the text object's rectangle
        textBox = text.get_rect()

        if centered:
            #centre coords are x,y
            textBox.center = (x,y)
        else:
            #changing the rects original coords to desired x, y
            textBox.move_ip(x,y)

        self.Window.blit(text,textBox)
    
class Ball():

    #class variables
    colour = "White"
    speed = 0.2
    radius = 15
    
    def __init__(self,game):
        #sets window to the same is game class window
        self.Window = game.Window
      


        #sets initial conditions of ball
        self.resetBall()
        
        #maximum coordinates ball may pass through,effectively making the field of pong
        self.maxRight = self.Window.get_width() - self.radius
        self.maxLeft = self.radius
        self.maxUp =  150 + self.radius
        self.maxDown = self.Window.get_height() - self.radius


        
    def draw(self):
        #spearating line in field
        draw.rect(self.Window, "white",( 595,150,10,800))
        #draws circle for ball
        draw.circle(self.Window,self.colour,(self.x,self.y),self.radius)
        #cool outline
        draw.circle(self.Window, "black" ,(self.x,self.y),self.radius, width = 2)
    def update(self,dt):#updates ball position every frame
        #change in displacement in x and y directions
        deltax = self.velX * dt
        deltay = self.velY * dt

        #updating x position
        self.x += deltax

        #checking if ball went too far left or right (when a point is scored)
        if self.x < self.maxLeft:
            self.resetBall()
            game.P2score += 1
            
        if self.x > self.maxRight:
            self.resetBall()
            game.P1score += 1
        #updating y position
        self.y += deltay

        #checking if ball went too far up or down
        if self.y < self.maxUp:
            self.y = 2*self.maxUp - self.y
            self.velY *= -1

        if self.y > self.maxDown:
            self.y = 2*self.maxDown - self.y
            self.velY *= -1
            
        #updates hitbox to new location
        self.rect.update(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)

    def resetBall(self):
        #initial coordinates
        self.x = 600
        self.y = 450

        #Ball angle set randomly so both teams have equal chance of hitting it first
        players = [1,2]
        randPick = random.choice(players)
        if randPick == 1:
        #these angles are specific so that it doesn't go all the way up and take forever
        #to reach the players
            angle = random.uniform(-0.25*math.pi,0.25*math.pi)
        else:
            angle = random.uniform(0.75*math.pi,1.25*math.pi)

        #velocityt components (trig stuff since horizontal component is cos of angle and vertical is sin)
        self.velX = self.speed * math.cos(angle)
        self.velY = self.speed * math.sin(angle)

        #draws collision (or hit) box
        self.rect = Rect(self.x -self.radius,self.y - self.radius,self.radius*2,self.radius*2)
        
class Paddle():
    #class variables
    length = 200
    width = 20
    speed = 0.8
    
    def __init__(self,game,player):
        self.Window = game.Window
        self.player = player
        #key variables position and coluor determined based on player
        if player == 1:
            self.colour = "blue"
            self.x = 50
            self.y = 375
        else:
            self.colour = "red"
            self.x = self.Window.get_width() - (50+self.width)
            self.y = 375

        #maximum coordinates so paddles don't fly off into the atmosphere
        self.maxUp = 150
        self.maxDown = self.Window.get_height() - self.length

        #hitbox is loaded
        self.rect = Rect(self.x,self.y,self.width,self.length)

        
        
   
    def draw(self):
        #drawing the paddles onto the screen
        draw.rect(self.Window, self.colour, self.rect)

    def update(self, dt, keys):
        #updating the y coordinates so the paddles go up and down when keys are pressed

        #determines what key controlls which players movement
        if self.player == 1: 
            
            if keys[K_w]:
                #new variable to store speed but with direction this time (vector quantity)
                velocity = -self.speed
            elif keys[K_s]:
                velocity = self.speed
            else:
                velocity = 0 #so paddles don't move if no key is pressed
                
        else:

            if keys[K_UP]:
                velocity = -self.speed
            elif keys[K_DOWN]:
                velocity = self.speed
            else: velocity = 0 #so paddles don't move if not key is pressed

        #updating y position
        delta = velocity*dt
        self.y += delta

        #blocking movement off screen
        if self.y < self.maxUp:
            self.y = self.maxUp
        elif self.y > self.maxDown:
            self.y = self.maxDown

        #update hitbox
        self.rect.update(self.x,self.y,self.width, self.length)
        
    

#checks to see if pygame is working or not
if init()[1] != 0:
    print("Error initializing PyGame")


#Welcome Message and Save file Recording
print("Welcome to MLG PONG!\nWhen you quit your file will autmatically save")
saveFile = input("Please enter your file name, or if you're new, name your new file:\n")

#loading Playerscores
P1score = load(saveFile)[0]
P2score = load(saveFile)[1]


Screen = (1200,800)
game = Game(Screen,P1score,P2score)#constructs game
clock = time.Clock()#counts the time in between frames


                
#Main Game loop

while True:

    for Event in event.get():
        #event.get gets all current key presses and mouse actions being done
        if Event.type == QUIT:
            save(saveFile,game.P1score,game.P2score)
            quit()
            sys.exit()
           

    #sets max fps to 60 and also counts all time between frames     
    dt = clock.tick(60)

    
    keys = key.get_pressed()#gets list of all currently pressed keys

    #calls update function using keys and dt as a paramter so we can use them in all the other classes
    game.update(dt, keys)

    #sets background colour
    game.Window.fill("Dark Green")

    #calls draw function for game class
    game.draw()
    
    display.update()
    







    
        
