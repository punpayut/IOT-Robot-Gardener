from datetime import datetime
import requests

state = False

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
    with open("setting.txt", "r") as file:
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

while True:
    now = str(datetime.now())[11:16]
    camera_time = settings["camera_time"]
    
    if camera_time == now and not state:
        try:
            requests.post('http://127.0.0.1:5000/camera')
            state = True

        except:
            print("Camera connection error")
    
    if camera_time != now:
        state = False
