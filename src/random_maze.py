import pygame
import random
 
# Define some colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)

mazecolors = [white, black, red]
doorsize = 10
min_room_size = 4 *doorsize

# Initialize pygame
pygame.init()
  
# Set the height and width of the screen
size=[1000,1000]
screen=pygame.display.set_mode(size)
# Set the screen background
screen.fill(white)
      
# Set title of screen
pygame.display.set_caption("Random Maze")
 
# Create a 2 dimensional array. A two dimensional
# array in our implementation is simply a list of lists.
# Each cell corresponds to a 5 pixel x 5 pixel area of the screen surface.
def NewEmptyMaze():
    newmazegrid=[]
    for row in xrange(200):
        # Add an empty array that will hold each cell in this row
        newmazegrid.append([])
        for column in xrange(200):
            newmazegrid[row].append(0) # Append a cell
    return newmazegrid

mazegrid = NewEmptyMaze()

# code to be implemented

def GenerateMaze():
    #create the initial four outside walls
    for i in xrange(200):
        mazegrid[0][i] = 1
        mazegrid[199][i] = 1
        mazegrid[i][0] = 1
        mazegrid[i][199] = 1
        
    #create the initial door in top left 
    for i in xrange(doorsize/2):
        mazegrid[0][i] = 0
        mazegrid[i][0] = 0
        
    #create all the inner rooms
    AddWalls(mazegrid, (0,0), (200,200), True)
    
    
def AddWalls(mazegrid, room_topleft, room_botright, cheeseflag):
    #unpack coord tuples
    tl_X, tl_Y = room_topleft
    br_X, br_Y = room_botright
    room_W, room_H = br_X - tl_X, br_Y - tl_Y
    
    #if not base case (room is small enough) make more rooms
    if room_W > min_room_size and room_H > min_room_size:
        
        #get new wall x and y 
        rX = random.randint(tl_X+doorsize*2,br_X-doorsize*2)
        rY = random.randint(tl_Y+doorsize*2,br_Y-doorsize*2)
        
        #draw new walls
        for x in xrange(tl_X,br_X):
            mazegrid[x][rY] = 1
        for y in xrange(tl_Y,br_Y):
            mazegrid[rX][y] = 1
        
        #remove part of new walls to make new doors
        for i in xrange(doorsize):
            mazegrid[rX - (doorsize/2) + i][rY]=0
            mazegrid[rX][rY - (doorsize/2) + i]=0
        
        #recursive call to make each sub-room
        cflag = 0
        if cheeseflag:
            cflag = random.randint(1,4)
        AddWalls(mazegrid, (tl_X, tl_Y), (rX, rY), cflag==1)
        AddWalls(mazegrid, (rX, tl_Y), (br_X, rY), cflag==2)
        AddWalls(mazegrid, (tl_X, rY), (rX, br_Y), cflag==3)
        AddWalls(mazegrid, (rX, rY), (br_X, br_Y), cflag==4)
        
    else:
        #only add cheese if room is not big enough to recurse
        #also check if it actually is the cheese room
        if cheeseflag==True:
            #make a 3x3 cheese randomly in the cheese room 
            rX = random.randint(tl_X+3,br_X-3)
            rY = random.randint(tl_Y+3,br_Y-3)
            for x in xrange(rX-1,rX+1):
                for y in xrange(rY-1,rY+1):
                    mazegrid[x][y]=2
        
    
def DisplayMaze():
    screen.fill(white)
    for y in xrange(len(mazegrid)):
        for x in xrange(len(mazegrid[y])):
            pygame.draw.rect(screen, mazecolors[mazegrid[x][y]], pygame.Rect(x*5,y*5,5,5))


# Loop until the user clicks the close button.
done=False

# Used to manage how fast the screen updates
clock=pygame.time.Clock()

######################################
# -------- Main Program Loop -----------
while done==False:
    for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            if event.type == pygame.KEYDOWN: # If user wants to perform an action
                if event.key == pygame.K_m:
                    mazegrid = NewEmptyMaze()
                    GenerateMaze()
                    DisplayMaze()
                if event.key == pygame.K_ESCAPE:
                    done=True
   
    # Limit to 20 frames per second
    clock.tick(20)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
     
# If you forget this line, the program will 'hang' on exit.
pygame.quit ()