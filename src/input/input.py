import pygame
import pygame_widgets
from pygame_widgets.textbox import TextBox
from pygame_widgets.slider import Slider
import requests

#init GUI
pygame.init()
screen = pygame.display.set_mode((1000,600))
done = False

#light
labelLight = TextBox(
    screen,
    470, 20,
    200, 50,
    fontSize = 30,
    textColour = (255,255,255),
    colour = (0,0,0))
sliderLight = Slider(
    screen,
    100,100,
    800, 20,
    min = 0, max = 100,
    step = 1,
    handleRadius = 30,
    handleColour = ((252,244,3)) )
labelValueLight = TextBox(
    screen,
    475, 150,
    80, 50,
    fontSize = 30,
    textColour = (255,255,255),
    colour = (0,0,0))
labelLED = TextBox(
    screen,
    455, 200,
    100, 50,
    fontSize = 30,
    textColour = (207,206,194),
    colour = (0,0,0) )

#moisture
labelMoisture = TextBox(
    screen,
    450, 320,
    200, 50,
    fontSize = 30,
    textColour = (255,255,255),
    colour = (0,0,0))
sliderMoisture = Slider(
    screen,
    100,400,
    800, 20,
    min = 0, max = 100,
    step = 1,
    handleRadius = 30,
    handleColour = ((0,238,242)) )
labelValueMoisture = TextBox(
    screen,
    475, 450,
    80, 50,
    fontSize = 30,
    textColour = (255,255,255),
    colour = (0,0,0))
labelPump = TextBox(
    screen,
    455, 500,
    100, 50,
    fontSize = 30,
    textColour = (207,206,194),
    colour = (0,0,0) )

settings = {
    "moisture" : 80,
    "light" : 80,
    "camera_time" : "07:00",
    "light_time_start" : "06:00",
    "light_time_end" : "18:00",
    "isLightOn" : True,
    "isPumpOn" : True
    }

try:
    with open("../server/setting.txt", "r") as file:
        for line in file:
            (key, val) = line.split()
            if val.isnumeric():
                settings[key] = int(val)
            elif val == "True":
                settings[key] = True
            elif val == "False":
                settings[key] = False
            else:
                settings[key] = val
            print(key, settings[key])
except IOError:
    print("file not found")
    lines = [key + " " + str(settings[key]) for key in dict.keys(settings)]
    with open("setting.txt", "w") as file:
        file.write("\n".join(lines))
print(settings)

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    #light
    labelLight.setText("Light")
    # labelLight.draw()
    
    sliderLight.listen(events)
    lightValue = sliderLight.getValue()
    # sliderLight.draw()
    
    labelValueLight.setText(lightValue)
    # labelValueLight.draw()
    
    if(lightValue < settings["light"]):
        labelLED.setText("LED ON")
        labelLED.textColour = ((252,244,3))
    else:
        labelLED.setText("LED OFF")
        labelLED.textColour = ((207,206,194))
    # labelLED.draw()
    
    #moisture
    labelMoisture.setText("Moisture")
    # labelMoisture.draw()
    
    # sliderMoisture.listen(events)
    moistureValue = sliderMoisture.getValue()
    # sliderMoisture.draw()
    
    labelValueMoisture.setText(moistureValue)
    # labelValueMoisture.draw()
    
    if(moistureValue < settings["moisture"]):
        labelPump.setText("Pump ON")
        labelPump.textColour = ((0,38,242))
    else:
        labelPump.setText("Pump OFF")
        labelPump.textColour = ((207,206,194))
    # labelPump.draw()
    
    #send data to server
    my_data = ({'Light' : lightValue, 'Moisture': moistureValue})
    
    try:
        req = requests.post('http://127.0.0.1:5000/receiveData', json = my_data)
        print(req.status_code)
    except:
        print("connection error")
    
    pygame_widgets.update(events)
    pygame.display.update()
    screen.fill((0,0,0))
