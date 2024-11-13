import pyglet
from pyglet import shapes
from shapely.geometry import Polygon
import math

#Create the window
window = pyglet.window.Window(width=800, height = 400, caption = 'Race Track')

#Add the track image
track_image = pyglet.resource.image('track_3.png')
track_sprite = pyglet.sprite.Sprite(track_image, x=0, y=0)

#Resize the image
imageWidth = 800
imageHeight = 523
track_sprite.width = imageWidth
track_sprite.height = imageHeight

#For the innner track
#Creating the track boundary with circles for the edges 
circle1_left = shapes.Circle(x=230,y=209,radius=91, color=(50,225,30))
circle1_right = shapes.Circle(x=570,y=209,radius=91, color=(50,225,30))

##First lets create the lines o the track 
line_top1 = shapes.Line(230, 295, 570, 295, width=11.5, color=(200,20,20))
line_bottom1 = shapes.Line(230, 123, 570, 123, width=11.5, color=(200,20,20))

# Control points for the semicircle
RADIUS = 185
CENTER_X = 195
CENTER_Y = 210
start_angle = math.pi / 2 # Start angle in radians
angle = math.pi

# Create an arc for the rounded edges
arc_1 = shapes.Arc(x=CENTER_X, y=CENTER_Y, radius = RADIUS, start_angle= start_angle , angle=angle, color=(255, 0, 0),segments=100,thickness = 11.5)

RADIUS = 185
CENTER_X = 600
CENTER_Y = 210
start_angle = 3 * math.pi / 2  # Start angle at 270 degrees (3π/2 radians)
angle = math.pi

# Create an arc for the rounded edges
arc_2 = shapes.Arc(x=CENTER_X, y=CENTER_Y, radius = RADIUS, start_angle= start_angle , angle=angle, color=(255, 0, 0),segments=100,thickness = 11.5)


#For the outer track 

##First lets create the lines o the track 
line_top2 = shapes.Line(190, 395, 610, 395, width=11.5, color=(200,20,20))
line_bottom2 = shapes.Line(190, 14, 610, 13.7, width=11.5, color=(200,20,20))

# --- Agent Class ---
class Agent:
    def __init__(self, x, y, size=10, speed=2):
        # Initial agent position
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

        # Shape of the agent (for visualization)
        self.shape = shapes.Circle(self.x, self.y, self.size, color=(0, 0, 255))

    def move(self, direction):
        """
        Move the agent in the specified direction:
        'left' = turn left
        'right' = turn right
        'up' = move up (north)
        'down' = move down (south)
        """
        if direction == 'left':  # Move agent left
            self.x -= self.speed
        elif direction == 'right':  # Move agent right
            self.x += self.speed
        elif direction == 'up':  # Move agent up
            self.y += self.speed
        elif direction == 'down':  # Move agent down
            self.y -= self.speed

        # Update the agent's shape position
        self.shape.x = self.x
        self.shape.y = self.y

    def get_position(self):
        return self.x, self.y

    def draw(self):
        self.shape.draw()

# Create agent instance
agent = Agent(x=70, y=220)  # Start the agent at some initial position

#Registering the function
@window.event
def on_draw():
    track_sprite.draw()
    #Inner Track
    line_top1.draw()
    circle1_left.draw()
    circle1_right.draw()
    line_bottom1.draw()
    #OuterTrack
    line_top2.draw()
    arc_1.draw()
    arc_2.draw()
    line_bottom2.draw()
    agent.draw()


# Registering the function for keyboard input to control the agent
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.LEFT:
        agent.move('left')  # Move left
    elif symbol == pyglet.window.key.RIGHT:
        agent.move('right')  # Move right
    elif symbol == pyglet.window.key.UP:
        agent.move('up')  # Move up
    elif symbol == pyglet.window.key.DOWN:
        agent.move('down')  # Move down

# Run the pyglet application
pyglet.app.run()