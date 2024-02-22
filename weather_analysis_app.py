import requests
import json
from datetime import datetime, timedelta
import statistics
import csv

# Function to fetch current weather data
def get_current_weather(city):
    api_key = 'b68a13e3121841c58dd94150242002'
    base_url = 'http://api.weatherapi.com/v1/current.json'
    params = {'key': api_key, 'q': city}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad requests
        data = response.json()
        return data['current']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching current weather data: {e}")
        return None

# Function to fetch historical weather data for the last seven days
def get_historical_weather(city):
    api_key = 'b68a13e3121841c58dd94150242002'  # Replace 'YOUR_API_KEY' with your actual API key
    base_url = 'http://api.weatherapi.com/v1/history.json'
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    
    params = {'key': api_key, 'q': city, 'dt': start_date, 'end_dt': end_date}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['forecast']['forecastday']
    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical weather data: {e}")
        return None

# Function to calculate average, median, and mode of temperature
def calculate_statistics(temperature_data):
    temperatures = [day['day']['avgtemp_c'] for day in temperature_data]
    avg_temperature = statistics.mean(temperatures)
    median_temperature = statistics.median(temperatures)
    mode_temperature = statistics.mode(temperatures)
    
    return avg_temperature, median_temperature, mode_temperature

# Function to save data and statistical analysis results to a file
def save_to_file(city, current_weather, historical_data, statistics_result):
    filename = f"{city}_weather_data.csv"
    
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write current weather data
        writer.writerow(['Current Weather'])
        writer.writerow(['Time', 'Temperature (C)', 'Condition'])
        writer.writerow([current_weather['last_updated'], current_weather['temp_c'], current_weather['condition']['text']])
        writer.writerow([])  # Add an empty line
        
        # Write historical weather data
        writer.writerow(['Historical Weather'])
        writer.writerow(['Date', 'Temperature (C)'])
        for day in historical_data:
            writer.writerow([day['date'], day['day']['avgtemp_c']])
        
        # Write statistical analysis results
        writer.writerow([])  # Add an empty line
        writer.writerow(['Statistical Analysis'])
        writer.writerow(['Average Temperature', 'Median Temperature', 'Mode Temperature'])
        writer.writerow(statistics_result)

if __name__ == "__main__":
    # User input
    city = input("Enter the name of the city: ").strip()
    
    # Validate user input
    if not city:
        print("City name cannot be empty.")
    else:
        # Fetch current weather data
        current_weather = get_current_weather(city)
        
        if current_weather:
            # Fetch historical weather data
            historical_data = get_historical_weather(city)
            
            if historical_data:
                # Calculate statistics
                avg_temp, median_temp, mode_temp = calculate_statistics(historical_data)
                
                # Display results to the user
                print(f"\nCurrent Weather in {city}:")
                print(f"Temperature: {current_weather['temp_c']}°C")
                print(f"Condition: {current_weather['condition']['text']}")
                
                print("\nHistorical Weather for the Last Seven Days:")
                for day in historical_data:
                    print(f"{day['date']}: {day['day']['avgtemp_c']}°C")
                
                print("\nStatistical Analysis:")
                print(f"Average Temperature: {avg_temp}°C")
                print(f"Median Temperature: {median_temp}°C")
                print(f"Mode Temperature: {mode_temp}°C")
                
                # Save results to a file
                save_to_file(city, current_weather, historical_data, [avg_temp, median_temp, mode_temp])
                print("Results saved to file.")
            else:
                print(f"Unable to fetch historical weather data for {city}.")
        else:
            print(f"Unable to fetch current weather data for {city}.")
