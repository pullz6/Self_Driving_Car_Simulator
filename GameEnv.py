import pyglet
from pyglet import shapes
import random
import numpy as np
from math import sqrt, atan2

# Create the window
window = pyglet.window.Window(width=800, height=400, caption='Race Track')

# Add the track image
track_image = pyglet.resource.image('track_3.png')
track_sprite = pyglet.sprite.Sprite(track_image, x=0, y=0)

# Resize the image
imageWidth = 800
imageHeight = 523
track_sprite.width = imageWidth
track_sprite.height = imageHeight

# Define track boundaries and obstacles
circle1_left = shapes.Circle(x=230, y=209, radius=91, color=(50, 225, 30))
circle1_right = shapes.Circle(x=570, y=209, radius=91, color=(50, 225, 30))
line_top1 = shapes.Line(230, 295, 570, 295, width=11.5, color=(200, 20, 20))
line_bottom1 = shapes.Line(230, 123, 570, 123, width=11.5, color=(200, 20, 20))
line_top2 = shapes.Line(190, 395, 610, 395, width=11.5, color=(200, 20, 20))
line_bottom2 = shapes.Line(190, 14, 610, 13.7, width=11.5, color=(200, 20, 20))

# Define arcs for the rounded corners
RADIUS = 185
CENTER_X = 195
CENTER_Y = 210
start_angle = np.pi / 2
arc_1 = shapes.Arc(CENTER_X, CENTER_Y, radius=RADIUS, start_angle=start_angle, angle=np.pi, color=(255, 0, 0), segments=100, thickness=11.5)

RADIUS = 185
CENTER_X = 600
CENTER_Y = 210
start_angle = 3 * np.pi / 2
arc_2 = shapes.Arc(CENTER_X, CENTER_Y, radius=RADIUS, start_angle=start_angle, angle=np.pi, color=(255, 0, 0), segments=100, thickness=11.5)

# Add all obstacles to a list
obstacles = [circle1_left, circle1_right, line_top1, line_bottom1, line_top2, line_bottom2, arc_1, arc_2]

# --- RL Agent Class ---
class RLAgent:
    def __init__(self, x, y, size=10, speed=2, epsilon=1.0, alpha=0.1, gamma=0.9):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.q_table = {}
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.shape = shapes.Circle(self.x, self.y, self.size, color=(0, 0, 255))

    def get_state(self, obstacles):
        state = []
        for obstacle in obstacles:
            if isinstance(obstacle, shapes.Circle):
                dist = sqrt((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2)
                state.append(dist)
            elif isinstance(obstacle, shapes.Line):
                line_start = np.array([obstacle.x, obstacle.y])
                line_end = np.array([obstacle.x2, obstacle.y2])
                point = np.array([self.x, self.y])
                distance = np.linalg.norm(np.cross(line_end-line_start, line_start-point)) / np.linalg.norm(line_end-line_start)
                state.append(distance)
            elif isinstance(obstacle, shapes.Arc):
                center_x, center_y = obstacle.x, obstacle.y
                dist = sqrt((self.x - center_x) ** 2 + (self.y - center_y) ** 2) - obstacle.radius
                state.append(dist)
        return tuple(state)

    def choose_action(self, state):
        actions = ['left', 'right', 'up', 'down']
        if random.random() < self.epsilon:
            return random.choice(actions)
        if state in self.q_table:
            return max(self.q_table[state], key=self.q_table[state].get)
        return random.choice(actions)

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0 for a in ['left', 'right', 'up', 'down']}
        if next_state not in self.q_table:
            self.q_table[next_state] = {a: 0 for a in ['left', 'right', 'up', 'down']}
        old_value = self.q_table[state][action]
        future_reward = max(self.q_table[next_state].values())
        self.q_table[state][action] = old_value + self.alpha * (reward + self.gamma * future_reward - old_value)

    def move(self, action, obstacles):
        original_x, original_y = self.x, self.y
        if action == 'left':
            self.x -= self.speed
        elif action == 'right':
            self.x += self.speed
        elif action == 'up':
            self.y += self.speed
        elif action == 'down':
            self.y -= self.speed
        collision = self.check_collision(obstacles)
        if collision:
            self.x, self.y = original_x, original_y
        self.shape.x = self.x
        self.shape.y = self.y
        return collision

    def check_collision(self, obstacles):
        for obstacle in obstacles:
            if isinstance(obstacle, shapes.Circle):
                distance = sqrt((self.x - obstacle.x) ** 2 + (self.y - obstacle.y) ** 2)
                if distance < self.size + obstacle.radius:
                    return True
            elif isinstance(obstacle, shapes.Line):
                line_start = (obstacle.x, obstacle.y)
                line_end = (obstacle.x2, obstacle.y2)
                min_x = min(line_start[0], line_end[0]) - self.size
                max_x = max(line_start[0], line_end[0]) + self.size
                min_y = min(line_start[1], line_end[1]) - self.size
                max_y = max(line_start[1], line_end[1]) + self.size
                if min_x <= self.x <= max_x and min_y <= self.y <= max_y:
                    return True
            elif isinstance(obstacle, shapes.Arc):
                center_x, center_y = obstacle.x, obstacle.y
                distance = sqrt((self.x - center_x) ** 2 + (self.y - center_y) ** 2)
                if abs(distance - obstacle.radius) <= self.size:
                    return True
        return False

    def draw(self):
        self.shape.draw()


# --- RL Step Function ---
def step(agent, obstacles):
    state = agent.get_state(obstacles)
    action = agent.choose_action(state)
    collision = agent.move(action, obstacles)
    reward = -1 if collision else 1
    next_state = agent.get_state(obstacles)
    agent.update_q_table(state, action, reward, next_state)
    agent.epsilon = max(0.1, agent.epsilon * 0.99)


# Create an RL agent instance
agent = RLAgent(x=70, y=220)

# Schedule updates
def update(dt):
    step(agent, obstacles)

pyglet.clock.schedule_interval(update, 1/60.0)

# Drawing function
@window.event
def on_draw():
    track_sprite.draw()
    for obstacle in obstacles:
        obstacle.draw()
    agent.draw()


# Run the app
pyglet.app.run()
