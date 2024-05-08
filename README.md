# Snake Game Report

## 1. Introduction

### Goal of the Coursework

The goal of this coursework is to develop a classic Snake Game using Python.

### Description of the Topic

The Snake Game is a simple yet engaging arcade game where the player controls a snake that moves around the screen, eating apples to grow longer. The objective is to achieve the highest score possible without colliding with the snake's own body or the game window boundaries.

#### What is your application?

The Snake Game application allows users to play snake on the computer. Players control the snake's movement using arrow keys and the aim is to eat apples to grow longer and increase their score.

#### How to run the program?

1. Ensure Python is installed on your system.
2. Install the Pygame library using `pip install pygame`.
3. Navigate to `import pygame.py`.
4. Run the script.

#### How to use the program?

Upon running the program, players are presented with the game window. They can control the snake's movement using the arrow keys. The goal is to eat as many apples as possible to grow longer and increase the score. Players must avoid colliding with the snake's own body or the game window boundaries. If the game ends, players can press the "R" key to restart.

## 2. Body/Analysis

### Object-Oriented Programming (OOP) Pillars

1. **Encapsulation**

   - **Description**: Encapsulation is the bundling of data and methods that operate on the data into a single unit or class. It allows for the hiding of internal state and only exposing necessary functionalities to the outside world, thus promoting information hiding and reducing system complexity.
  
    `class Snake:
   def __init__(self, start_pos, segment_size):
   self.body = [start_pos, (start_pos[0] - segment_size, start_pos[1]), ...]
   ...`
    
    `def move_up(self):
   self.change_direction((0, -1))`

    `class Apple:
   def __init__(self, size, screen_width, screen_height):
   self.size = size
   self.screen_width = screen_width
   self.screen_height = screen_height
   self.position = self.generate_position()
   ...`

3. **Inheritance**

   - **Description**: Inheritance is the mechanism by which a class can inherit attributes and methods from another class, called the parent class. It promotes code reusability and allows for creating specialized classes that inherit common functionalities from the parent class.
     
    `class GoldenApple(Apple):
    def __init__(self, size, screen_width, screen_height):
        super().__init__(size, screen_width, screen_height)
        self.color = (255, 215, 0)`

    `class AquaApple(Apple):
    def __init__(self, size, screen_width, screen_height):
        super().__init__(size, screen_width, screen_height)
        self.color = (0, 255, 255)`

4. **Polymorphism**

   - **Description**: Polymorphism allows objects of different classes to be treated as objects of a common superclass. It enables methods to behave differently based on the object they are invoked on, promoting flexibility and code extensibility.
  
    `class Apple:
   ...
   def draw(self, screen):
   pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size, self.size))`

    `class GoldenApple(Apple):
   ...
   def draw(self, screen):
   pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], self.size, self.size))`

6. **Abstraction**

   - **Description**: Abstraction is the concept of hiding complex implementation details and showing only the necessary features of an object. It allows for focusing on essential attributes and behaviors while hiding irrelevant details, thereby simplifying the system's design and making it easier to understand and use.
  
   `class Snake:
   ...
   def move_up(self):
   self.change_direction((0, -1))`

### Design Patterns

- **Singleton Pattern**: The Singleton Pattern ensures that a class has only one instance and provides a global point of access to that instance. It is useful when exactly one object is needed to coordinate actions across the system, such as managing shared resources or tracking global state.

   `class HighscoreTracker:
  _instance = None
  ...
  @classmethod
  def __new__(cls):
  if cls._instance is None:
  cls._instance = super().__new__(cls)
  ...
  return cls._instance`

### Reading from File & Writing to File

Reading from a file and writing to a file is implemented in the HighscoreTracker class when we need to save and load the user's high score.

`with open("highscore.txt", "r") as file:
highscore = int(file.read())`

`with open("highscore.txt", "w") as file:
file.write(str(highscore))`

## 3. Results and Summary

### Results

- The implementation of the Snake Game effectively utilizes Object-Oriented Programming principles, including encapsulation, inheritance, polymorphism, and abstraction, resulting in a code that is easy to understand and quite flexible.
- The planned incorporation of a second design pattern was not implemented within the current scope of the project.
- The adoption of the Singleton Pattern ensures the unique instantiation of the HighscoreTracker class, facilitating seamless high score management across different game sessions.
- The Snake Game possesses significant potential for the addition of new features, as the current codebase is quite flexible and easy to update.
- Despite the challenges faced during implementation, the code structure of the Snake Game remains clean and well-organized.

### Conclusions

- The Snake Game project has successfully demonstrated the application of Object-Oriented Programming principles. Despite encountering challenges in implementing certain features, the project has achieved its primary goal of developing a functional and enjoyable game experience.
- The program effectively implements core OOP concepts such as encapsulation, inheritance, polymorphism, and abstraction, making the code quite flexible and easy to understand for people.
- Through some bug testing, the game shows no runtime errors or unexpected behaviors.
- The program's documentation and code comments provide clear and comprehensive explanations of its functionality, making the code easy to understand.

### Future Prospects

- The Snake Game possesses significant potential for further development and expansion. Future prospects include:
  - Introducing power-ups and obstacles to add complexity to the gameplay.
  - Integrating multiplayer to allow players to compete against each other.
  - Adding customizable features such as snake skins, background themes, and sound effects to enhance player experience.
