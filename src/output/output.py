from flask import Flask, request, jsonify, render_template

isLEDOn = True
isPumpOn = True

app = Flask(__name__)

@app.route('/onLED', methods=['GET','POST'])
def onLED():
    global isLEDOn, isPumpOn
    print("LED: On")
    isLEDOn = True
    if isPumpOn:
        print("Pump: On")
    else:
        print("Pump: Off")
    return "onLED"

@app.route('/offLED', methods=['GET','POST'])
def offLED():
    global isLEDOn, isPumpOn
    print("LED: Off")
    isLEDOn = False
    if isPumpOn:
        print("Pump: On")
    else:
        print("Pump: Off")
    return "offLED"

@app.route('/onPump', methods=['GET','POST'])
def onPump():
    global isLEDOn, isPumpOn
    print("Pump: On")
    isPumpOn = True
    if isLEDOn:
        print("LED: On")
    else:
        print("LED: Off")
    return "onPump"

@app.route('/offPump', methods=['GET','POST'])
def offPump():
    global isLEDOn, isPumpOn
    print("Pump: Off")
    isPumpOn = False
    if isLEDOn:
        print("LED: On")
    else:
        print("LED: Off")
    return "offPump"

if __name__ == "__main__":
    app.run(debug=False, port=8080)