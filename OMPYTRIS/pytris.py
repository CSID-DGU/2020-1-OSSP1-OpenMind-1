# PYTRIS™ Copyright (c) 2017 Jason Kim All Rights Reserved.

import pygame
import operator
from tkinter import *
from mino import *
from random import *
from pygame.locals import *

# Define
block_size = 35 # Height, width of single block
width = 10 # Board width
height = 20 # Board height
framerate = 30 # Bigger -> Slower

movement_keys = {'left': 0, 'right': 0}
movement_keys_speed = 0.05
movement_keys_timer = movement_keys_speed * 2

pygame.init() # pygame 모듈 생성 

clock = pygame.time.Clock() # 타임트렉커 생성
screen = pygame.display.set_mode((1200, 730), FULLSCREEN | HWSURFACE | DOUBLEBUF)  # 창크기 설정 1200 * 730, 하드웨어 가속, 더블버퍼 모드
pygame.time.set_timer(pygame.USEREVENT, framerate * 10) # 유저이벤트 0.3초마다 입력
pygame.display.set_caption("OPENMIND TETRIS™")
volume = 1.0
class ui_variables:
    # Fonts
    font_path = "./assets/fonts/Maplestory_Light.ttf"
    font_path_b = "./assets/fonts/OpenSans-Bold.ttf"
    font_path_i = "./assets/fonts/Inconsolata/Inconsolata.otf"

    h1 = pygame.font.Font(font_path, 53) ##
    h2 = pygame.font.Font(font_path, 42)
    h4 = pygame.font.Font(font_path, 32)
    h5 = pygame.font.Font(font_path, 20)   # press space
    h6 = pygame.font.Font(font_path, 10)  # copyright

    h1_b = pygame.font.Font(font_path_b, 50)
    h2_b = pygame.font.Font(font_path_b, 40)

    h2_i = pygame.font.Font(font_path_i, 35)
    h5_i = pygame.font.Font(font_path_i, 13)

    # Sounds
    pygame.mixer.music.load("assets/sounds/SFX_BattleMusic.wav")
    intro_sound = pygame.mixer.Sound("assets/sounds/SFX_Intro.wav")
    intro_sound.set_volume(volume)
    fall_sound = pygame.mixer.Sound("assets/sounds/SFX_Fall.wav")
    fall_sound.set_volume(volume)
    break_sound = pygame.mixer.Sound("assets/sounds/SFX_Break.wav")
    break_sound.set_volume(volume)
    click_sound = pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")
    click_sound.set_volume(volume)
    move_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
    move_sound.set_volume(volume)
    drop_sound = pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
    drop_sound.set_volume(volume)
    single_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
    single_sound.set_volume(volume)
    double_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
    double_sound.set_volume(volume)
    triple_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
    triple_sound.set_volume(volume)
    tetris_sound = pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")
    tetris_sound.set_volume(volume)
    GameOver_sound = pygame.mixer.Sound("assets/sounds/SFX_GameOver.wav")
    GameOver_sound.set_volume(volume)
    LevelUp_sound = pygame.mixer.Sound("assets/sounds/SFX_LevelUp.wav")
    LevelUp_sound.set_volume(volume)

    combos = [] # 콤보 그래픽
    large_combos = [] # 사이즈 조절한 콤보 그래픽
    combo_ring = pygame.image.load("assets/Combo/4combo ring.png") # 4블록 제거용 그래픽
    combo_4ring = pygame.transform.scale(combo_ring, (200, 100))
    for i in range (1,11):
        combos.append(pygame.image.load("assets/Combo/"+str(i)+"combo.png"))
        large_combos.append(pygame.transform.scale(combos[i-1], (150, 200)))  # 사진크기 조절

    combos_sound = []
    for i in range(1, 10) :
        combos_sound.append(pygame.mixer.Sound("assets/sounds/SFX_"+str(i+2)+"Combo.wav"))


    # Background colors
    black = (10, 10, 10) #rgb(10, 10, 10)
    #yellow = (10, 10, 10)
    white = (255, 255, 240) #rgb(255, 255, 255) 오른쪽 바(아이보리)
    grey_1 = (70, 130, 180) #rgb(26, 26, 26) 파란색(238,130,238)(70, 130, 180)
    #blue = (30,30,30)
    grey_2 = (221, 221, 221) #rgb(35, 35, 35)테트리스 게임내 배경(회색)(221, 221, 221) (135,206,235)
    grey_3 = (000,000,139) #rgb(55, 55, 55) 블록 그림자 색

    # Tetrimino colors
    cyan = (69, 206, 204) #rgb(69, 206, 204) # I
    blue = (64, 111, 249) #rgb(64, 111, 249) # J
    orange = (253, 189, 53) #rgb(253, 189, 53) # L
    yellow = (246, 227, 90) #rgb(246, 227, 90) # O
    green = (98, 190, 68) #rgb(98, 190, 68) # S
    pink = (242, 64, 235) #rgb(242, 64, 235) # T
    red = (225, 13, 27) #rgb(225, 13, 27) # Z

    t_color = [grey_2, cyan, blue, orange, yellow, green, pink, red, grey_3]

def checkCombo(combo_count,sent):
    if combo_count > 0:
        if combo_count <= 8:
            sent += (combo_count+1)/2
        else :
            sent += 4
    return sent
def draw_image(window,img_path, x,y,width,height):

    image= pygame.image.load(img_path)
    image = pygame.transform.scale(image,(width,height))
    window.blit(image,(x,y))
class button(): 
    def __init__(self, color, x,y,width,height, text='',img='', img_clicked=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = img
        self.image = img_clicked

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            # pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            draw_image(screen, self.image ,self.x, self.y, self.width, self.height )

            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
        

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

# 버튼 클래스 
    # 버튼 생성
    # 버튼 이미지 경로
    # 버튼 선택했을 때 이미지 경로
    # 버튼 id 값
    # 버튼 
    
# Draw block

def draw_block(x, y, color): # 블럭 그리는 함수
    pygame.draw.rect(
        screen,
        color,
        Rect(x, y, block_size, block_size)
    )
    pygame.draw.rect(
        screen,
        ui_variables.grey_1,
        Rect(x, y, block_size, block_size),
        1
    )


def draw_multiboard(next_1P,hold_1P,next_2P,hold_2P,score,level,goal):
    screen.fill(ui_variables.grey_1)
    draw_board(next_1P,hold_1P,score,level,goal)
    draw_2Pboard(next_2P,hold_2P,score,level,goal)


# Draw game screen
def draw_board(next, hold, score, level, goal):
    

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(384, 0, 180, 730)
    )   

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4): # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(4):
            dx = 415 + block_size * j
            dy = 220 + block_size * i
            if grid_n[i][j] != 0:
                draw_block(dx,dy,ui_variables.t_color[grid_n[i][j]]) # 다음 블럭의 형상 가독성을 높임.
               

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 415 + block_size * j
                dy = 60 + block_size * i
                if grid_h[i][j] != 0:
                    
                    draw_block(dx,dy,ui_variables.t_color[grid_h[i][j]])

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.black) # 콤보 
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.black) # 콤보 값

    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)

    # Place texts
### <<<<<<< HEAD
    screen.blit(text_hold, (215, 14))
    screen.blit(text_next, (215, 104))
    screen.blit(text_score, (215, 194))
    screen.blit(score_value, (220, 210))
    screen.blit(text_level, (215, 254))
    screen.blit(level_value, (220, 270)) 
    screen.blit(text_goal, (215, 314))
    screen.blit(goal_value, (220, 330))
## =======
    screen.blit(text_hold, (415, 20))
    screen.blit(text_next, (415, 170))
    screen.blit(text_score, (415, 340))
    screen.blit(score_value, (420, 370))
    screen.blit(text_level, (415, 470))
    screen.blit(level_value, (420, 500))
    #screen.blit(text_goal, (415, 600))
    #screen.blit(goal_value, (420, 630))
    screen.blit(text_combo,(415,600))
    screen.blit(combo_value,(420,630))
# >>>>>>> 9019b1371478d307091a004b6d22207004f8782c

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = 17 + block_size * x
            dy = 17 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix[x][y + 1]])

def draw_2Pboard(next, hold, score, level, goal):

    # Draw sidebar
    pygame.draw.rect(
        screen,
        ui_variables.white,
        Rect(948, 0, 180, 730)
    )   

    # Draw next mino
    grid_n = tetrimino.mino_map[next - 1][0]

    for i in range(4): # 16개의 그리드 칸에서 true인 값만 뽑아서 draw.rect
        for j in range(4):
            dx = 979 + block_size * j
            dy = 220 + block_size * i
            if grid_n[i][j] != 0:
                draw_block(dx,dy,ui_variables.t_color[grid_n[i][j]]) # 다음 블럭의 형상 가독성을 높임.
                

    # Draw hold mino
    grid_h = tetrimino.mino_map[hold - 1][0]

    if hold_mino != -1:
        for i in range(4):
            for j in range(4):
                dx = 979 + block_size * j
                dy = 60 + block_size * i
                if grid_h[i][j] != 0:
                    draw_block(dx,dy,ui_variables.t_color[grid_h[i][j]])

    # Set max score
    if score > 999999:
        score = 999999

    # Draw texts
    text_hold = ui_variables.h5.render("HOLD", 1, ui_variables.black)
    text_next = ui_variables.h5.render("NEXT", 1, ui_variables.black)
    text_combo = ui_variables.h5.render("COMBO", 1, ui_variables.black) # 콤보 
    text_score = ui_variables.h5.render("SCORE", 1, ui_variables.black)
    combo_value = ui_variables.h4.render(str(combo_count), 1, ui_variables.black) # 콤보 값

    score_value = ui_variables.h4.render(str(score), 1, ui_variables.black)
    text_level = ui_variables.h5.render("LEVEL", 1, ui_variables.black)
    level_value = ui_variables.h4.render(str(level), 1, ui_variables.black)
    text_goal = ui_variables.h5.render("GOAL", 1, ui_variables.black)
    goal_value = ui_variables.h4.render(str(goal), 1, ui_variables.black)

    # Place texts
### <<<<<<< HEAD
    screen.blit(text_hold, (779, 14))
    screen.blit(text_next, (779, 104))
    screen.blit(text_score, (779, 194))
    screen.blit(score_value, (784, 210))
    screen.blit(text_level, (779, 254))
    screen.blit(level_value, (784, 270)) 
    screen.blit(text_goal, (779, 314))
    screen.blit(goal_value, (784, 330))
## =======
    screen.blit(text_hold, (979, 20))
    screen.blit(text_next, (979, 170))
    screen.blit(text_score, (979, 340))
    screen.blit(score_value, (984, 370))
    screen.blit(text_level, (979, 470))
    screen.blit(level_value, (984, 500))
    screen.blit(text_combo,(979,600))
    screen.blit(combo_value,(984,630))

    # Draw board
    for x in range(width):
        for y in range(height):
            dx = 581 + block_size * x
            dy = 17 + block_size * y
            draw_block(dx, dy, ui_variables.t_color[matrix_2P[x][y + 1]])


# Draw a tetrimino
def draw_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[tx + j][ty + i] = 8

    # Draw mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = grid[i][j]
def draw_mino_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    tx, ty = x, y
    while not is_bottom_2P(tx, ty, mino, r):
        ty += 1

    # Draw ghost
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix_2P[tx + j][ty + i] = 8

    # Draw mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix_2P[x + j][y + i] = grid[i][j]
# Erase a tetrimino
def erase_mino(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(21):
        for i in range(10):
            if matrix[i][j] == 8:
                matrix[i][j] = 0

    # Erase mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix[x + j][y + i] = 0

def erase_mino_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    # Erase ghost
    for j in range(21):
        for i in range(10):
            if matrix_2P[i][j] == 8:
                matrix_2P[i][j] = 0

    # Erase mino
    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                matrix_2P[x + j][y + i] = 0
# Returns true if mino is at bottom
def is_bottom(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix[x + j][y + i + 1] != 0 and matrix[x + j][y + i + 1] != 8:
                    return True

    return False
def is_bottom_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (y + i + 1) > 20:
                    return True
                elif matrix_2P[x + j][y + i + 1] != 0 and matrix_2P[x + j][y + i + 1] != 8:
                    return True

    return False
# Returns true if mino is at the left edge
def is_leftedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix[x + j - 1][y + i] != 0:
                    return True

    return False
def is_leftedge_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j - 1) < 0:
                    return True
                elif matrix_2P[x + j - 1][y + i] != 0:
                    return True

    return False
# Returns true if mino is at the right edge
def is_rightedge(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix[x + j + 1][y + i] != 0:
                    return True

    return False
def is_rightedge_2P(x, y, mino, r):
    grid = tetrimino.mino_map[mino - 1][r]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j + 1) > 9:
                    return True
                elif matrix_2P[x + j + 1][y + i] != 0:
                    return True

    return False
# Returns true if turning right is possible
def is_turnable_r(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True
def is_turnable_r_2P(x, y, mino, r):
    if r != 3:
        grid = tetrimino.mino_map[mino - 1][r + 1]
    else:
        grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix_2P[x + j][y + i] != 0:
                    return False

    return True
# Returns true if turning left is possible
def is_turnable_l(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix[x + j][y + i] != 0:
                    return False

    return True
def is_turnable_l_2P(x, y, mino, r):
    if r != 0:
        grid = tetrimino.mino_map[mino - 1][r - 1]
    else:
        grid = tetrimino.mino_map[mino - 1][3]

    for i in range(4):
        for j in range(4):
            if grid[i][j] != 0:
                if (x + j) < 0 or (x + j) > 9 or (y + i) < 0 or (y + i) > 20:
                    return False
                elif matrix_2P[x + j][y + i] != 0:
                    return False

    return True

# Returns true if new block is drawable
def is_stackable(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            #print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix[3 + j][i] != 0:
                return False

    return True
def is_stackable_2P(mino):
    grid = tetrimino.mino_map[mino - 1][0]

    for i in range(4):
        for j in range(4):
            #print(grid[i][j], matrix[3 + j][i])
            if grid[i][j] != 0 and matrix_2P[3 + j][i] != 0:
                return False

    return True

# Initial values
blink = False
start = False # 게임 화면
pause = False # 일시 정지
done = False 
game_over = False # 게임 종료
menu = False # 메뉴화면
help = False # 도움 화면 
over_screen = False
mode = False
setting = False


leader_board = False # 점수판 목록
combo_count = 0
score = 0
level = 1
goal = level * 5
bottom_count = 0
bottom_count_2P = 0
hard_drop = False
hard_drop_2P = False

current_button = 0 # 선택 버튼 


text_mode = ui_variables.h5.render("Game Mode", 1, ui_variables.black)

# 게임 모드 선택 버튼 
#mode_button = button((ui_variables.grey_1),130,100,270,80,"Mode")
        
## 게임 종료 선택 버튼
#exit_button = button((0,255,0),130,200,270,80,'Exit')
## 점수판 목록 선택 버튼 
#leaderboard_button = button((0,255,0),130,300,270,80,'Leader Board')
        
## 시작 화면으로 돌아가기
#return_button = button((0,255,0),130,400,270,80,'Return')

## 설정 버튼
#setting_button = button((0,255,0),130,500,270,80,'Setting')

start_button = 'assets/images/start.png'     
help_button = 'assets/images/help.png'
quit_button = 'assets/images/quit.png'

start_iamge_button = button((0,255,0),130,200,270,80,'',start_button,help_button)

dx, dy = 3, 0 # Minos location status
dx_2P , dy_2P = 3, 0
rotation = 0 # Minos rotation status
rotation_2P = 0
mino = randint(1, 7) # Current mino
mino_2P = randint(1,7)
next_mino = randint(1, 7) # Next mino
next_mino_2P = randint(1,7)

hold = False # Hold status
hold_2P = False
hold_mino = -1 # Holded mino
hold_mino_2P = -1

name_location = 0
name = [65, 65, 65]

with open('leaderboard.txt') as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
for i in lines:
    leaders[i.split(' ')[0]] = int(i.split(' ')[1])
leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

matrix = [[0 for y in range(height + 1)] for x in range(width)] # Board matrix

matrix_2P = [[0 for y in range(height + 1)] for x in range(width)] # Board matrix




###########################################################
# Loop Start
###########################################################
ui_variables.intro_sound.play()

while not done:
    # Pause screen
    pygame.mixer.init()
    if pause:
        pygame.mixer.music.pause()    # 게임 일시정지시 배경음악 pause
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                draw_board(next_mino, hold_mino, score, level, goal)
                draw_2Pboard(next_mino_2P, hold_mino_2P, score, level, goal)


                pause_text = ui_variables.h2_b.render("PAUSED", 1, ui_variables.green)
                pause_start = ui_variables.h5.render('Press "ESC" to continue', 1, ui_variables.green)
                menu_start = ui_variables.h5.render('Press M to Menu Screen', 1, ui_variables.green)

                screen.blit(pause_text, (115, 250))
                if blink:
                    screen.blit(pause_start, (75, 310))
                    screen.blit(menu_start,(75,360))
                    blink = False
                else:
                    blink = True
                pygame.display.update()
            elif event.type == KEYUP:                            ##
                erase_mino(dx, dy, mino, rotation)
                erase_mino_2P(dx_2P,dy_2P,mino_2P,rotation_2P)
                if event.key == K_ESCAPE:
                    pause = False
                    start = True
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    pygame.mixer.music.unpause() # 게임 일시정지 해제시 배경음악 unpause
                elif event.key == K_m :
                    pause = False
                    menu = True
                    ui_variables.click_sound.play()
                    pygame.time.set_timer(pygame.USEREVENT, 1)

    # Game screen
    elif start:
        # 콤보 카운트
        #pressed = lambda key: event.type == pygame.KEYDOWN and event.key == key
        #unpressed = lambda key: event.type == pygame.KEYUP and event.key == key

        for event in pygame.event.get():
            #event.key = pygame.key.get_pressed()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                # Set speed
                if not game_over:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[K_DOWN]:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 1)
                    else:
                        pygame.time.set_timer(pygame.USEREVENT, framerate * 20)

                # Draw a mino
                draw_mino(dx, dy, mino, rotation)

                draw_mino_2P(dx_2P,dy_2P,mino_2P,rotation_2P)

                draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)

                # Erase a mino
                if not game_over:
                    erase_mino(dx, dy, mino, rotation)
                    erase_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)


                # Move mino down
                if not is_bottom(dx, dy, mino, rotation):
                    dy += 1

                # Create new mino
                else:
                    if hard_drop or bottom_count == 6:
                        hard_drop = False
                        bottom_count = 0
                        score += 10 * level
                        draw_mino(dx, dy, mino, rotation)
                        
                        draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                        draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)

                        if is_stackable(next_mino):
                            mino = next_mino
                            next_mino = randint(1, 7)
                            dx, dy = 3, 0
                            rotation = 0
                            hold = False
                        else: #더이상 쌓을 수 없으면 게임오버
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count += 1


                # Move mino down
                if not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                    dy_2P += 1

                # Create new mino
                else:
                    if hard_drop_2P or bottom_count_2P == 6:
                        hard_drop_2P = False
                        bottom_count_2P = 0
                        score += 10 * level
                        draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                        draw_mino(dx, dy, mino, rotation)
                        draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)

                        if is_stackable_2P(next_mino_2P):
                            mino_2P = next_mino_2P
                            next_mino_2P = randint(1, 7)
                            dx_2P, dy_2P = 3, 0
                            rotation_2P = 0
                            hold_2P = False
                        else: #더이상 쌓을 수 없으면 게임오버
                            ui_variables.GameOver_sound.play()
                            start = False
                            game_over = True
                            pygame.time.set_timer(pygame.USEREVENT, 1)
                    else:
                        bottom_count_2P += 1

                # Erase line
                # 콤보 카운트 
                erase_count = 0
                erase_count_2P = 0
                combo_value = 0
                sent = 0

                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count += 1
                        k = j
                        combo_value += 1
                        while k > 0:
                            for i in range(10):
                                matrix[i][k] = matrix[i][k - 1]
                            k -= 1
                for j in range(21):
                    is_full = True
                    for i in range(10):
                        if matrix_2P[i][j] == 0:
                            is_full = False
                    if is_full:
                        erase_count_2P += 1
                        k = j
                        combo_value += 1
                        while k > 0:
                            for i in range(10):
                                matrix_2P[i][k] = matrix_2P[i][k - 1]
                            k -= 1

                # 지운 블록이 없으면 콤보 -1
                #if erase_count == 0 :
                    #combo_count -= 1
                    #if combo_count < 0:
                        #combo_count = 0

                if erase_count >= 1:
                    combo_count += 1
                    if erase_count == 1:
                        ui_variables.break_sound.play()
                        ui_variables.single_sound.play()
                        score += 50 * level * erase_count + combo_count
                        sent += 1
                    elif erase_count == 2:
                        ui_variables.break_sound.play()
                        ui_variables.double_sound.play()
                        ui_variables.double_sound.play()
                        score += 150 * level * erase_count + 2 * combo_count
                        sent += 2
                    elif erase_count == 3:
                        ui_variables.break_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        ui_variables.triple_sound.play()
                        score += 350 * level * erase_count + 3 * combo_count
                        sent += 3
                    elif erase_count == 4:
                        ui_variables.break_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        ui_variables.tetris_sound.play()
                        score += 1000 * level * erase_count + 4 * combo_count
                        screen.blit(ui_variables.combo_4ring, (250, 160))
                        sent += 4

                    for i in range(1, 11) :
                        if combo_count == i :  # 1 ~ 10 콤보 이미지
                            screen.blit(ui_variables.large_combos[i-1], (124, 190))  # blits the combo number
                        elif combo_count > 10 : # 11 이상 콤보 이미지
                            screen.blit(tetris4, (100, 190))  # blits the combo number

                    for i in range(1, 10) :
                        if combo_count == i+2 : # 3 ~ 11 콤보 사운드
                            ui_variables.combos_sound[i-1].play()


                sent = checkCombo(combo_count, sent)  # 콤보 증가

                # Increase level
                goal -= erase_count
                if goal < 1 and level < 15:
                    level += 1
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()
                    ui_variables.LevelUp_sound.play()
                    goal += level * 5
                    framerate = int(framerate * 0.8)

            elif event.type == KEYUP:                                 ##중요
                erase_mino(dx, dy, mino, rotation)
                erase_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)

                
                if event.key == K_ESCAPE:
                    ui_variables.click_sound.play()
                    start = False
                    pause = True
                # Hard drop
                elif event.key == K_SPACE:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom(dx, dy, mino, rotation):
                        dy += 1
                    hard_drop = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P,dy_2P,mino_2P,rotation_2P)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                elif event.key == K_f:
                    ui_variables.fall_sound.play()
                    ui_variables.drop_sound.play()
                    while not is_bottom_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        dy_2P += 1
                    hard_drop_2P = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                # Hold
                elif event.key == K_LSHIFT :
                    if hold == False:
                        ui_variables.move_sound.play()
                        if hold_mino == -1:
                            hold_mino = mino
                            mino = next_mino
                            next_mino = randint(1, 7)
                        else:
                            hold_mino, mino = mino, hold_mino
                        dx, dy = 3, 0
                        rotation = 0
                        hold = True
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                elif event.key == K_c :
                    if hold_2P == False:
                        ui_variables.move_sound.play()
                        if hold_mino_2P == -1:
                            hold_mino_2P = mino_2P
                            mino_2P = next_mino_2P
                            next_mino_2P = randint(1, 7)
                        else:
                            hold_mino_2P, mino_2P = mino_2P, hold_mino_2P
                        dx_2P, dy_2P = 3, 0
                        rotation_2P = 0
                        hold_2P = True
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                # Turn right
                elif event.key == K_UP :
                    if is_turnable_r(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation += 1
                    # Kick
                    elif is_turnable_r(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation += 1
                    elif is_turnable_r(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation += 1
                    elif is_turnable_r(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation += 1
                    elif is_turnable_r(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_r(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_r(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                        rotation += 1
                    if rotation == 4:
                        rotation = 0
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                elif event.key == K_x:
                    if is_turnable_r(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        rotation_2P += 1
                    # Kick
                    elif is_turnable_r(dx_2P, dy_2P - 1, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 1, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 1, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 1
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P, dy_2P - 2, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dy_2P -= 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P + 2, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P += 2
                        rotation_2P += 1
                    elif is_turnable_r(dx_2P - 2, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        dx_2P -= 2
                        rotation_2P += 1
                    if rotation_2P == 4:
                        rotation_2P = 0
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                # Turn left
                elif event.key == K_z or event.key == K_LCTRL:
                    if is_turnable_l(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        rotation -= 1
                    # Kick
                    elif is_turnable_l(dx, dy - 1, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 1
                        rotation -= 1
                    elif is_turnable_l(dx + 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 1
                        rotation -= 1
                    elif is_turnable_l(dx - 1, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 1
                        rotation -= 1
                    elif is_turnable_l(dx, dy - 2, mino, rotation):
                        ui_variables.move_sound.play()
                        dy -= 2
                        rotation += 1
                    elif is_turnable_l(dx + 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx += 2
                        rotation += 1
                    elif is_turnable_l(dx - 2, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        dx -= 2
                    if rotation == -1:
                        rotation = 3
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                # Move left
                elif event.key == K_LEFT :                     # key = pygame.key.get_pressed()
                    if not is_leftedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx -= 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                # Move right
                elif event.key == K_RIGHT :
                    if not is_rightedge(dx, dy, mino, rotation):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx += 1
                    draw_mino(dx, dy, mino, rotation)
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                elif event.key == K_a :                     # key = pygame.key.get_pressed()
                    if not is_leftedge_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx_2P -= 1
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)
                # Move right
                elif event.key == K_d :
                    if not is_rightedge_2P(dx_2P, dy_2P, mino_2P, rotation_2P):
                        ui_variables.move_sound.play()
                        keys_pressed = pygame.key.get_pressed()
                        pygame.time.set_timer(pygame.KEYUP, framerate * 3)
                        dx_2P += 1
                    draw_mino_2P(dx_2P, dy_2P, mino_2P, rotation_2P)
                    draw_mino(dx, dy, mino, rotation)
                    draw_multiboard(next_mino,hold_mino,next_mino_2P,hold_mino_2P,score,level,goal)


                #elif unpressed(pygame.K_LEFT) :
                #   movement_keys_timer = movement_keys_speed * 2
                #elif unpressed(pygame.K_RIGHT) :
                #    movement_keys_timer = movement_keys_speed * 2

        if any(movement_keys.values()):
            movement_keys_timer += clock.tick(50)
        #if movement_keys_timer > movement_keys_speed:
        #    pressed(pygame.K_LEFT)
        #    pressed(pygame.K_RIGHT)
        #    movement_keys_timer %= movement_keys_speed

        pygame.display.update()

    # Game over screen
    elif game_over:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.mixer.music.stop()
                pygame.time.set_timer(pygame.USEREVENT, 300)
                over_text_1 = ui_variables.h2_b.render("GAME", 1, ui_variables.red)
                over_text_2 = ui_variables.h2_b.render("OVER", 1, ui_variables.red)
                over_start = ui_variables.h5.render("Press return to continue", 1, ui_variables.black)

                draw_board(next_mino, hold_mino, score, level, goal)
                screen.blit(over_text_1, (130, 250))
                screen.blit(over_text_2, (135, 290))

                name_1 = ui_variables.h2_i.render(chr(name[0]), 1, ui_variables.black)
                name_2 = ui_variables.h2_i.render(chr(name[1]), 1, ui_variables.black)
                name_3 = ui_variables.h2_i.render(chr(name[2]), 1, ui_variables.black)

                underbar_1 = ui_variables.h2.render("_", 1, ui_variables.black)
                underbar_2 = ui_variables.h2.render("_", 1, ui_variables.black)
                underbar_3 = ui_variables.h2.render("_", 1, ui_variables.black)

                screen.blit(name_1, (155, 347))
                screen.blit(name_2, (185, 347))
                screen.blit(name_3, (215, 347))

                if blink:
                    screen.blit(over_start, (70, 400))
                    blink = False
                else:
                    if name_location == 0:
                        screen.blit(underbar_1, (155, 345))
                    elif name_location == 1:
                        screen.blit(underbar_2, (185, 345))
                    elif name_location == 2:
                        screen.blit(underbar_3, (215, 345))
                    blink = True

                pygame.display.update()
            elif event.type == KEYDOWN:                                          ##
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

                    outfile = open('leaderboard.txt','a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    game_over = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score = 0
                    level = 1
                    combo_count = 0
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_m:
                    ui_variables.click_sound.play()
                    game_over = False
                    menu = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                    
    elif menu:
       
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT:
                pygame.time.set_timer(pygame.USEREVENT, 300)
                screen.fill(ui_variables.white)
                menu_text = ui_variables.h2_b.render("MENU", 1, ui_variables.cyan)
                screen.blit(menu_text, (200, 50))
                
                #mode_button.draw(screen,(0,0,0))
                #exit_button.draw(screen,(0,0,0))
                #leaderboard_button.draw(screen,(0,0,0))
                #return_button.draw(screen,(0,0,0))
                #setting_button.draw(screen,(0,0,0))


                pygame.display.flip()
        
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()

                    outfile = open('leaderboard.txt','a')
                    outfile.write(chr(name[0]) + chr(name[1]) + chr(name[2]) + ' ' + str(score) + '\n')
                    outfile.close()

                    menu = False
                    hold = False
                    dx, dy = 3, 0
                    rotation = 0
                    mino = randint(1, 7)
                    next_mino = randint(1, 7)
                    hold_mino = -1
                    framerate = 30
                    score = 0
                    score = 0
                    level = 1
                    goal = level * 5
                    bottom_count = 0
                    hard_drop = False
                    name_location = 0
                    name = [65, 65, 65]
                    matrix = [[0 for y in range(height + 1)] for x in range(width)]

                    with open('leaderboard.txt') as f:
                        lines = f.readlines()
                    lines = [line.rstrip('\n') for line in open('leaderboard.txt')]

                    leaders = {'AAA': 0, 'BBB': 0, 'CCC': 0}
                    for i in lines:
                        leaders[i.split(' ')[0]] = int(i.split(' ')[1])
                    leaders = sorted(leaders.items(), key=operator.itemgetter(1), reverse=True)

                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_RIGHT:
                    if name_location != 2:
                        name_location += 1
                    else:
                        name_location = 0
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_LEFT:
                    if name_location != 0:
                        name_location -= 1
                    else:
                        name_location = 2
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if name[name_location] != 90:
                        name[name_location] += 1
                    else:
                        name[name_location] = 65
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if name[name_location] != 65:
                        name[name_location] -= 1
                    else:
                        name[name_location] = 90
                    pygame.time.set_timer(pygame.USEREVENT, 1)
                elif event.key == K_m:
                    ui_variables.click_sound.play()
                    menu = True
                    pygame.time.set_timer(pygame.USEREVENT, 1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                #  버튼 위로 마우스 올릴 시 색깔 변동 
                # 모드 버튼 
                if mode_button.isOver(pos):
                    print("button clicked")
                    
                    mode = True
                    menu = False
                # 종료  버튼 

                if exit_button.isOver(pos):
                    print("button clicked")
                   
                    done = True
                    menu = False

                # 점수판 목록 버튼 

                if leaderboard_button.isOver(pos):
                    print("button clicked")
                    
                    leader_board = True
                    menu = False

                # 돌아가기 버튼 
                if return_button.isOver(pos):
                    print("button clicked")

                    pause = True
                    menu = False
                if setting_button.isOver(pos):
                    print("button clicked")

                    setting = True
                    menu = False

            elif event.type == pygame.MOUSEMOTION:
                #  버튼 위로 마우스 올릴 시 색깔 변동 
                # 모드 버튼 
                if mode_button.isOver(pos):
                    mode_button.color = (255,0,0)

                else : 
                    mode_button.color = (0,255,0)

                # 종료  버튼 

                if exit_button.isOver(pos):
                    exit_button.color = (255,0,0)
                else : 
                    exit_button.color = (0,255,0)
                # 점수판 목록 버튼 

                if leaderboard_button.isOver(pos):
                    leaderboard_button.color = (255,0,0)
                else : 
                    leaderboard_button.color = (0,255,0)
                # 돌아가기 버튼 
                if return_button.isOver(pos):
                    return_button.color = (255,0,0)
                else : 
                    return_button.color = (0,255,0)
                if setting_button.isOver(pos):
                    setting_button.color = (255,0,0)
                else : 
                    return_button.color = (0,255,0)




    # Start screen
    elif setting :
        root = Tk()


        root.geometry('300x300')
        root.title("Volume Setting")
        text = Label(root,text='Setting Volume!')
        text.pack()
        def set_vol(val):
            volume = int(val)/100
    
        scale = Scale(root, from_ =100, to =0, orient = VERTICAL , command = set_vol )
        scale.set(50)
        scale.pack()
        root.mainloop()
        print(volume)
        menu = True
        setting = False

    else:
        vals = ["start", "help", "exit"]  # 3가지 버튼
        button1 = Rect(520, 414, 146, 50)    # start 버튼Rect(520, 414, 146, 50)  
        buttons = [Rect(525, b * 40 + 481, 135, 40) for b in range(3)]  # help, quit 버튼
        

        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            elif event.type == USEREVENT  : 
                pygame.time.set_timer(pygame.USEREVENT, 300)
                

            elif event.type == pygame.KEYUP :
                if event.key == K_RETURN:
                    ui_variables.click_sound.play()
                    
                    if current_button == 0:
                        start = True
                        pygame.mixer.music.play(-1)
                    elif current_button == 1:
                        help = True
                    elif current_button == 2:
                        done = True
                    
                elif event.key == K_UP:
                    ui_variables.click_sound.play()
                    if current_button == 0 :
                        current_button = 2
                        pygame.time.set_timer(pygame.USEREVENT, 1)
                        print(current_button)
                    else :
                        current_button = current_button - 1 
                        pygame.time.set_timer(pygame.USEREVENT, 1)
                        print(current_button)
                      
                elif event.key == K_DOWN:
                    ui_variables.click_sound.play()
                    if current_button == 2 :
                        current_button = 0
                        pygame.time.set_timer(pygame.USEREVENT, 1)
                        print(current_button)
                    else :
                        current_button = current_button + 1 
                        pygame.time.set_timer(pygame.USEREVENT, 1)
                        print(current_button)

            m_pos = pygame.mouse.get_pos()
            m_pre = pygame.mouse.get_pressed()

        for r,v in zip(buttons,vals):
            if r.collidepoint(m_pos):
                if m_pre[0]==1:
                    v = True

        if button1.collidepoint(m_pos):
            screen.blit(start_button, (519, 417))
            if m_pre[0] == 1:
                start = True
                pygame.mixer.music.play(-1)
        elif buttons[1].collidepoint(m_pos):
            screen.blit(help_button, (525, 517))
        elif buttons[2].collidepoint(m_pos):
            screen.blit(quit_button, (525, 557))
            if m_pre[0] == 1:
                done = True  # 게임 종료
        else:
            pygame.display.update()

        pygame.display.update()
        clock.tick(50)
        pygame.display.flip()

        # pygame.time.set_timer(pygame.USEREVENT, 300)
        screen.fill(ui_variables.white)
        pygame.draw.rect(
            screen,
            ui_variables.grey_1,
            Rect(0, 400, 1200, 110)
        )
        pygame.draw.rect(
            screen,
            ui_variables.grey_1,
            Rect(0, 620, 1200, 110)
        )
        Competition = pygame.image.load('assets/images/Competition.png')
        Competition2 = pygame.transform.scale(Competition, (170, 120)) # 사진크기 조절

        Benedict = pygame.image.load('assets/images/Benedict.png')
        Benedict2 = pygame.transform.scale(Benedict, (100, 140)) # 사진크기 조절

        Bubble = pygame.image.load('assets/images/Bubble1.png')
        Bubble2 = pygame.transform.scale(Bubble, (100, 140))
        
        Benedict3 = pygame.image.load('assets/images/Benedict3.png')
        Benedict4 = pygame.transform.scale(Benedict3, (100, 140)) # 사진크기 조절

        intro_screen = pygame.image.load('assets/images/intro_screen.jpg')
        intro_screen2 = pygame.transform.scale(intro_screen, (50, 50)) # 사진크기 조절

        tetris3 = pygame.image.load('assets/images/tetris3.png')
        tetris4 = pygame.transform.scale(tetris3, (200, 150))

        square_background = pygame.image.load('assets/images/Square_Background.png')
        sbg = pygame.transform.scale(square_background, (1300, 810))

        tetris = pygame.image.load('assets/images/tetris3.png')
        tetris3 = pygame.image.load('assets/images/tetris3.png')
        
        screen.blit(Competition2, (0, 0))
        screen.blit(sbg, (-50, -40))
        screen.blit(start_button, (519, 417))
        screen.blit(help_button, (525, 517))
        screen.blit(quit_button, (525, 557))
        #screen.blit(tetris4, (600, 300))
        #screen.blit(Benedict2, (0, 180))
        #screen.blit(Benedict4, (200, 180))
        #screen.blit(Bubble2, (120, 120))

        title = ui_variables.h1.render("OM TETRIS", 1, ui_variables.grey_1)
        title_start = ui_variables.h5.render('Press "Start" to play', 1, ui_variables.white)
        title_info = ui_variables.h6.render("Copyright (c) 2017 Jason Kim All Rights Reserved.", 1, ui_variables.white)

        leader_1 = ui_variables.h5_i.render('1st ' + leaders[0][0] + ' ' + str(leaders[0][1]), 1, ui_variables.grey_1)
        leader_2 = ui_variables.h5_i.render('2nd ' + leaders[1][0] + ' ' + str(leaders[1][1]), 1, ui_variables.grey_1)
        leader_3 = ui_variables.h5_i.render('3rd ' + leaders[2][0] + ' ' + str(leaders[2][1]), 1, ui_variables.grey_1)

        if blink:
            screen.blit(title_start, (485, 470))
            blink = False
        else:
            blink = True

        screen.blit(title, (445, 240))
        screen.blit(title_info, (180, 80))

        screen.blit(leader_1, (908, 100))
        screen.blit(leader_2, (908, 110))
        screen.blit(leader_3, (908, 120))

        if not start:
            pygame.display.update()
            clock.tick(3)

pygame.quit()
