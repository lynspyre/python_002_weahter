# Import dependencies
import requests
import json
import datetime
import time

apiKey = "4c84891dd5a264c93da2f738478d8b69"  # https://openweathermap.org/api/


# Initializes cities JSON
def checkForJSON():
    # Try to read the JSON file
    try:
        with open("cities.json", "r") as db:
            db.read()
    # If file not found, creates it
    except FileNotFoundError:
        with open("cities.json", "w") as db:
            db.write("[]")


# Show JSON file containing user's cities
def showCities():
    with open("cities.json", "r") as db:
        cities = json.load(db)
        return cities


# Add a new city to the user's JSON dataset
def addCity():
    print("City name example: Santo Domingo")
    city = input("Enter city name: ")
    print("Country example: DO")
    country = input("Enter the country code in ISO format: ")
    newData = {"city": city, "country": country}
    # Opens the JSON file in read-only mode
    with open("cities.json", "r") as db:
        cities = json.load(db)  # Reads its content
        cities.append(newData)  # Converts it into python object format
    # Opens the JSON file in overwrite mode
    with open("cities.json", "w") as db:
        json.dump(cities, db, indent=4)  # Copy the data and formats it to JSON
    print("City succesfully added!")
    startMenu()


# Menu options for city selection
def citiesSelection():
    # Calls the showCities function
    cities = showCities()
    # If the JSON file is empty asks to add a city
    if len(cities) == 0:
        print("[9] Add a new city: ")
        action = int(input("Select a city: "))
        if action == 9:
            # Calls the addCity function
            addCity()
    # If JSON contains less than 9 cities, shows option to add anothe city
    elif len(cities) > 0 and len(cities) < 9:
        with open("cities.json", "r") as db:
            cities2 = json.load(db)
            for i in range(len(cities2)):
                item = cities2[i]
                city = item["city"]
                country = item["country"]
                print(f"[{i}] {city}, {country}")
            print("[9] Add a new city: ")
            action = int(input("Select a city: "))
            if action == 9:
                addCity()
            else:
                item = cities2[action]
                city = item["city"]
                country = item["country"]
                return (city, country)
    # If JSON contains 9 cities, disables the option to add more
    else:
        with open("cities.json", "r") as db:
            cities2 = json.load(db)
            for i in range(len(cities2)):
                item = cities2[i]
                city = item["city"]
                country = item["country"]
                print(f"[{i}] {city}, {country}")
            action = int(input("Select a city: "))
            item = cities2[action]
            city = item["city"]
            country = item["country"]
            return (city, country)


# Prints the menu options
def startMenu():
    print("[1] Current conditions\n[2] Forecast\n[0] Exit")
    option = int(input("Select an option: "))
    return option


# Get the Latitude and Longitud of a city
def getLatLon(city, country):
    geocodingEndPoint = (f"http://api.openweathermap.org/geo/1.0/direct?\
                         q={city},{country}&limit=1&appid={apiKey}")
    geocodingResponse = requests.get(geocodingEndPoint).json()[0]
    lat = geocodingResponse.get('lat')
    lon = geocodingResponse.get('lon')
    return lat, lon


# Get the curent condition of a city
def currentWeather(city, country):
    lat, lon = getLatLon(city, country)
    currentWeatherEndPoint = (f"https://api.openweathermap.org/data/2.5/\
                              weather?lat={lat}&lon={lon}&appid={apiKey}")
    currentWeatherResponse = requests.get(currentWeatherEndPoint).json()
    weather = currentWeatherResponse.get('weather')[0]
    temp = round((currentWeatherResponse.get('main').get('temp') - 273.15), 1)
    description = weather.get('description').capitalize()
    return temp, description


# Get the forecast condition of a city
def forecastWeather(city, country):
    lat, lon = getLatLon(city, country)
    forecastWeatherEndPoint = (f"https://pro.openweathermap.org/data/2.5/\
                               forecast/hourly?lat={lat}&lon={lon}\
                                &appid={apiKey}")
    forecastWeatherResponse = requests.get(forecastWeatherEndPoint).json()
    weather = forecastWeatherResponse.get('weather')[0]
    temp = round((forecastWeatherResponse.get('main').get('temp') - 273.15), 1)
    description = weather.get('description').capitalize()
    return temp, description


# Compute the user requests
def menuSelection():
    selection = startMenu()
    # Computes the forecast
    if selection == 2:
        print("Forecast")
    # Computes the current weather
    elif selection == 1:
        city, country = citiesSelection()
        temp, description = currentWeather(city, country)
        print(f"City: {city}\nCurrent condition: {description}\
              \nTemperature: {temp}°C")
    # Exits the program
    else:
        print("Bye!")


checkForJSON()
menuSelection()
