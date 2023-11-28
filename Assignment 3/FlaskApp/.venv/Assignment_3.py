from model.smart_device import SmartDevice, LightBulb, Home 
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)
# Step 6
@app.route('/')
def index():
    home = Home("204 Pitt St.")
    lrBulb = LightBulb("Living Room Light", "Philips", 50)
    frBulb = LightBulb("Family Room Main Light", "Philips", 75)
    bedRoomStrip = LightBulb("Bed Room LED LightStrip", "Govee", 100)
    kitchenTube = LightBulb("Kitchen Tube Light", "GE", 25)

    home.add_device(lrBulb)
    home.add_device(frBulb)
    home.add_device(bedRoomStrip)
    home.add_device(kitchenTube)

    return render_template('home.html', home = home)

# Step 8
@app.route('/add_lightbulb', methods = ['POST'])
def add_lightbulb():
    data = request.get_json()
    name = data.get('name')
    manufacturer = data.get('manufacturer')
    brightness = data.get('brightness')

    lightbulb = LightBulb(name, manufacturer, brightness)

    with open('light.json', 'w') as json_file:
        json.dump(lightbulb.to_json(), json_file)
    return jsonify({'message' : 'Lightbulb added successfully'})

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 8000, debug=True)