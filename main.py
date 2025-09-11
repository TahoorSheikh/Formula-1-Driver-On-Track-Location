# import libraries 
import pygame
import F1_position_data as F1
import math

# Print driver list
print(F1.session.drivers)

# Pick driver 1 and 2
driver_1 = input("Select driver 1: ")
driver_2 = input("Select driver 2: ")

# Normalize x and y
x_norm = 800
y_norm = 800

# List of 'long tracks'
long_tracks_x = ['Jeddah','Montréal','Yas Island']
long_tracks_y = ['Singapore']

if F1.track in long_tracks_x:
    x_norm = 400

if F1.track in long_tracks_y:
    y_norm = 400

# set up pygamec
pygame.init()
screen = pygame.display.set_mode((1600, 1000))
clock = pygame.time.Clock()
running = True

# Function to Normalize
def Nomalize(x,y):
    # Normalaize positional data for driver 1
    x_max, x_min = x.max(), x.min()

    y_max, y_min = y.max(), y.min()

    x_list = []

    y_list = []

    for i in range(len(x)):
        x_list.append(((x.iloc[i][0] - x_min) / (x_max - x_min)) * x_norm)
        y_list.append(((y.iloc[i][0] - y_min) / (y_max - y_min)) * y_norm)
    
    return x_list, y_list

x, y, Throttle, Brake, lap_time_1 = F1.pick_driver(driver_1)

x2, y2, Throttle2, Brake2, lap_time_2 = F1.pick_driver(driver_2)

x_list, y_list = Nomalize(x,y)

x2_list, y2_list = Nomalize(x2,y2)

x_list_track, y_list_track = Nomalize(F1.x_track,F1.y_track)

i = 0
k = 0

text_font = pygame.font.SysFont('Arial', 30)
text_font_2 = pygame.font.SysFont('Arial', 15)

# draw text function
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img,(x ,y))

# draw circle
def draw_dot(u,x,screen,color,xlist,ylist,throttle,brake,driver,ycord):
    if u < len(x):
        pygame.draw.circle(screen, color, (xlist[u][0]+50.0, ylist[u][0]+50.0), 5)

        press = (throttle[u]/100) * 255

        press_surface = pygame.Surface((50, 100), pygame.SRCALPHA) 
        press_surface.fill((0, 255, 0, press))
        screen.blit(press_surface,(900,ycord))
        draw_text(f"{round(throttle[u],2)}%",text_font,(0, 255, 0), 900, ycord+100)
    
        if brake[u] == True:
            pygame.draw.rect(screen, (255, 0, 0),[1000,ycord,50,100])

        draw_text(f"Driver : {driver}", text_font, color, 950, ycord-50)

if F1.type == 'R':
    current_lap = 1
    crossed = False
    message = ""
    race_control_msg_done = False
    flag = ""

Start_pos = (x_list_track[0][0]+50.0,y_list_track[0][0]+50.0)

def distance(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

while running:
    # check if user pressed x to exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0)) 

    draw_text(f"{F1.track_name} {F1.Year}:", text_font, (255, 255, 255), 900, 100)
    draw_text(f"{F1.session.name}", text_font, (255, 255, 255), 900, 150)

    for j in range(len(F1.x_track)-1):
        pygame.draw.line(screen, (255, 255, 255), (x_list_track[j][0]+50.0, y_list_track[j][0]+50.0),(x_list_track[j+1][0]+50.0, y_list_track[j+1][0]+50.0),width=2)

    # RENDER YOUR GAME HERE
    pygame.draw.circle(screen,(255,255,255),Start_pos,10)
    draw_dot(i,x,screen,(0, 255, 255),x_list,y_list,Throttle,Brake,driver_1,500)
    draw_dot(k,x2,screen,(255, 255, 0),x2_list,y2_list,Throttle2,Brake2,driver_2,750)
    i+=1
    k+=1
   
    if i >= len(x):
        draw_text(driver_1, text_font, (0, 255, 255), 950, 450)
        draw_text(str(lap_time_1).strip('0 days :'),text_font, (0, 255, 255), 950, 500)
    
    if k >= len(x2):
        draw_text(driver_2, text_font, (255, 255, 0), 950, 650)
        draw_text(str(lap_time_2).strip('0 days :'), text_font, (255, 255, 0), 950, 700)

    if F1.type == 'R':
        
        draw_text(f"Lap: {current_lap}/{F1.all_laps}",text_font,(255,255,255),900,200)

        car_pos = (x_list[i][0]+50, y_list[i][0]+50)
        
        # Check if car is very close to start dot
        if distance(car_pos, Start_pos) < 10:   
            if not crossed:  
                current_lap += 1
                crossed = True
                race_control_msg_done = False
        else:
            crossed = False 

        if not race_control_msg_done:
            message = ""
            flag = ""
            for a in range(len(F1.race_messages)):
                if (F1.race_messages.iloc[a][2] == current_lap):
                    message += f"{F1.race_messages.iloc[a][0]}---"
                    flag += f"{F1.race_messages.iloc[a][1]}-"
        
            race_control_msg_done = True
        
        draw_text(f"{message}",text_font_2,(255,255,255),40,20)

        draw_text(f"Current Flag: {flag.replace('None-','')}",text_font,(255,255,255),900,300)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # set fps
    clock.tick(10)

pygame.quit()

