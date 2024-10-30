import pyglet
from pyglet import shapes

window = pyglet.window.Window(width=800, height = 800, caption = 'Race Track')

track_image = pyglet.resource.image('track.png')
track_sprite = pyglet.sprite.Sprite(track_image, x=0, y=0)

imageWidth = 800
imageHeight = 800

track_sprite.width = imageWidth
track_sprite.height = imageHeight
#circle = shapes.Circle(x=700,y=150,radius=100, color=(50,225,30))
#label = pyglet.text.Label('Car goes Vroom Vroom',font_name='Times New Roman',font_size=36,x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')

#Registering the function
@window.event
def on_draw():
    track_sprite.draw()
    #window.clear()
    #circle.draw()
pyglet.app.run()