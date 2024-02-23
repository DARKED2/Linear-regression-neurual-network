import pygame
import math
from sklearn.linear_model import LinearRegression
import numpy as np


# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

points = [(-40, -40), (0, 0), (40, 40)] #координаты трех точек 

POINT_RADIUS = 7 #радиус точки 
line_thickness = 2 # толщина линии
is_mouse_pressed_left = False

# Установка размеров окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Создает окно с заданными размерами
pygame.display.set_caption("Template") # устанавливает заголовок окна 

#Функция для нахождения линейной регресии
def linear_regression(points):
    Xs = []
    Ys = []
    for index in points:
        Xs.append(index[0])
        Ys.append(index[1])
        
    Xs =np.array(Xs).reshape(-1, 1)
    Ys = np.array(Ys)

    model = LinearRegression()

    model.fit(Xs, Ys)
    
    w = model.coef_
    b = model.intercept_

    return w,b


#рисуем кординатные оси
def draw_axes():
    pygame.draw.line(screen,BLACK,(WIDTH // 2,0),(WIDTH // 2 , HEIGHT))
    pygame.draw.line(screen,BLACK,(0, HEIGHT // 2), (WIDTH, HEIGHT // 2))

# рисуем линию 
def draw_line(w,b):
    x1 = -400
    x2 = 400
    y1 = w[0] * x1 + b
    y2 = w[0] * x2 + b

    x1 += WIDTH//2
    y1 = HEIGHT//2 -y1
    x2 += WIDTH//2
    y2 = HEIGHT //2 - y2
    pygame.draw.line(screen,RED,(x1,y1), (x2,y2),line_thickness)

#рисует точки на кординатной плоскости 
def draw_points():
    for point in points:
        x,y = point

        x += WIDTH //2
        y = HEIGHT // 2 - y
        pygame.draw.circle(screen,RED,(x,y),POINT_RADIUS)

#фукция для пороверки касания точки 
def check_point_touch(x,y,):
    for index in range(len(points)):
        px,py = points[index]
        px += WIDTH //2
        py = HEIGHT //2 - py
        
        distance = ((x -px)**2 + (y - py)**2)**0.5
        if distance <= POINT_RADIUS:
            
            return index
    return -1

#функция для смещения точек к центру
def Shifted_point_to_center(x,y):
    xm = x - WIDTH //2
    ym = HEIGHT // 2 - y
    return xm,ym

#основной цыкл программы
running = True
index = -1
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                is_mouse_pressed_left = True
                x, y = pygame.mouse.get_pos()
                index = check_point_touch(x,y,)
                if index != -1:
                  print("вы нажали на точку: ", index)
             
            #при нажатии правой кнопки мыши, добавляем току и рисуем на графике
            if event.button == 3: # 3 - означает нажатие правой кнопки мыши в pygame
                mouse_x,mouse_y = event.pos
                points.append(Shifted_point_to_center(mouse_x,mouse_y))


        elif event.type == pygame.MOUSEMOTION: # проверяет событие движение мышки
            if is_mouse_pressed_left and index != -1:
                mouse_x, mouse_y = event.pos #возвращает координаты мыши
                points[index] = Shifted_point_to_center(mouse_x,mouse_y) #сдвигаем координаты относительно центра

        elif event.type == pygame.MOUSEBUTTONUP:
            is_mouse_pressed_left = False


    screen.fill(WHITE)
    draw_axes() 
    draw_points()
    w,b = linear_regression(points)
    draw_line(w,b)
    pygame.display.flip()

pygame.quit()