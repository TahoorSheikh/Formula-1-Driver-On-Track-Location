# import libraries 
import pygame
import F1_position_data as F1

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
screen = pygame.display.set_mode((1200, 1000))
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

# Normalaize positional data for track
x_max_track, x_min_track = F1.x_track.max(), F1.x_track.min()

y_max_track, y_min_track = F1.y_track.max(), F1.y_track.min()

x_list_track = []

y_list_track = []

for i in range(len(F1.x_track)):
    x_list_track.append(((F1.x_track.iloc[i][0] - x_min_track) / (x_max_track - x_min_track)) * x_norm)
    y_list_track.append(((F1.y_track.iloc[i][0] - y_min_track) / (y_max_track - y_min_track)) * y_norm)

i = 0
k = 0

text_font = pygame.font.SysFont('Arial', 30)

# draw text function
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img,(x ,y))

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
    if i < len(x):
        pygame.draw.circle(screen, (0, 255, 255), (x_list[i][0]+50.0, y_list[i][0]+50.0), 5)

        press = (Throttle[i]/100) * 255

        press_surface = pygame.Surface((50, 100), pygame.SRCALPHA) 
        press_surface.fill((0, 255, 0, press))
        screen.blit(press_surface,(900,500))
        draw_text(f"{round(Throttle[i],2)}%",text_font,(0, 255, 0), 900, 600)
    
        if Brake[i] == True:
            pygame.draw.rect(screen, (255, 0, 0),[1000,500,50,100])

        i+=1

        draw_text(f"Driver : {driver_1}", text_font, (0, 255, 255), 950, 450)
    
    if k < len(x2):
        pygame.draw.circle(screen, (255, 255, 0), (x2_list[k][0]+50.0, y2_list[k][0]+50.0), 5)

        press2 = (Throttle2[k]/100) * 255

        press_surface2 = pygame.Surface((50, 100), pygame.SRCALPHA) 
        press_surface2.fill((0, 255, 0, press2))
        screen.blit(press_surface2,(900,750))
        draw_text(f"{round(Throttle2[k],2)}%",text_font,(0, 255, 0), 900, 850)
    
        if Brake2[k] == True:
            pygame.draw.rect(screen, (255, 0, 0),[1000,750,50,100])

        k+=1

        draw_text(f"Driver : {driver_2}", text_font, (255, 255, 0), 950, 700)
    
    if i >= len(x):
        draw_text(driver_1, text_font, (0, 255, 255), 950, 450)
        draw_text(str(lap_time_1).strip('0 days :'),text_font, (0, 255, 255), 950, 500)
    
    if k >= len(x2):
        draw_text(driver_2, text_font, (255, 255, 0), 950, 650)
        draw_text(str(lap_time_2).strip('0 days :'), text_font, (255, 255, 0), 950, 700)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # set fps
    clock.tick(20)

pygame.quit()

