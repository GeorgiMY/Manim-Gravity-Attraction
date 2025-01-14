from manim import *

class Ball:
    def __init__(self, position, mass, color):
        self.position = np.array(position)
        self.velocity = np.zeros(3)
        self.mass = mass
        self.color = color
        self.circle = Circle(
            radius=0.1 * mass,
            color=color,
            fill_opacity=0.95,
            stroke_width=2
        )
        self.circle.move_to(position)

    # a = F / m
    # v = v0 + a * dt
    def apply_force(self, force, dt):
        acceleration = force / self.mass
        self.velocity += acceleration * dt
    
    # x = x0 + v * dt
    def update_position(self, dt):
        self.position += self.velocity * dt
        self.circle.move_to(self.position)
    
    # Collision with walls
    def handle_boundary_collision(self):
        # Bounce off walls
        if abs(self.position[0]) > 6:
            self.velocity[0] *= -0.8
            # Ensure ball stays in bounds
            self.position[0] = np.sign(self.position[0]) * 6
            
        # Bounce off top/bottom
        if abs(self.position[1]) > 3.5:
            self.velocity[1] *= -0.8
            self.position[1] = np.sign(self.position[1]) * 3.5
