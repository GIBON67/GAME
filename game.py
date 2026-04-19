import pygame, random

pygame.init()
SIZE, TILE = 400, 18
screen = pygame.display.set_mode((SIZE, SIZE))
clock = pygame.time.Clock()


class Segment(pygame.sprite.Sprite):
    def __init__(self, x, y, color='green'):
        super().__init__()
        self.image = pygame.Surface((TILE, TILE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))

class Snake:
    def __init__(self):
        self.x, self.y = 200, 200
        self.vel, self.vx, self.vy = 4, 0, 0
        self.history = [] 
        self.length = 1
        self.step = 5
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

    def draw(self, surf):
        self.group.draw(surf) 

food_sprite = Segment(random.randint(0, 380), random.randint(0, 380), 'red')
food_group = pygame.sprite.GroupSingle(food_sprite)

snake = Snake()

while True:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:    snake.vx, snake.vy = 0, -snake.vel
            if event.key == pygame.K_DOWN:  snake.vx, snake.vy = 0, snake.vel
            if event.key == pygame.K_LEFT:  snake.vx, snake.vy = -snake.vel, 0
            if event.key == pygame.K_RIGHT: snake.vx, snake.vy = snake.vel, 0

    snake.update()

    segments = snake.group.sprites()
  
    head_segment = segments[0] 

    hits = pygame.sprite.spritecollide(head_segment, food_group, False)
    if hits:
        snake.length += 1
        food_group.sprite.rect.topleft = (random.randint(0, 380), random.randint(0, 380))


    
    if not screen.get_rect().collidepoint(snake.x, snake.y):
        break

    food_group.draw(screen)
    snake.draw(screen)

    pygame.display.flip()
    clock.tick(60)
