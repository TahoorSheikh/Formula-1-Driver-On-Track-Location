import pygame
import math

# Normalaize positional data for drivers
def Nomalize(x,y,x_norm,y_norm):
    x_max, x_min = x.max(), x.min()

    y_max, y_min = y.max(), y.min()

    x_list = []

    y_list = []

    for i in range(len(x)):
        x_list.append(((x.iloc[i][0] - x_min) / (x_max - x_min)) * x_norm)
        y_list.append(((y.iloc[i][0] - y_min) / (y_max - y_min)) * y_norm)
    
    return x_list, y_list

# draw text function
def draw_text(text, font, color, x, y, screen):
    img = font.render(text, True, color)
    screen.blit(img,(x ,y))

# draw circle
def draw_dot(u,x,screen,color,xlist,ylist,throttle,brake,Gears,Speed,driver,ycord,text_font):
    if u < len(x):
        pygame.draw.circle(screen, color, (xlist[u][0]+50.0, ylist[u][0]+50.0), 5)

        press = (throttle[u]/100) * 255

        press_surface = pygame.Surface((50, 100), pygame.SRCALPHA) 
        press_surface.fill((0, 255, 0, press))
        screen.blit(press_surface,(900,ycord))
        draw_text(f"{round(throttle[u],2)}%",text_font,(0, 255, 0), 900, ycord+100,screen)
        draw_text(f"Gear: {Gears[u]}",text_font,(0, 255, 0), 1200, ycord,screen)
        draw_text(f"Speed: {round(Speed[u],2)}",text_font,(0, 255, 0), 1200, ycord-50,screen)
        if brake[u] == True:
            pygame.draw.rect(screen, (255, 0, 0),[1000,ycord,50,100])

        draw_text(f"Driver : {driver}", text_font, color, 950, ycord-50,screen)

# Calcuate disacne between dots
def distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

