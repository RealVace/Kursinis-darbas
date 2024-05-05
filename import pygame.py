import pygame  # Import the Pygame library for game development
import random  # Import the random module for generating random numbers
import os # Import library for operating system interaction

class HighscoreTracker:
    """Singleton class to manage and track the highscore."""
    _instance = None

    def __new__(cls):
        """Create a new instance if it doesn't exist, cls refers to the class itself."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.highscore = cls._instance.load_highscore()
        return cls._instance

    def load_highscore(self):
        """Load the highscore from a file, or return 0 if file not found."""
        try:
            with open("highscore.txt", "r") as file: # read mode (ensure the file is closed after reading)
                return int(file.read())
        except FileNotFoundError:
            return 0

    def save_highscore(self):
        """Save the current highscore to a file."""
        with open("highscore.txt", "w") as file: # write mode (ensure the file is closed after writing)
            file.write(str(self.highscore))

    def update_highscore(self, score):
        """Update the highscore if the given score is higher."""
        if score > self.highscore:
            self.highscore = score
            self.save_highscore()

    def get_highscore(self):
        """Return the current highscore."""
        return self.highscore

class ScoreDisplay:
    """Class to display the current score and highscore on the screen."""
    def __init__(self, font, width, height):
        self.font = font  # Initialize the font for rendering text
        self.width = width  # Set the width of the display area
        self.height = height  # Set the height of the display area
        self.current_score = 0  # Initialize the current score to 0
        self.highscore = 0  # Initialize the highscore to 0

    def update_score(self, current_score, highscore):
        """Update the current score and highscore."""
        self.current_score = current_score  # Update the current score
        self.highscore = highscore  # Update the highscore

    def draw(self, screen):
        """Draw the current score and highscore on the screen."""
        current_score_text = self.font.render(f"Score: {self.current_score}", True, (0, 0, 0))  # Render the current score text
        highscore_text = self.font.render(f"Highscore: {self.highscore}", True, (0, 0, 0))  # Render the highscore text
        screen.blit(current_score_text, (10, 10))  # Draw the current score text on the top left side of the screen
        screen.blit(highscore_text, (self.width - highscore_text.get_width() - 10, 10))  # Draw the highscore text on the top right side of the screen

class GameWindow:
    """Class representing the game window and main game logic."""
    def __init__(self, width, height):
        
        self.width = width  # Set the width of the game window
        self.height = height  # Set the height of the game window
        self.grid_size = 20  # Set the size of the grid squares
        self.grid_color = (173, 216, 230)  # Set the color of the grid lines
        self.background_color = (255, 255, 255)  # Set the background color

        self.snake = Snake((self.width // 2, self.height // 2), self.grid_size)  # Create the snake object
        self.apples = [GoldenApple(self.grid_size, self.width, self.height),  # Create a list of apple objects
                       AquaApple(self.grid_size, self.width, self.height),
                       RedApple(self.grid_size, self.width, self.height)]
        
        self.score_display = ScoreDisplay(pygame.font.SysFont(None, 36), width, height)  # Create the score display object
        self.current_score = 0  # Initialize the current score to 0
        self.highscore_tracker = HighscoreTracker()  # Create the highscore tracker object
        self.highscore = self.highscore_tracker.get_highscore()  # Get the current highscore

        self.color_changer = ColorChanger()  # Create the color changer object
        self.background_changer = BackgroundColorChanger()  # Create the background color changer object

        self.screen = pygame.display.set_mode((width, height))  # Create the game window
        pygame.display.set_caption("Snake Game")  # Set the title of the game window
        self.menu_text = self.score_display.font.render("Press any key to start", True, (0, 0, 0))  # Render the menu text
        self.game_over_text = self.score_display.font.render("Game Over! Press R to restart", True, (0, 0, 0))  # Render the game over text

        self.game_over = False  # Flag to indicate if the game is over
        self.playing = False  # Flag to indicate if the game is currently being played

        self.grace_period = 500  # Set the grace period (0.5-second grace period in milliseconds)
        self.game_start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        self.clock = pygame.time.Clock()  # Create a clock object to control the frame rate
   
    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN :
                if not self.playing:
                    self.playing = True
                elif self.game_over:
                    if event.key == pygame.K_r:
                        self.restart_game()
                else:
                    if event.key == pygame.K_UP  :
                        self.snake.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.snake.move_down()
                    elif event.key == pygame.K_LEFT:
                        self.snake.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.snake.move_right()

    def start_menu(self):
        """Display the start menu."""
        self.screen.fill(self.background_color)
        self.screen.blit(self.menu_text, (self.width // 2 - self.menu_text.get_width() // 2, self.height // 2 - self.menu_text.get_height() // 2))
        pygame.display.flip()

    def game_over_screen(self):
        """Display the game over screen."""
        self.screen.fill((255, 255, 255))  # Fill screen with white background
        self.screen.blit(self.game_over_text, (self.width // 2 - self.game_over_text.get_width() // 2, self.height // 2 - self.game_over_text.get_height() // 2))
        pygame.display.flip()

    def restart_game(self):
        """Restart the game."""
        self.snake.reset((self.width // 2, self.height // 2)) # Reset snake to its initial position
        for apple in self.apples:
            apple.generate_new_position(self.snake.body) # Regenerate apple positions
        self.game_over = False
        self.current_score = 0
        self.color_changer.reset() # Reset snake color changer
        self.background_changer.reset()  # Reset background color changer
        self.background_color = (255, 255, 255)  # Reset background color to white
        self.grace_period = 500  # Reset grace period to 0.5 seconds
        

    def draw_grid(self):
            """Draw the grid lines on the game window."""
            for x in range(0, self.width, self.grid_size):
                pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height))  # Draw vertical grid lines
            for y in range(0, self.height, self.grid_size):
                pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y))  # Draw horizontal grid lines

    def run_game(self):
        """Run the game loop."""

        self.clock.tick(10) # Frame rate

        """Checks what game window we are in."""
        while True:
            if not self.playing:
                self.handle_events()
                self.start_menu()
            elif self.game_over:
                self.handle_events()
                self.game_over_screen()
            else:
                self.handle_events()
                
                if pygame.time.get_ticks() - self.game_start_time > self.grace_period: #Checks if the grace period is over.
                    
                    """Handles apple eating and score tracking."""
                    for apple in self.apples:
                        if self.snake.body[0] == apple.position:
                            self.snake.grow()
                            self.current_score += 1
                            self.highscore_tracker.update_highscore(self.current_score)
                            self.highscore = self.highscore_tracker.get_highscore()
                            apple.generate_new_position(self.snake.body) # Regenerate apple
                            self.color_changer.change_color(self.snake) # Change snake color
                            self.background_changer.change_background_color(apple.color)  # Change background color
                    
                    """Handles drawing."""
                    self.screen.fill(self.background_changer.get_background_color())  # Fill the background with appropriate color
                    self.draw_grid()
                    self.snake.move()
                    self.snake.draw(self.screen)
                    for apple in self.apples:
                        apple.draw(self.screen)
                    
                    """Handles score display."""
                    self.score_display.update_score(self.current_score, self.highscore)
                    self.score_display.draw(self.screen)
                    
                    pygame.display.flip() # Update display window
                    self.clock.tick(10) # Frame rate

                    if self.snake.collide_with_border(self.width, self.height) or self.snake.collide_with_self():
                        self.game_over = True

class Snake:
    """Class representing the snake
    start pos, is the x axis
    start pos, 1 is the y axis."""
    def __init__(self, start_pos, segment_size):
        self.body = [start_pos, (start_pos[0] - segment_size, start_pos[1]), (start_pos[0] - 2 * segment_size, start_pos[1]), (start_pos[0] - 3 * segment_size, start_pos[1])]
        self.direction = (1, 0)
        self.segment_size = segment_size
        self.color = (0, 120, 0)
        self.next_direction = None

    def move_up(self):
        """Change the snake's direction to up."""
        self.change_direction((0, -1))

    def move_down(self):
        """Change the snake's direction to down."""
        self.change_direction((0, 1))

    def move_left(self):
        """Change the snake's direction to left."""
        self.change_direction((-1, 0))

    def move_right(self):
        """Change the snake's direction to right."""
        self.change_direction((1, 0))

    def change_direction(self, direction):
        """Change the snake's direction if it's not the opposite direction."""
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction

    def move(self):
        """Move the snake by one step in its current direction
        direction 0 is the x axis, 1 is the y axis
        body [segment][x/y]."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        # Calculate the new position of the snake's head based on the current direction and segment size
        new_head = (self.body[0][0] + self.direction[0] * self.segment_size, 
                    self.body[0][1] + self.direction[1] * self.segment_size)
        # Update the snake's body with the new position of the head and remove the last segment
        self.body = [new_head] + self.body[:-1]
        
    def grow(self):
        """Make the snake grow longer by one segment."""
        tail = self.body[-1]
        self.body.append(tail)

    def draw(self, screen):
        """Draw the snake on the screen
        segment[x/y] represents each segment in body."""
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0], segment[1], self.segment_size, self.segment_size))

    def collide_with_border(self, width, height):
        """Check if the snake collides with the game borders
        body [segment][x/y]."""
        return self.body[0][0] < 0 or self.body[0][0] >= width or self.body[0][1] < 0 or self.body[0][1] >= height

    def collide_with_self(self):
        """Check if the snake collides with itself."""
        return any(segment == self.body[0] for segment in self.body[1:])

    def reset(self, start_pos):
        """Reset the snake to its initial state."""
        self.body = [start_pos, (start_pos[0] - self.segment_size, start_pos[1]), (start_pos[0] - 2 * self.segment_size, start_pos[1]), (start_pos[0] - 3 * self.segment_size, start_pos[1])]
        self.color = (0, 120, 0)

class Apple:
    """Base class representing an apple."""
    def __init__(self, size, screen_width, screen_height):
        self.size = size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.position = self.generate_position()

    def generate_position(self):
        """Generate a random position for the apple."""
        x = random.randint(0, (self.screen_width - self.size) // self.size) * self.size
        y = random.randint(0, (self.screen_height - self.size) // self.size) * self.size
        return (x, y)

    def generate_new_position(self, snake_body):
        """Generate a new position for the apple until it doesn't collide with the snake."""
        while True:
            new_position = self.generate_position()
            if new_position not in snake_body:
                self.position = new_position
                break

    def draw(self, screen):
        """Draw the apple on the screen."""
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size, self.size))

class GoldenApple(Apple):
    """Class representing a golden apple."""
    def __init__(self, size, screen_width, screen_height):
        super().__init__(size, screen_width, screen_height) #calls the parent class instructor
        self.color = (255, 215, 0)  # Golden color

class AquaApple(Apple):
    """Class representing an aqua-colored apple."""
    def __init__(self, size, screen_width, screen_height):
        super().__init__(size, screen_width, screen_height) #calls the parent class instructor
        self.color = (0, 255, 255)  # Aqua color

class RedApple(Apple):
    """Class representing a red apple."""
    def __init__(self, size, screen_width, screen_height):
        super().__init__(size, screen_width, screen_height) #calls the parent class instructor
        self.color = (255, 0, 0)  # Red color

class ColorChanger:
    """Class to change the snake's color."""
    def __init__(self):
        self.colors = [
            (0, 120, 0),  # Green
            (0, 0, 120),  # Blue
            (120, 0, 0)   # Red
        ]
        self.transition_step = 0.1
        self.transition_speed = 0.25
        self.current_color_index = 0
        self.current_transition = 0

class ColorChanger:
    """Class to change the snake's color."""
    def __init__(self):
        self.colors = [
            (0, 120, 0),  # Green
            (0, 0, 120),  # Blue
            (120, 0, 0)   # Red
        ]
        # Step size for each color transition
        self.transition_step = 0.25
        # Index of the current color in the colors list
        self.current_color_index = 0
        # Current progress of the color transition
        self.current_transition = 0

    def change_color(self, snake):
        """Change the snake's color."""

        # Check if the current color transition is complete between RGB
        if self.current_transition >= 1:
            # Reset transition progress
            self.current_transition = 0
            # Move to the next color in the list, looping back to the beginning if necessary
            self.current_color_index = (self.current_color_index + 1) % len(self.colors) # len=length of array

        # Calculate the index of the next color in the list
        next_color_index = (self.current_color_index + 1) % len(self.colors) # len=length of array
        # Retrieve the current color from the colors list
        current_color = self.colors[self.current_color_index]
        # Retrieve the next color from the colors list
        next_color = self.colors[next_color_index]

        # Calculate the interpolated color between the current and next colors
        new_color = self.interpolate_color(current_color, next_color, self.current_transition)
        # Set the snake's color to the interpolated color
        snake.color = new_color

        # Increment the transition progress
        self.current_transition += self.transition_step

    def interpolate_color(self, color1, color2, t): # current=color1, next=color2, transition progress=t
        """Interpolate between two colors."""
        # Interpolate each component of the colors using the current transition progress
        return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2)) # Zip in this case means adding two tuple individual values into a single tuple for each value

    def reset(self):
        """Reset color changer state."""
        self.current_color_index = 0
        self.current_transition = 0

class BackgroundColorChanger:
    """Class to change the background color based on the apple color."""
    def __init__(self):
        self.initial_color = (255, 255, 255)  # Initial background color (white)
        self.background_color = self.initial_color
        self.lighten_value = 225  # Value to increase the RGB components by

    def change_background_color(self, apple_color):
        """Change the background color based on the apple color by generating a new tuple based on apple array, the 255 is there to ensure a value doesnt exceed 255."""
        new_background_color = tuple(min(255, component + self.lighten_value) for component in apple_color) # component = 1 value of apple (RGB)
        self.background_color = new_background_color

    def get_background_color(self):
        """Get the current background color."""
        return self.background_color
    
    def reset(self):
        """Reset background color to initial color."""
        self.background_color = self.initial_color  # Reset to initial background color

# Initialize Pygame
pygame.init()

#locate where the script is at and change it
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# Create a game window and run the game loop
game_window = GameWindow(520, 520)
game_window.run_game()
