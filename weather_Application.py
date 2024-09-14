import requests
import json
from datetime import datetime, timedelta
import statistics
import csv
import tkinter as tk
from tkinter import messagebox, filedialog

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
        messagebox.showerror("Error", f"Error fetching current weather data: {e}")
        return None

# Function to fetch historical weather data for the last seven days
def get_historical_weather(city):
    api_key = 'b68a13e3121841c58dd94150242002'
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
        messagebox.showerror("Error", f"Error fetching historical weather data: {e}")
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
    filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if filename:
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
        
        messagebox.showinfo("Success", "Data saved successfully.")

# Function to fetch and display weather data in the GUI
def fetch_weather_data():
    city = city_entry.get().strip()
    
    if not city:
        messagebox.showwarning("Input Error", "City name cannot be empty.")
    else:
        # Fetch current weather data
        current_weather = get_current_weather(city)
        
        if current_weather:
            # Fetch historical weather data
            historical_data = get_historical_weather(city)
            
            if historical_data:
                # Calculate statistics
                avg_temp, median_temp, mode_temp = calculate_statistics(historical_data)
                
                # Display results in the GUI
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, f"\nCurrent Weather in {city}:\n")
                result_text.insert(tk.END, f"Temperature: {current_weather['temp_c']}°C\n")
                result_text.insert(tk.END, f"Condition: {current_weather['condition']['text']}\n")
                
                result_text.insert(tk.END, "\nHistorical Weather for the Last Seven Days:\n")
                for day in historical_data:
                    result_text.insert(tk.END, f"{day['date']}: {day['day']['avgtemp_c']}°C\n")
                
                result_text.insert(tk.END, "\nStatistical Analysis:\n")
                result_text.insert(tk.END, f"Average Temperature: {avg_temp}°C\n")
                result_text.insert(tk.END, f"Median Temperature: {median_temp}°C\n")
                result_text.insert(tk.END, f"Mode Temperature: {mode_temp}°C\n")
                
                # Save results to a file
                save_to_file(city, current_weather, historical_data, [avg_temp, median_temp, mode_temp])

# Creating the GUI window
root = tk.Tk()
root.title("Weather Data Fetcher")

# Create GUI elements
city_label = tk.Label(root, text="Enter City:")
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

fetch_button = tk.Button(root, text="Fetch Weather Data", command=fetch_weather_data)
fetch_button.pack()

result_text = tk.Text(root, height=20, width=80)
result_text.pack()

# Start the GUI event loop
root.mainloop()