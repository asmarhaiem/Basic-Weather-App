import tkinter as tk
from tkinter import messagebox, ttk
import requests
import matplotlib.pyplot as plt

def get_weather(location):
    # Get latitude and longitude
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
    geocode_response = requests.get(geocode_url)

    if geocode_response.status_code == 200:
        results = geocode_response.json()
        if results['results']:
            latitude = results['results'][0]['latitude']
            longitude = results['results'][0]['longitude']

            # Get current weather
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true"
            weather_response = requests.get(weather_url)
            if weather_response.status_code == 200:
                return weather_response.json()
            else:
                print("Error fetching weather data.")
                messagebox.showerror("Error", "Error fetching weather data.")
        else:
            messagebox.showerror("Error", "Location not found.")
    else:
        messagebox.showerror("Error", "Error in geocoding request.")

def display_weather():
    location = location_entry.get()
    weather_data = get_weather(location)

    if weather_data:
        current_weather = weather_data['current_weather']
        temperature = current_weather['temperature']
        weather_description = current_weather['weathercode']

        # Unit conversion
        if unit_combobox.get() == "Fahrenheit":
            temperature = temperature * 9/5 + 32

        # Clear previous weather info
        output_text.delete(1.0, tk.END)

        # Display the current weather details
        output_text.insert(tk.END, f"Current weather in {location}:\n")
        output_text.insert(tk.END, f"Temperature: {temperature:.1f} °{unit_combobox.get()[0]}\n")
        output_text.insert(tk.END, f"Conditions: {get_weather_description(weather_description)}\n")

        # Plot temperature
        plot_temperature(temperature)

def get_weather_description(weather_code):
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Drizzle",
        53: "Light rain",
        61: "Rain",
        63: "Heavy rain",
        80: "Showers",
        81: "Heavy showers",
        82: "Violent showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_descriptions.get(weather_code, "Unknown weather condition")

def plot_temperature(current_temperature):
    # Data for visualization
    temperatures = [current_temperature, current_temperature + 1, current_temperature + 2]  # Dummy data for illustration
    days = ['Today', 'Tomorrow', 'Day After Tomorrow']

    plt.figure(figsize=(6, 4))
    plt.plot(days, temperatures, marker='o')
    plt.title('Temperature Forecast')
    plt.xlabel('Days')
    plt.ylabel('Temperature (°C or °F)')
    plt.grid(True)
    plt.ylim(min(temperatures) - 5, max(temperatures) + 5)
    plt.axhline(y=current_temperature, color='r', linestyle='--', label='Current Temperature')
    plt.legend()
    plt.show()

# Create the main window
root = tk.Tk()
root.title("Weather App")

# Create and place the widgets
tk.Label(root, text="Enter City Name:").pack()

location_entry = tk.Entry(root)
location_entry.pack()

# Dropdown for temperature unit selection
unit_label = tk.Label(root, text="Select temperature unit:")
unit_label.pack()

unit_combobox = ttk.Combobox(root, values=["Celsius", "Fahrenheit"])
unit_combobox.set("Celsius")  # Default selection
unit_combobox.pack()

fetch_button = tk.Button(root, text="Get Weather", command=display_weather)
fetch_button.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

# Start the GUI event loop
root.mainloop()
