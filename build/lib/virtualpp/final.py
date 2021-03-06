import numpy as np
import cv2
import random
import pygame
from pygame.locals import *

cap = cv2.VideoCapture(0) #This enables the camera.The value 1 is for external camera,0 for internal camera
p=100
i=0
pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Ping Pong')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH//2,HEIGHT//2]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)

    if right == False:
        horz = - horz

    ball_vel = [horz,-vert]

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT//2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT//2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score

    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2, 0],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel

    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [(592,0),(600,0),(600,1000),(592,1000)], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1])>=paddle1_pos[1]-HALF_PAD_HEIGHT and int(ball_pos[1])<=paddle1_pos[1]+HALF_PAD_HEIGHT:
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.3
        ball_vel[1] *= 1.3
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)

    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(0,592 + 500,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.3
        ball_vel[1] *= 1.3

    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (470, 20))


#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel
    '''
    if event.key == K_w:
        paddle2_vel = -8
    elif event.key == K_s:
        paddle2_vel = 8
        '''
    if event == 1 and paddle1_pos[1]>40:
        #paddle1_vel = -8
        paddle1_pos[1] += -0.5
        '''
    elif event.key == K_DOWN:
        paddle1_vel = 8
        '''

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    '''
    if event.key in (K_UP, K_DOWN):
        paddle1_vel = 0
        '''
    if event==1 and paddle1_pos[1]<360:
        #paddle2_vel = 8
        paddle1_pos[1] += 0.5

init()

def game(ColorLow,ColorHigh):
    #game loop
    cX=25
    cY=25
    while True:
        ret, frame = cap.read()  #returns ret=either true or false. the frame variable has the frames
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        '''
        why did we convert to hsv ? because while using BGR,we have to use 3 values for color combinations(eg.(255,90,30))
        But in case of hsv,for getting the required color,we have to change only one parameter,that is ,hue ,and the two other parameters can be changed just to change the saturation and values.
        '''
        blur = cv2.GaussianBlur(hsv,(5,5),5)
        '''
        The blurring is set to high here. we did blurring because,blurring eliminates the image noise and  reduce detail.
        '''
        lower_orange = np.array(ColorLow)#see,the hue from 0,30 is used here for orange,but remeber to set the other values too according to your need.If the other two values are zero,then you will get black because of zero intensity
        upper_orange = np.array(ColorHigh)
        mask = cv2.inRange(blur, lower_orange, upper_orange)
        '''
        the color from lower orange to upper orange is noted here.
        '''
        ret, thresh_img = cv2.threshold(mask,91,255,cv2.THRESH_BINARY)
        '''
        Here, the matter is straight forward.
        If pixel value is greater than a threshold value, it is assigned one value (may be white), else it is assigned another value (may be black).
        The function used is cv.threshold. First argument is the source image, which should be a grayscale image.
        Second argument is the threshold value which is used to classify the pixel values.
        Third argument is the maxVal which represents the value to be given if pixel value is more than (sometimes less than) the threshold value.
        OpenCV provides different styles of thresholding and it is decided by the fourth parameter of the function.
        '''
        contours =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]#ah,the cool fun part!draw contours over the required orange area!
        '''
        I gave the parameter thresh_img here as input. If I gave frame as input I would get contours for every shape in the camera.
        But by masking and thresholding, I have concentrated my interests into just the orange area .
        '''
        M = cv2.moments(mask)
        if M["m00"]!=0 :
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        #These moments and cX and cY ,i used to draw centroids.I will be using the centroid of the orange area.
        cv2.circle(frame, (cX, cY), 5, (255, 255, 255), -1)
        cv2.putText(frame, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        for c in contours:
            cv2.drawContours(frame, [c], -1, (0,255,0), 3)#in previous function of contours i just only found contours. Now here I am drawing
        cv2.imshow("frame",frame)
        p=200
        i=0
        if cY>=p:
            for j in range(int((cY-p)/10)):
                keydown(1)

            p=cY
            '''
            Simulating down arrow pressing when the centroid moves down
            '''
        else:
            for j in range(int((p-cY)/10)):
                keyup(1)
            p=cY
            '''
            Simulating up arrow pressing when the centroid moves up
            '''
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        draw(window)
        pygame.display.update()
        fps.tick(100)

    cap.release()#release the camera beast
    cv2.destroyAllWindows()
def GameColor(color):
    if color=="GREEN":
        game([51,74,160],[90,147,255])
    if color=="ORANGE":
        game([0,150,150],[30,255,255])
