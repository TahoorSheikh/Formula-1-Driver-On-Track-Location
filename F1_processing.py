import pygame
import math
import matplotlib.pyplot as plt
import fastf1.plotting
import F1_position_data as F1

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

# Create telementary graph
def plot_speed(driver_1,driver_2):
    # Enable Matplotlib patches for plotting timedelta values and load
    # FastF1's dark color scheme
    fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme='fastf1')

    fastest_lap_driver_1 = F1.session.laps.pick_drivers(driver_1).pick_fastest()
    fastest_lap_driver_2 = F1.session.laps.pick_drivers(driver_2).pick_fastest()

    car_data_1 = fastest_lap_driver_1.get_car_data().add_distance()
    car_data_2 = fastest_lap_driver_2.get_car_data().add_distance()

    circuit_info = F1.session.get_circuit_info()

    team_color_1 = fastf1.plotting.get_team_color(fastest_lap_driver_1['Team'],session=F1.session)
    team_color_2 = fastf1.plotting.get_team_color(fastest_lap_driver_2['Team'],session=F1.session)

    fig, ax = plt.subplots()
    ax.plot(car_data_1['Distance'], car_data_1['Speed'],
        color=team_color_1, label=fastest_lap_driver_1['Driver'])
    ax.plot(car_data_2['Distance'], car_data_2['Speed'],
        color=team_color_2, label=fastest_lap_driver_2['Driver'])

    # Draw vertical dotted lines at each corner that range from slightly below the
    # minimum speed to slightly above the maximum speed.
    v_min = car_data_1['Speed'].min()
    v_max = car_data_1['Speed'].max()
    ax.vlines(x=circuit_info.corners['Distance'], ymin=v_min-20, ymax=v_max+20,
            linestyles='dotted', colors='grey')

    # Plot the corner number just below each vertical line.
    # For corners that are very close together, the text may overlap. A more
    # complicated approach would be necessary to reliably prevent this.
    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"
        ax.text(corner['Distance'], v_min-30, txt,
                va='center_baseline', ha='center', size='small')

    ax.set_xlabel('Distance in m')
    ax.set_ylabel('Speed in km/h')
    ax.legend()

    # Manually adjust the y-axis limits to include the corner numbers, because
    # Matplotlib does not automatically account for text that was manually added.
    ax.set_ylim([v_min - 40, v_max + 20])

    plt.show()
