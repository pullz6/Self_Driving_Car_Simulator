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
line_top1 = shapes.Line(230, 295, 570, 295, width=11.5)
line_bottom1 = shapes.Line(230, 123, 570, 123, width=11.5, color=(200,20,20))

# Control points for the semicircle
RADIUS = 185
CENTER_X = 195
CENTER_Y = 210
start_angle = math.pi / 2 # Start angle in radians
angle = math.pi

# Create an arc for the rounded edges
arc = shapes.Arc(x=CENTER_X, y=CENTER_Y, radius = RADIUS, start_angle= start_angle , angle=angle, color=(255, 0, 0),segments=100,thickness = 11.5)

#For the outer track 
#Creating the track boundary with circles for the edges 


##First lets create the lines o the track 
line_top2 = shapes.Line(190, 660, 610, 660, width=11.5, color=(200,20,20))
line_bottom2 = shapes.Line(190, 13.7, 610, 13.7, width=11.5, color=(200,20,20))


#Registering the function
@window.event
def on_draw():
    track_sprite.draw()
    line_top1.draw()
    circle1_left.draw()
    circle1_right.draw()
    line_bottom1.draw()
    line_top2.draw()
    arc.draw()
    line_bottom2.draw()
    
    
pyglet.app.run()