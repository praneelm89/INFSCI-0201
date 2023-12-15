import json
from abc import ABC, abstractmethod
import requests

class SmartDevice(ABC):
    def __init__(self, device_id, device_type, manufacturer, location):
        self.device_id = device_id
        self.device_type = device_type
        self.manufacturer = manufacturer
        self.location = location

    @abstractmethod
    def to_json(self):
        pass

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value) # update object attributes
        return self


class Thermostat(SmartDevice):
    def __init__(self, device_id, manufacturer, location, temperature):
        super().__init__(device_id, "Thermostat", manufacturer, location)
        self.temperature = temperature
    
    def getTemp(self):
        return self.temperature
    
    def to_json(self):
        thermostat_dict = {
            'device_id' : self.device_id,
            'device_type' : "Thermostat",
            'manufacturer' : self.manufacturer,
            'location' : self.location,
            'temperature' : self.temperature
        }
        return json.dumps(thermostat_dict)
    


class SmartVacuum(SmartDevice):
    def __init__(self, device_id, manufacturer, location, binStatus):
        super().__init__(device_id, "Smart Vacuum", manufacturer, location)
        self.binStatus = binStatus
        self.binStatusMessage = ""

    def to_json(self):
        SmartVacuum_dict = {
            'device_id' : self.device_id,
            'device_type' : "Smart Vacuum",
            'manufacturer' : self.manufacturer,
            'location' : self.location,
            'binStatus' : self.binStatus
        }
        return json.dumps(SmartVacuum_dict)


    # BinStatus False = Empty or partially filled
    # BinStatus True = Bin Filled
    def setBinStatus(self, binFull):
        self.binStatus = binFull
        return self.binStatus

    def setStatus(self):
        if(self.binStatus):
            self.binStatusMessage = "Bin is Full. Please Empty Bin"
        elif(self.binStatus == False):
            self.binStatusMessage = "Bin is not Full. Bin may be paritally full. Check Bin"
    


class SmartFridge(SmartDevice):
    def __init__(self, device_id, manufacturer, location, city):
        super().__init__(device_id, "Smart Refrigerator", manufacturer, location)
        self.city = city
        self.currentWeather = 0

    def to_json(self):
        smartFridge_dict = {
            'device_id' : self.device_id,
            'device_type' : "Smart Refrigerator",
            'manufacturer' : self.manufacturer,
            'location' : self.location,
            'physical address' : self.city
        }
        return json.dumps(smartFridge_dict)
    
    def getCity(self):
        return self.city
        
    
    # Publicly Available API - Weather API - https://www.weatherapi.com/
    def get_weather(self):
        url = f'http://api.weatherapi.com/v1/current.json?key=50420e80266a48f4aab222504231412&q=' + self.city
        response = requests.get(url)
        data = response.json()
        if data:
            self.currentWeather = data['current']['temp_f']
            return self.currentWeather
        return None

    def setLocalTemperature(self):
        self.localTemperature = self.get_weather()

    

class LightBulb(SmartDevice):
    def __init__(self, device_id, manufacturer, location, brightness):
        super().__init__(device_id, "LightBulb", manufacturer, location)
        self.brightness = brightness
    
    def to_json(self):
        lightBulb_dict = {
            'device_id' : self.device_id,
            'device_type' : "LightBulb",
            'manufacturer' : self.manufacturer,
            'location' : self.location,
            'device brightness' : self.brightness
        }
        return json.dumps(lightBulb_dict)
    
    def adjust_brightness(self, value):
        self.brightness = value
        print("Brightness is set to", value)


class GarageDoor(SmartDevice):
    def __init__(self, device_id, manufacturer, location):
        super().__init__(device_id, "GarageDoor", manufacturer, location)
        self.openStatus = False # Closed by Default
        self.garageDoorMessage = ""

    def to_json(self):
        garageDoor_dict = {
            'device_id' : self.device_id,
            'device_type' : "GarageDoor",
            'manufacturer' : self.manufacturer,
            'location' : self.location,
            'door Open' : self.openStatus
        }
        return json.dumps(garageDoor_dict)

    def openDoor(self):
        self.openStatus = True
        self.setStatus()

    def closeDoor(self):
        self.openStatus = False
        self.setStatus()
    
    def setStatus(self):
        if(self.openStatus):
            self.garageDoorMessage = "Garage Door is Open"
        elif(self.openStatus == False):
            self.garageDoorMessage = "Garage Door is Closed"
    

class Home:
    def __init__(self, address):
        self.address = address
        self.smart_devices = []
        self.num_smart_devices = 0

    def add_device(self, dev):
        self.smart_devices.append(dev)
        self.num_smart_devices += 1
    
    def get_New_DeviceID(self):
        return self.num_smart_devices
        
    def print_devices(self):
        for device in self.smart_devices:
            print(device.to_json())
    
    def update_Device(self, id, data):
        for device in self.smart_devices:
            if device.device_id == id:
                device.update(data)
                return True
        return False 
    
    def delete_Device(self, id):
        for dev in self.smart_devices:
            if dev.device_id == id:
                self.smart_devices.remove(dev)