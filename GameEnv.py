import pyglet
from pyglet import shapes

window = pyglet.window.Window(width=1280, height = 720, caption = 'Car Simulator')
circle = shapes.Circle(x=700,y=150,radius=100, color=(50,225,30))
#label = pyglet.text.Label('Car goes Vroom Vroom',font_name='Times New Roman',font_size=36,x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center')

#Registering the function
@window.event
def on_draw():
    window.clear()
    circle.draw()
    
pyglet.app.run()