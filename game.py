import pygame, random

pygame.init()
FPS = 10
SIZE = 400
TILE = 18
COLOR = (40, 40, 40)
screen = pygame.display.set_mode((SIZE, SIZE))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 30)
text = font.render("You Lose", True, (255, 255, 255))

def draw_grid():
    for x in range(0, SIZE, TILE):
        pygame.draw.line(screen, COLOR, (x, 0), (x, SIZE))
    for y in range(0, SIZE, TILE):
        pygame.draw.line(screen, COLOR, (0, y), (SIZE, y))





class Segment(pygame.sprite.Sprite):
    def __init__(self, x, y, color='green'):
        super().__init__()
        self.image = pygame.Surface((TILE, TILE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Snake:
    def __init__(self):
        self.x, self.y = 200, 200
        self.vel, self.vx, self.vy = 18, 0, 0
        self.history = [(self.x, self.y)] 
        self.length = 1
        self.step = 1
        self.group = pygame.sprite.Group() 

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.history.append((self.x, self.y))


        if len(self.history) > self.length * self.step:
            self.history.pop(0)

       
        self.group.empty() 
        for i in range(len(self.history) - 1, -1, -self.step):
            
            seg = Segment(*self.history[i])
            self.group.add(seg)

    def check_position(self):

        if len(self.history) < 2:
            return False
        
        head = self.history[0]
        for i in range(self.step, len(self.history), self.step):
            if i < len(self.history) and self.history[i] == head:
                return True
        return False

    def draw(self, surf):
        self.group.draw(surf) 



def get_random_food():
    max_cells = SIZE // TILE
    x = random.randint(0, max_cells - 1) * TILE
    y = random.randint(0, max_cells - 1) * TILE
    return x, y

while True:
    food_x, food_y = get_random_food()
    if (food_x, food_y) != (200, 200):  # Не на голове змеи
        break



food_x, food_y = get_random_food()
food_sprite = Segment(food_x, food_y, 'red')
food_group = pygame.sprite.GroupSingle(food_sprite)

snake = Snake()
game = True

while game == True:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.vx, snake.vy = 0, -snake.vel
            if event.key == pygame.K_DOWN:
                snake.vx, snake.vy = 0, snake.vel
            if event.key == pygame.K_LEFT:
                snake.vx, snake.vy = -snake.vel, 0
            if event.key == pygame.K_RIGHT:
                snake.vx, snake.vy = snake.vel, 0

    snake.update()
    segments = snake.group.sprites()
    head_segment = segments[0] 
    draw_grid()

    hits = pygame.sprite.spritecollide(head_segment, food_group, False)
    if hits:
        snake.length += 1
        food_sprite = Segment(*get_random_food(), 'red')
        food_group = pygame.sprite.GroupSingle(food_sprite)



    
    if not screen.get_rect().collidepoint(snake.x, snake.y):
        screen.fill('red')
        screen.blit(text, (150, 170))
        FPS = 0

    if snake.check_position():
        screen.fill('red')
        screen.blit(text, (150, 170))
        FPS = 0


    food_group.draw(screen)
    snake.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)