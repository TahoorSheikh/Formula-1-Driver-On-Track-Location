# import libraries 
import pygame
import F1_position_data as F1
import F1_processing as Fp

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

# Adjusting for 'Long tracks' so they fit in the screen
if F1.track in long_tracks_x:
    x_norm = 400

if F1.track in long_tracks_y:
    y_norm = 400

# set up pygame
pygame.init()
screen = pygame.display.set_mode((1600, 1000))
clock = pygame.time.Clock()
running = True

x, y, Throttle, Brake, lap_time_1, Gears, Speed = F1.pick_driver(driver_1)

x2, y2, Throttle2, Brake2, lap_time_2, Gears2, Speed2 = F1.pick_driver(driver_2)

x_list, y_list = Fp.Nomalize(x,y,x_norm,y_norm)

x2_list, y2_list = Fp.Nomalize(x2,y2,x_norm,y_norm)

x_list_track, y_list_track = Fp.Nomalize(F1.x_track,F1.y_track,x_norm,y_norm)

# Initialize values for loops
i = 0
k = 0

# Set up fonts
text_font = pygame.font.SysFont('Arial', 30)
text_font_2 = pygame.font.SysFont('Arial', 15)

# get postion of starting line
Start_pos = (x_list_track[0][0]+50.0,y_list_track[0][0]+50.0)

# Main simulation loop
while running:
    # check if user pressed x to exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0)) 

    Fp.draw_text(f"{F1.track_name} {F1.Year}:", text_font, (255, 255, 255), 900, 100, screen)
    Fp.draw_text(f"{F1.session.name}", text_font, (255, 255, 255), 900, 150, screen)

    for j in range(len(F1.x_track)-1):
        pygame.draw.line(screen, (255, 255, 255), (x_list_track[j][0]+50.0, y_list_track[j][0]+50.0),(x_list_track[j+1][0]+50.0, y_list_track[j+1][0]+50.0),width=2)

    # Rendering all visuals
    pygame.draw.circle(screen,(255,255,255),Start_pos,10)
    Fp.draw_dot(i,x,screen,(0, 255, 255),x_list,y_list,Throttle,Brake,Gears,Speed,driver_1,500,text_font)
    Fp.draw_dot(k,x2,screen,(255, 255, 0),x2_list,y2_list,Throttle2,Brake2,Gears2,Speed2,driver_2,750,text_font)
    i+=1
    k+=1
   
    if i >= len(x):
        Fp.draw_text(driver_1, text_font, (0, 255, 255), 950, 450, screen)
        Fp.draw_text(str(lap_time_1).strip('0 days :'),text_font, (0, 255, 255), 950, 500, screen)
    
    if k >= len(x2):
        Fp.draw_text(driver_2, text_font, (255, 255, 0), 950, 650, screen)
        Fp.draw_text(str(lap_time_2).strip('0 days :'), text_font, (255, 255, 0), 950, 700, screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # set fps
    clock.tick(10)

pygame.quit()