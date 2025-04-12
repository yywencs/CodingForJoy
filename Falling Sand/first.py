import sys
import random
import pygame
import colorsys


SIZE = 5  # 棋盘每个点时间的间隔
Width_Points = 201  # 棋盘每行/每列点数
Hight_Points = 121  # 棋盘每行/每列点数
num_rows = Hight_Points - 1  # 行数和列数
num_cols = Width_Points - 1
BACKGROUND_COLOR = (0, 0, 0)  # 背景颜色
WHITE_COLOR = (255, 255, 255)  # 白色
Outer_Width = 20  # 棋盘外宽度
Border_Width = 4  # 边框宽度
Inside_Width = 4  # 边框跟实际的棋盘之间的间隔
Border_Width_Length = SIZE * (Width_Points - 1) + Inside_Width * 2 + Border_Width  # 边框线的长度
Border_Height_Length = SIZE * (Hight_Points - 1) + Inside_Width * 2 + Border_Width  # 边框线的高度
Start_X = Start_Y = Outer_Width + int(Border_Width / 2) + Inside_Width  # 网格线起点（左上角）坐标
SCREEN_HEIGHT = SIZE * (Hight_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2  # 游戏屏幕的高
SCREEN_WIDTH = SIZE * (Width_Points - 1) + Outer_Width * 2 + Border_Width + Inside_Width * 2  # 游戏屏幕的宽
all_blocks = [[0] * num_cols for _ in range(num_rows) ]  # 所有的方块
speeds = [[0] * num_cols for _ in range(num_rows) ]

# 画棋盘
def _draw_checkerboard(screen):
    # 填充棋盘背景色
    screen.fill(BACKGROUND_COLOR)
    # 画棋盘网格线外的边框
    pygame.draw.rect(screen, WHITE_COLOR, (Outer_Width, Outer_Width, Border_Width_Length, Border_Height_Length), Border_Width)

def _draw_block() :

    # 画方块
    for i in range(num_rows):
        for j in range(num_cols):
            if all_blocks[i][j] > 0:
                r, g, b = colorsys.hsv_to_rgb(all_blocks[i][j], 1, 1)
                # 将 RGB 值从 0 - 1 范围转换为 0 - 255 范围
                r = int(r * 255)
                g = int(g * 255)
                b = int(b * 255)
                pygame.draw.rect(screen, (r, g, b), (Start_X + SIZE * j, Start_Y + SIZE * i, SIZE, SIZE), 0)


def block_down() :
    global all_blocks, speeds
    new_blocks = [[0] * num_cols for _ in range(num_rows)]  # 新建一个二维数组来存储新的方块状态
    new_speeds = [[0] * num_cols for _ in range(num_rows)]  # 新建一个二维数组来存储新的速度状态
    for i in range(num_rows) :
        for j in range(num_cols) :
            if all_blocks[i][j] > 0 :
                state = all_blocks[i][j]  # 当前方块的状态
                speed = speeds[i][j]  # 当前方块的速度

                new_location = i + int(speed + GRAVITY)
                new_location = min(new_location, num_rows - 1)  # 限制新位置不超过边界
                moved = False

                for loc in range(new_location, i, -1) :
                    below = all_blocks[loc][j]
                    
                    dir = random.choice([-1, 1])
                    
                    belowA = belowB = None
                    if 0 <= j - dir < num_cols: belowA = all_blocks[loc][j - dir]
                    if 0 <= j + dir < num_cols: belowB = all_blocks[loc][j + dir]

                    # 判断当前方块是否可以下落 
                    if below == 0 :
                        new_blocks[loc][j] = state
                        new_speeds[loc][j] = speed + GRAVITY
                        moved = True
                        break
                    elif belowA == 0 :
                        new_blocks[loc][j - dir] = state
                        new_speeds[loc][j] = speed + GRAVITY
                        moved = True
                        break
                    elif belowB == 0:
                        new_blocks[loc][j + dir] = state
                        new_speeds[loc][j] = speed + GRAVITY
                        moved = True
                        break
                if not moved:
                    new_blocks[i][j] = state
                    new_speeds[i][j] = speed + GRAVITY

    all_blocks = new_blocks
    speeds = new_speeds

            
    
def change_block(mouse_x: int, mouse_y: int, color: float) :
    # 计算鼠标点击的行和列
    row = (mouse_y - Start_Y) // SIZE
    col = (mouse_x - Start_X) // SIZE
    
    # 检查鼠标点击是否在棋盘范围内
    if 0 <= row < num_rows and 0 <= col < num_cols:
        for i in range(-3, 3):
            for j in range(-3, 3):
                x = row + i
                y = col + j
                if 0 <= x < num_rows and 0 <= y < num_cols and random.random() < 0.75:
                    all_blocks[x][y] = color
                    speeds[x][y] = 0.1


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('FALLING SAND!')
is_shooting = False
GRAVITY = 0.2
color = 0.1

while True :
    mouse_x, mouse_y = None, None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 获取鼠标位置
            is_shooting = True
        elif event.type == pygame.MOUSEBUTTONUP:
            is_shooting = False
    
    block_down()
    
    if is_shooting:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        color += 0.0028
        if color > 1 :
            color = 0.0028
        change_block(mouse_x, mouse_y, color)
        
    
    _draw_checkerboard(screen)
    _draw_block()
    
    pygame.display.flip()
    clock.tick(60)
