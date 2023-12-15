from model.smart_Device import SmartDevice, Thermostat, SmartVacuum, SmartFridge, LightBulb, GarageDoor, Home 
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

home = Home("204 Pitt St.")

# array to store devices using JSON serializaiton
devices = []
global numDevices 



# API endpoints
@app.route('/devices', methods = ['GET'])
def get_Devices():
    return jsonify(devices)

@app.route('/devices/<int:device_id>', methods=['GET'])
def get_Device(device_id):
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if device:
        return jsonify(device)
    return jsonify({'error':'Device not found'}), 404

@app.route('/devices/<int:device_id>', methods = ['PUT'])
def update_Device(device_id):
    device = next((d for d in devices if d['device_id'] == device_id), None)
    if device:
        data = request.json
        device.update(data)
        home.update_Device(device_id, data)
        return jsonify({'message' : 'Device updated successfully'})
    return jsonify({'error' : 'Device not found'}), 404

@app.route('/device/<int:device_id>', methods = ['DELETE'])
def delete_Device(device_id):
    global devices
    devices = [d for d in devices if d['device_id'] != device_id]
    home.delete_Device(device_id)
    return jsonify({'message' : 'Device deleted successfully'})


@app.route('/devices/html', methods = ['GET'])
def get_Devices_HTML():
    return render_template('devices.html', home = home)

@app.route('/')
def index():
    return render_template('home.html', home = home)

# Device Sub Links

@app.route('/lightbulbs')
def list_lightbulbs():
    return render_template('lightbulbs.html', home = home)

@app.route('/thermostats')
def list_thermostats():
    return render_template('thermostats.html', home = home)

@app.route('/vacuums')
def list_vacuums():
    return render_template('vacuums.html', home = home)

@app.route('/fridges')
def list_fridges():
    return render_template('fridges.html', home = home)

@app.route('/garagedoors')
def list_garagedoors():
    return render_template('garagedoors.html', home = home)


@app.route('/add_lightbulb', methods = ['POST'])
def add_lightbulb():
    data = request.get_json()
    id = home.get_New_DeviceID()
    manufacturer = data.get('manufacturer')
    location = data.get('location')
    brightness = data.get('brightness')

    lightbulb = LightBulb(id, manufacturer, location, brightness)

    home.add_device(lightbulb)

    # Save new objects to a file for data persistence
    with open('light.json', 'w') as json_file:
        json.dump(lightbulb.to_json(), json_file)
    return jsonify({'message' : 'Lightbulb added Successfully'}), 201

@app.route('/add_smart_vacuum', methods = ['POST'])
def add_smart_vacuum():
    data = request.get_json()
    id = home.get_New_DeviceID()
    manufacturer = data.get('manufacturer')
    location = data.get('location')
    binStatus = data.get('binStatus')

    vacuum = SmartVacuum(id, manufacturer, location, binStatus)
    vacuum.setStatus()
    home.add_device(vacuum)

    # Save new objects to a file for data persistence
    with open('vacuum.json', 'w') as json_file:
        json.dump(vacuum.to_json(), json_file)
    return jsonify({'message' : 'Smart Vacuum added Successfully'}), 201

@app.route('/add_smart_fridge', methods = ['POST'])
def add_smart_fridge():
    data = request.get_json()
    id = home.get_New_DeviceID()
    manufacturer = data.get('manufacturer')
    location = data.get('location')
    city = data.get('city')

    fridge = SmartFridge(id, manufacturer, location, city)
    fridge.setLocalTemperature()
    home.add_device(fridge)

    # Save new objects to a file for data persistence
    with open('fridge.json', 'w') as json_file:
        json.dump(fridge.to_json(), json_file)
    return jsonify({'message' : 'Smart Fridge added Successfully'}), 201
    
@app.route('/add_garage_door', methods = ['POST'])
def add_garage_door():
    data = request.get_json()
    id = home.get_New_DeviceID()
    manufacturer = data.get('manufacturer')
    location = data.get('location')

    garageDoor = GarageDoor(id, manufacturer, location)
    garageDoor.openDoor()
    garageDoor.setStatus()
    home.add_device(garageDoor)

    # Save new objects to a file for data persistence
    with open('garageDoor.json', 'w') as json_file:
        json.dump(garageDoor.to_json(), json_file)
    return jsonify({'message' : 'Smart Garage Door Opener added Successfully'}), 201

@app.route('/add_thermostat', methods = ['POST'])
def add_thermostat():
    data = request.get_json()
    id = home.get_New_DeviceID()
    manufacturer = data.get('manufacturer')
    location = data.get('location')
    temperature = data.get('temperature')
    
    thermo = Thermostat(id, manufacturer, location, temperature)
    home.add_device(thermo)

    # Save new objects to a file for data persistence
    with open('thermostat.json', 'w') as json_file:
        json.dump(thermo.to_json(), json_file)
    return jsonify({'message' : 'Thermostat added Successfully'}), 201

# Driver code
if __name__ == '__main__':
    thermostat = Thermostat(home.get_New_DeviceID(), "Google Nest", "Living Room", 68)
    devices.append({'device_id': 0, 'device_type': "Thermostat", 'manufacturer': 'Google Nest', 'location': 'Living Room', 'temperature': 68})
    home.add_device(thermostat)

    smart_vacuum = SmartVacuum(home.get_New_DeviceID(), "iRobot", "Kitchen", False)
    devices.append({'device_id': 1, 'device_type': "Smart Vacuum", 'manufacturer': 'iRobot', 'location': 'Kitchen'})
    smart_vacuum.setStatus()
    home.add_device(smart_vacuum)

    mainFridge = SmartFridge(home.get_New_DeviceID(), "Samsung", "Kitchen", "Pittsburgh")
    devices.append({'device_id': 2, 'device_type': "Smart Refrigerator", 'manufacturer': 'Samsung', 'location': 'Kitchen'})
    mainFridge.setLocalTemperature()
    home.add_device(mainFridge)

    basementFridge = SmartFridge(home.get_New_DeviceID(), "LG", "Basement", "Pittsburgh")
    devices.append({'device_id': 3, 'device_type': "Smart Refrigerator", 'manufacturer': 'LG', 'location': 'Basement'})
    basementFridge.setLocalTemperature()
    home.add_device(basementFridge)

    drinkFridge = SmartFridge(home.get_New_DeviceID(), "Samsung", "Man Cave", "Pittsburgh")
    devices.append({'device_id': 4, 'device_type': "Smart Refrigerator", 'manufacturer': 'Samsung', 'location': 'Man Cave'})    
    drinkFridge.setLocalTemperature()
    home.add_device(drinkFridge)

    lb_Kitchen = LightBulb(home.get_New_DeviceID(), "Philips", "Kitchen", 75)
    devices.append({'device_id': 5, 'device_type': "LightBulb", 'manufacturer': 'Philips', 'location': 'Kitchen'})
    home.add_device(lb_Kitchen)

    lb_Basement = LightBulb(home.get_New_DeviceID(), "Philips", "Basement", 50)
    devices.append({'device_id': 6, 'device_type': "LightBulb", 'manufacturer': 'Philips', 'location': 'Basement'})
    home.add_device(lb_Basement)

    lb_ManCave = LightBulb(home.get_New_DeviceID(), "Govee", "Man Cave", 100)
    devices.append({'device_id': 7, 'device_type': "LightBulb", 'manufacturer': 'Govee', 'location': 'Man Cave'})
    home.add_device(lb_ManCave)

    lb_LivRoom = LightBulb(home.get_New_DeviceID(), "Philips", "Living Room", 45)
    devices.append({'device_id': 8, 'device_type': "LightBulb", 'manufacturer': 'Philips', 'location': 'Living Room'})
    home.add_device(lb_LivRoom)

    garageDoor1 = GarageDoor(home.get_New_DeviceID(), "myQ", "Garage")
    devices.append({'device_id': 9, 'device_type': "GarageDoor", 'manufacturer': 'myQ', 'location': 'Garage'})
    garageDoor1.setStatus()
    home.add_device(garageDoor1)

    garageDoor2 = GarageDoor(home.get_New_DeviceID(), "Chamberlain", "Garage")
    devices.append({'device_id': 10, 'device_type': "GarageDoor", 'manufacturer': 'Chamberlain', 'location': 'Garage'})
    garageDoor2.openDoor()
    garageDoor2.setStatus()
    home.add_device(garageDoor2)
    
    numDevices = home.get_New_DeviceID()

    app.run(host = "0.0.0.0", port = 8000, debug=True)