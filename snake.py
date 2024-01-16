import pygame,sys,random
from pygame.math import Vector2

class FRUIT():
    def __init__(self):
        self.fruit_lst=["apple","mango","bananas","grapes","pineapple","watermelon","orange"]
        self.randomize()

    def draw_fruit(self):
        fruit_rect=pygame.Rect(int(self.pos.x*cell_size),int(self.pos.y*cell_size),cell_size,cell_size)
        # pygame.draw.rect(screen,(126,166,114),fruit_rect)
        screen.blit(self.fruit_image,fruit_rect)

    def randomize(self):
        self.x=random.randint(0,cell_number-1)
        self.y=random.randint(0,cell_number-1)
        self.pos=Vector2(self.x,self.y)
        self.fruit_image=pygame.image.load(f"Assets/{random.choice(self.fruit_lst)}.png").convert_alpha()

class SNAKE():
    def __init__(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(0,0)
        self.new_block=False

        self.head_up=pygame.image.load('Assets/head_up.png').convert_alpha()
        self.head_down=pygame.image.load('Assets/head_down.png').convert_alpha()
        self.head_right=pygame.image.load('Assets/head_right.png').convert_alpha()
        self.head_left=pygame.image.load('Assets/head_left.png').convert_alpha()

        self.tail_up=pygame.image.load('Assets/tail_up.png').convert_alpha()
        self.tail_down=pygame.image.load('Assets/tail_down.png').convert_alpha()
        self.tail_right=pygame.image.load('Assets/tail_right.png').convert_alpha()
        self.tail_left=pygame.image.load('Assets/tail_left.png').convert_alpha()
        
        self.body_vertical=pygame.image.load('Assets/body_vertical.png').convert_alpha()
        self.body_horizontal=pygame.image.load('Assets/body_horizontal.png').convert_alpha()

        self.body_tr=pygame.image.load('Assets/body_tr.png').convert_alpha()
        self.body_tl=pygame.image.load('Assets/body_tl.png').convert_alpha()
        self.body_br=pygame.image.load('Assets/body_br.png').convert_alpha()
        self.body_bl=pygame.image.load('Assets/body_bl.png').convert_alpha()

        # sounds
        self.crunch_sound=pygame.mixer.Sound('Sound/crunch.wav')
        self.move_sound=pygame.mixer.Sound('Sound/move.wav')
        self.collision_sound=pygame.mixer.Sound('Sound/collision.wav')
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            xpos=int(block.x*cell_size)
            ypos=int(block.y*cell_size)
            block_rect=pygame.Rect(xpos,ypos,cell_size,cell_size)

            if(index==0):
                screen.blit(self.head,block_rect)
            elif index==len(self.body)-1:
                screen.blit(self.tail,block_rect)
            else:
                previous_block=self.body[index+1]-block
                next_block=self.body[index-1]-block
                if(previous_block.x==next_block.x):
                    screen.blit(self.body_vertical,block_rect)
                elif(previous_block.y==next_block.y):
                    screen.blit(self.body_horizontal,block_rect)
                else:
                    if previous_block.x==-1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==-1:
                        screen.blit(self.body_tl,block_rect)

                    elif previous_block.x==-1 and next_block.y==1 or previous_block.y==1 and next_block.x==-1:
                        screen.blit(self.body_bl,block_rect)

                    elif previous_block.x==1 and next_block.y==-1 or previous_block.y==-1 and next_block.x==1:
                        screen.blit(self.body_tr,block_rect)

                    elif previous_block.x==1 and next_block.y==1 or previous_block.y==1 and next_block.x==1:
                        screen.blit(self.body_br,block_rect)

    def update_head_graphics(self):
        head_relation=self.body[1]-self.body[0]
        if head_relation==Vector2(1,0):
            self.head=self.head_left
        elif head_relation==Vector2(-1,0):
            self.head=self.head_right
        elif head_relation==Vector2(0,1):
            self.head=self.head_up
        elif head_relation==Vector2(0,-1):
            self.head=self.head_down

    def update_tail_graphics(self):
        tail_relation=self.body[-2]-self.body[-1]
        if tail_relation==Vector2(1,0):
            self.tail=self.tail_left
        elif tail_relation==Vector2(-1,0):
            self.tail=self.tail_right
        elif tail_relation==Vector2(0,1):
            self.tail=self.tail_up
        elif tail_relation==Vector2(0,-1):
            self.tail=self.tail_down             

    def move_snake(self):
        if self.new_block==True:
            body_copy=self.body[:]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]
            self.new_block=False
            
        else:
            body_copy=self.body[:-1]
            body_copy.insert(0,body_copy[0]+self.direction)
            self.body=body_copy[:]

    def add_block(self):
        self.new_block=True
 
    def reset(self):
        self.body=[Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction=Vector2(0,0)

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_move_sound(self):
        self.move_sound.play()

    def play_collision_sound(self):
        self.collision_sound.play()

class MAIN():
    def __init__(self):
        self.snake=SNAKE()    
        self.fruit=FRUIT()    

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos==self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block==self.fruit.pos:
                self.fruit.randomize() 

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color=(167,209,61)
        for row in range(cell_number):
            if row % 2==0:
                for col in range(cell_number):
                    if col%2==0:
                        grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)
            else:
                for col in range(cell_number):
                    if col%2!=0:
                        grass_rect=pygame.Rect(col*cell_size,row*cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,grass_color,grass_rect)

    def check_fail(self):
        # hitting the wall:if snake is not in the defined region
        if not(0<=self.snake.body[0].x<cell_number) or not(0<=self.snake.body[0].y<cell_number):
            self.snake.play_collision_sound()
            self.game_over()
        
        # hits itself
        else:
            for block in self.snake.body[1:]:
                if block==self.snake.body[0]:
                    # print(block)
                    self.game_over()
     
    def draw_score(self):
        score_text=str(len(self.snake.body)-3)
        score_surface=game_font.render(score_text,True,(56,74,12))
        score_x=int(cell_size*cell_number-48)
        score_y=int(cell_size*cell_number-32)
        score_rect=score_surface.get_rect(center=(score_x,score_y))

        cherry_rect=cherry.get_rect(midright=(score_rect.left,score_rect.centery))

        screen.blit(cherry,cherry_rect)
        screen.blit(score_surface,score_rect)

pygame.init()
cell_size=32
cell_number=15
width=cell_size*cell_number
height=cell_size*cell_number
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake game')

cherry=pygame.image.load("Assets/cherries.png").convert_alpha()
game_font=pygame.font.Font('Font/PoetsenOne-Regular.ttf',25)

# set up clock
clock=pygame.time.Clock()
fps=60

main_game=MAIN()

# custom event:
SCREEN_UPDATE=pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)
# our custom event will trigger in every 150ms 

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type==SCREEN_UPDATE:
            main_game.update()

        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_UP:
                if main_game.snake.direction.y!=1:
                    main_game.snake.direction=Vector2(0,-1)
                    main_game.snake.play_move_sound()
                    

            if event.key== pygame.K_DOWN:
                if main_game.snake.direction.y!=-1:
                    main_game.snake.direction=Vector2(0,1)
                    main_game.snake.play_move_sound()

            if event.key== pygame.K_LEFT:
                if main_game.snake.direction.x!=1:
                    main_game.snake.direction=Vector2(-1,0)
                    main_game.snake.play_move_sound()

            if event.key== pygame.K_RIGHT:
                if main_game.snake.direction.x!=-1:
                    main_game.snake.direction=Vector2(1,0)
                    main_game.snake.play_move_sound()

    screen.fill((175,215,70))
    # screen.fill((229,255,204))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(fps)