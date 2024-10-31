import pyglet
from pyglet import shapes
from shapely.geometry import Polygon

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

#Creating the track boundary 

##First lets create the lines
line_top1 = shapes.Line(230, 295, 570, 295, width=12)
line_bottom1 = shapes.Line(230, 111, 570, 111, width=12, color=(200,20,20))

#Registering the function
@window.event
def on_draw():
    track_sprite.draw()
    line_top1.draw()
    line_bottom1.draw()
    
pyglet.app.run()