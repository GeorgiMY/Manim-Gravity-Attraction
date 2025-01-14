from manim import *
import numpy as np
from ball import Ball

class GravitationalAttraction(Scene):
    def calculate_gravitational_force(self, ball1, ball2):
            r = ball1.position - ball2.position
            r_mag = np.linalg.norm(r)
            
            # Avoid division by zero and limit very close interactions
            if r_mag < 0.1:
                return np.zeros(3)
                
            # Calculate gravitational force
            force_mag = self.G * ball1.mass * ball2.mass / (r_mag ** 2)
            return -force_mag * r / r_mag
        
    def update_simulation(self, dt):
        # Calculate and apply forces
        for i, ball1 in enumerate(self.balls):
            force = np.zeros(3)
            
            # Calculate total force on ball1 from all other balls
            for j, ball2 in enumerate(self.balls):
                if i != j:
                    force += self.calculate_gravitational_force(ball1, ball2)

                    # Make them not be able to collide with each other
                    r = ball1.position - ball2.position
                    # ballOnePosition + ballOneradius >= ballTwoposition2 - ballTworadius2
                    if np.linalg.norm(r) <= ball1.circle.radius + ball2.circle.radius:
                        ball1.velocity *= -1
                        ball2.velocity *= -1
                        ball1.position += ball1.velocity * dt
                        ball2.position += ball2.velocity * dt
                        ball1.circle.move_to(ball1.position)
                        ball2.circle.move_to(ball2.position)
            
            # Update velocity based on force
            ball1.apply_force(force, dt)
            
            # Update position
            ball1.update_position(dt)
            
            # Handle boundary collisions
            ball1.handle_boundary_collision()

    def construct(self):
        # Constants
        self.G = 1  # Gravitational constant (scaled for visualization)
        self.dt = 0.01  # Time step

        self.n_balls = 5
        self.balls = []
        self.colors = [RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE]  # Available colors
        
        for i in range(self.n_balls):
            # Can't have 2 balls at the same position
            position = np.array([
                    np.random.uniform(-6, 6),
                    np.random.uniform(-6, 6),
                    0
                ])
            mass = np.random.uniform(0.5, 3)
            color = self.colors[i % len(self.colors)]  # Cycle through colors

            while any(np.linalg.norm(ball.position - position) < mass * 0.1 for ball in self.balls):
                position = np.array([
                    np.random.uniform(-6, 6),
                    np.random.uniform(-6, 6),
                    0
                ])
            
            self.balls.append(Ball(position, mass, color))

        # Add balls to scene
        circles = VGroup(*[ball.circle for ball in self.balls])
        self.add(circles)
        
        # Add update function
        circles.add_updater(lambda m, dt: self.update_simulation(dt))

        # Run the animation
        self.wait(20)
