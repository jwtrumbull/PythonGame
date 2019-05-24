import pygame
import random
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PURPLE = (150, 0, 240)
BLUE = (0, 0, 255)
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
 
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
    controls. """
 
    # Constructor function
    def __init__(self, x, y):
        # Call the parent's constructor
        super().__init__()
 
        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
        # Set speed vector
        self.change_x = 0
        self.change_y = 0
        self.walls = None
 
    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y
 
    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x
 
        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            # If we are moving right, set our right side to the left side of
            # the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom
 
 
class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """
    def __init__(self, x, y, width, height):
        """ Constructor for the wall that the player can run into. """
        # Call the parent's constructor
        super().__init__()
 
        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
 
        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
 
class Block(pygame.sprite.Sprite):
     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__() 
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.ellipse(self.image,color, [0,0,width,height])
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

block_list = pygame.sprite.Group()

fontname = pygame.font.match_font('comicsans')

def scoreboard(score):
    font = pygame.font.Font(fontname, 34)
    text = font.render("Score: {}".format(score), True,(255,255,255))
    screen.blit(text, [0,0])
 
# Call this function so the Pygame library can initialize itself
pygame.init()
 
# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
 
# Set the title of the window
pygame.display.set_caption('Test')
 
# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()
 
# Make the walls. (x_pos, y_pos, width, height)
wall_list = pygame.sprite.Group()
 
wall = Wall(0, 0, 10, 600)
wall_list.add(wall)
all_sprite_list.add(wall)
 
wall = Wall(0, 0, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(790, 0, 10, 790)
wall_list.add(wall)
all_sprite_list.add(wall)

wall = Wall(0, 590, 790, 10)
wall_list.add(wall)
all_sprite_list.add(wall)

for i in range(8):
    for j in range(6):
        wall = Wall(i*100, j*100, 10, 10)
        wall_list.add(wall)
        all_sprite_list.add(wall)

for i in range(20):
    # This represents a block
    block = Block((255,255,0), 20, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(20, SCREEN_WIDTH-40)
    block.rect.y = random.randrange(20, SCREEN_HEIGHT-40)
     
    # Add the block to the list of objects
    block_list.add(block)
    all_sprite_list.add(block)  
 
# Create the player paddle object
player = Player(50, 50)
player.walls = wall_list
 
all_sprite_list.add(player)
 
clock = pygame.time.Clock()
 
done = False
score = 0
 
while not done:
 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, 3)
 
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(3, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-3, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

    # See if the player block has collided with anything.
    blocks_hit_list = pygame.sprite.spritecollide(player, block_list, True)  
    

    # Check the list of collisions.
    for block in blocks_hit_list:
        score +=1
        print( score )

    all_sprite_list.update()
 
    screen.fill(BLACK)
 
    all_sprite_list.draw(screen)
 
    scoreboard(score)

    pygame.display.update()
 
    clock.tick(60)
 
pygame.quit()