from flask import Flask, request, jsonify, render_template, make_response
from datetime import datetime
import os
import google.cloud.dialogflow
import requests
import json
import logging

app = Flask(__name__)
logging.basicConfig(filename='logging.log', filemode = 'a',
                    format='%(asctime)s, %(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S', level=logging.DEBUG)
logging.info('Started')

settings = {
    "moisture" : 80,
    "light" : 80,
    "camera_time" : "07:00",
    "light_time_start" : "06:00",
    "light_time_end" : "18:00",
    "isLightOn" : True,
    "isPumpOn" : True
    }

realtimeValue = {
    "moisture" : None,
    "light" : None
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
print(settings)

if __name__ == "__main__":
    app.run(debug=False, port=5000)
    
def updateSettingFile():
    lines = [key + " " + str(settings[key]) for key in dict.keys(settings)]
    with open("setting.txt", "w") as file:
        file.write("\n".join(lines))
        
def result():
    #build a request object
    req = request.get_json(force=True)
    
    intent = req.get('queryResult').get('intent').get('displayName')
    print(intent)
    
    global settings, realtimeValue
    
    if intent == "monitoring":
        logging.info("Request to monitor sensor value")
        return {'fulfillmentText': 'light intensity = ' +str(realtimeValue["light"])
                +"%\n"+ 'moisture = ' + str(realtimeValue["moisture"]) +"%"}

    if intent == "new setting camera":
        time = req.get('queryResult').get('parameters').get('time')[11:16]
        settings["camera_time"] = time
        updateSettingFile()
        
        logging.info('set camera time: ' + time)
        return {'fulfillmentText' : 'set camera success'}
    
    if intent == "new setting light":
        percentage = req.get('queryResult').get('parameters').get('lightpercentage').rstrip('%')
        startTime = req.get('queryResult').get('parameters').get('period').get('startTime')[11:16]
        endTime = req.get('queryResult').get('parameters').get('period').get('endTime')[11:16]
        
        settings["light"] = percentage
        settings["light_time_start"] = startTime
        settings["light_time_end"] = endTime
        
        updateSettingFile()
        
        logging.info('set light: '+percentage+ 'period: '+startTime+'-'+endTime)
        return {'fulfillmentText' : 'set light success'}
    
    if intent == "new setting moisture":
        percentage = req.get('queryResult').get('parameters').get('moisturepercentage').rstrip('%')
        print("HERE")

        settings["moisture"] = percentage
        updateSettingFile()
        print(settings['moisture'])
        
        logging.info('set moisture: '+percentage)
        return {'fulfillmentText' : 'set moisture success'}
    
    if intent == "setting":
        ans_string = 'setting\n' + 'moisture: '+str(settings["moisture"])+'%\n'+'light: '+str(settings["light"])+'% period: '+ str(settings["light_time_start"])+'-'+str(settings["light_time_end"])+'\n'+'camera time: '+str(settings["camera_time"])
               
        logging.info('request setting value')
        return {'fulfillmentText': ans_string}
    
    return {"fulfillmentText": "this is a text from fulfillment"}

def caltime(time):
    #calculate time
    time = time.strip().split(":")
    return int(time[0])*60 + int(time[1])

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    return make_response(jsonify(result()))

@app.route('/receiveData', methods=['GET','POST'])
def receiveData():
    data = request.get_json()
    
    global settings, realtimeValue
    realtimeValue["moisture"] = data["Moisture"]
    realtimeValue["light"] = data["Light"]
    
    #print(realtimeValue["moisture"], realtimeValue["light"])
    
    logging.info("Add value from sensors to realtimeValue")
    
    #light
    now = str(datetime.now())[11:16]
    if realtimeValue["light"] < settings["light"] and (caltime(now) > caltime(settings["light_time_start"])) and (caltime(now) < caltime(settings["light_time_end"])):
        if not settings["isLightOn"]:
            try:
                requests.post('http://127.0.0.1:8080/onLED')
                print("onLED")
                settings["isLightOn"] = True
                updateSettingFile()
            except:
                print("LED Connection Error")
    else:
        if settings["isLightOn"]:
            try:
                requests.post('http://127.0.0.1:8080/offLED')
                print("offLED")
                settings["isLightOn"] = False
                updateSettingFile()
            except:
                print("LED Connection Error")
    
    #moisture
    if realtimeValue["moisture"] < settings["moisture"]:
        if not settings["isPumpOn"]:
            try:
                requests.post('http://127.0.0.1:8080/onPump')
                print("onPump")
                settings["isPumpOn"] = True
                updateSettingFile()
            except:
                print("Pump Connection Error")
    else:
        if settings["isPumpOn"]:
            try:
                requests.post('http://127.0.0.1:8080/offPump')
                print("offPump")
                settings["isPumpOn"] = False
                updateSettingFile()
            except:
                print("Pump Connection Error")
    
    return "received data is processed"

@app.route('/camera', methods=['GET','POST'])
def camera():
    logging.info('Take Photo')

    return "a"