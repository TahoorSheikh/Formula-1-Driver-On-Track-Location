# import libraries 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import fastf1
import pandas as pd

fastf1.Cache.enable_cache('cache')

# Pick year
invalid = True
Year = 0
while(invalid):
    try:
        Year = int(input("Pick the year(2018 - present): "))
    except ValueError:
        print("Please enter a number")
    if Year >= 2018:
        invalid = False

# Season
Season = fastf1.get_event_schedule(Year)

# Pick track
for i in range(len(Season)):
    print(str(Season['Location'][i]))
track = input("Select track: ")

# Pick Race or Quali
types = ['R','Q']
invalid = True
while(invalid):
    type = input("Select session type(R or Q): ")
    if type in types:
        invalid = False

session = fastf1.get_session(Year, track, type)
session.load(telemetry=True, laps=True, weather=False)
track_name = session.session_info['Meeting']['Circuit']['ShortName']

def pick_driver(name):
    if type == 'Q':
        driver = session.laps.pick_drivers(name).pick_fastest().get_telemetry()
    else:
        driver = session.laps.pick_drivers(name).get_telemetry()
    # Position Data
    x = pd.DataFrame(driver['X'])
    y = pd.DataFrame(driver['Y'])
    # Throttle data and brake data
    Throttle = list(driver['Throttle'])
    Brake = list(driver['Brake'])
    # get fastestlap
    try:
        lap_time = session.laps.pick_drivers(name).pick_fastest()[3]
    except TypeError:
        lap_time = None
    return x, y, Throttle, Brake, lap_time

all_laps = session.total_laps
Track_Data = session.laps.pick_driver(session.results['Abbreviation'][0]).pick_fastest().get_telemetry()
race_messages = pd.DataFrame(session.race_control_messages).drop(['Time','Category','Status','Scope','Sector','RacingNumber'],axis=1)

# Track data
x_track = pd.DataFrame(Track_Data['X'])
y_track = pd.DataFrame(Track_Data['Y'])