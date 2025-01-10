


import random
import json
import threading
import time
import pandas as pd
import paho.mqtt.client as mqtt

# MQTT setup
broker = "broker.hivemq.com"
port = 1883
topic = "home/environment"

# Load dataset
data = pd.read_csv('Crop_recommendation.csv')
rice_data = data[data['label'] == 'rice']

# Exit flag for stopping threads
exit_flag = threading.Event()

# Function to check if conditions are suiq
# qtable for rice
def compare_conditions(real_temp, real_humidity, real_rainfall, real_ph):
    # Ideal ranges for rice from dataset
    temp_min, temp_max = rice_data['temperature'].min(), rice_data['temperature'].max()
    humidity_min, humidity_max = rice_data['humidity'].min(), rice_data['humidity'].max()
    rain_min, rain_max = rice_data['rainfall'].min(), rice_data['rainfall'].max()
    ph_min, ph_max = rice_data['ph'].min(), rice_data['ph'].max()

    # Check suitability
    temp_suitable = temp_min <= real_temp <= temp_max
    humidity_suitable = humidity_min <= real_humidity <= humidity_max
    rainfall_suitable = rain_min <= real_rainfall <= rain_max
    ph_suitable = ph_min <= real_ph <= ph_max

    # Display results in a formatted manner
    print("\n-------------------------------------------------------------")
    print("              Comparison of Real-Time Data                  ")
    print("-------------------------------------------------------------")
    print(f"Temperature: {real_temp:.2f}°C (Ideal: {temp_min:.2f}°C - {temp_max:.2f}°C) - {'Suitable' if temp_suitable else 'Not Suitable'}")
    print(f"Humidity:    {real_humidity:.2f}% (Ideal: {humidity_min:.2f}% - {humidity_max:.2f}%) - {'Suitable' if humidity_suitable else 'Not Suitable'}")
    print(f"Rainfall:    {real_rainfall:.2f}mm (Ideal: {rain_min:.2f}mm - {rain_max:.2f}mm) - {'Suitable' if rainfall_suitable else 'Not Suitable'}")
    print(f"pH:          {real_ph:.2f} (Ideal: {ph_min:.2f} - {ph_max:.2f}) - {'Suitable' if ph_suitable else 'Not Suitable'}")
    print("-------------------------------------------------------------")

    # Determine overall suitability
    if temp_suitable and humidity_suitable and rainfall_suitable and ph_suitable:
        print("             Result: The conditions are SUITABLE for rice.")
    else:
        print("             Result: The conditions are NOT SUITABLE for rice.")
    print("-------------------------------------------------------------\n")

# MQTT publishing function (sensor simulation)
def publish_sensor_data():
    client = mqtt.Client()
    client.connect(broker, port)
    while not exit_flag.is_set():
        data = {
            "temperature": random.uniform(20.0, 35.0),
            "humidity": random.uniform(50.0, 90.0),
            "light": random.uniform(300.0, 800.0),
            "rainfall": random.uniform(50.0, 400.0),
            "ph": random.uniform(5.0, 8.0)
        }
        client.publish(topic, json.dumps(data))
        print("\n-------------------------------------------------------------")
        print(f"Published Data: {data}")
        print("-------------------------------------------------------------")
        time.sleep(5)
    client.disconnect()

# MQTT on_message function
def on_message(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("\n-------------------------------------------------------------")
    print(f"Received Data: {payload}")
    print("-------------------------------------------------------------")
    compare_conditions(
        real_temp=payload["temperature"],
        real_humidity=payload["humidity"],
        real_rainfall=payload["rainfall"],
        real_ph=payload["ph"]
    )

# MQTT subscriber function
def mqtt_subscribe():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(topic)
    while not exit_flag.is_set():
        client.loop(timeout=1.0)  # Allows checking the exit flag each loop

# Keyboard listener function to stop the program
def keyboard_listener():
    input("\nPress 'q' to quit...\n")
    exit_flag.set()
    print("\n-------------------------------------------------------------")
    print("                     Exiting program...                     ")
    print("-------------------------------------------------------------")

# Main function to start threads
if __name__ == '__main__':
    # Start MQTT publisher in a separate thread
    publish_thread = threading.Thread(target=publish_sensor_data)
    publish_thread.start()

    # Start MQTT subscriber in a separate thread
    subscribe_thread = threading.Thread(target=mqtt_subscribe)
    subscribe_thread.start()

    # Start keyboard listener thread to allow quitting
    keyboard_thread = threading.Thread(target=keyboard_listener)
    keyboard_thread.start()

    # Wait for threads to complete
    publish_thread.join()
    subscribe_thread.join()
    keyboard_thread.join()









#
# # Function to determine the best district for rice growth
# def best_district_for_rice():
#     # Check if dataset has required column
#     if 'district' in data.columns:
#         # Filter dataset for rice and group by district to find mean values
#         district_growth = rice_data.groupby('district')[['temperature', 'humidity', 'rainfall', 'ph']].mean()
#
#         # Calculate the average growth score for each district (normalized to equal weights)
#         district_growth['growth_score'] = (
#             district_growth['temperature'].apply(lambda x: (x - rice_data['temperature'].min()) / (rice_data['temperature'].max() - rice_data['temperature'].min())) +
#             district_growth['humidity'].apply(lambda x: (x - rice_data['humidity'].min()) / (rice_data['humidity'].max() - rice_data['humidity'].min())) +
#             district_growth['rainfall'].apply(lambda x: (x - rice_data['rainfall'].min()) / (rice_data['rainfall'].max() - rice_data['rainfall'].min())) +
#             district_growth['ph'].apply(lambda x: (x - rice_data['ph'].min()) / (rice_data['ph'].max() - rice_data['ph'].min()))
#         ) / 4  # Average the scores
#
#         # Find the district with the highest growth score
#         best_district = district_growth['growth_score'].idxmax()
#         best_score = district_growth.loc[best_district, 'growth_score']
#
#         print("\n-------------------------------------------------------------")
#         print(f"Best District for Rice Growth: {best_district}")
#         print(f"Growth Score: {best_score:.2f}")
#         print("-------------------------------------------------------------")
#     else:
#         print("\n-------------------------------------------------------------")
#         print("Dataset does not contain a 'district' column.")
#         print("Please ensure the dataset has district information to perform this analysis.")
#         print("-------------------------------------------------------------")
#
# # Call the function to display results
# if __name__ == '__main__':
#     # Display best district for rice growth
#     best_district_for_rice()
#
#     # Start MQTT publisher in a separate thread
#     publish_thread = threading.Thread(target=publish_sensor_data)
#     publish_thread.start()
#
#     # Start MQTT subscriber in a separate thread
#     subscribe_thread = threading.Thread(target=mqtt_subscribe)
#     subscribe_thread.start()
#
#     # Start keyboard listener thread to allow quitting
#     keyboard_thread = threading.Thread(target=keyboard_listener)
#     keyboard_thread.start()
#
#     # Wait for threads to complete
#     publish_thread.join()
#     subscribe_thread.join()
#     keyboard_thread.join()










#
#
# import pandas as pd
#
# def best_district_for_rice():
#     # Load the dataset
#     file_path = 'combined_district_weather_dataset.csv'
#     data = pd.read_csv(file_path)
#
#     # Ensure required columns exist
#     required_columns = ['District', 'Temperature (°C)', 'Rainfall (mm)', 'Agricultural_Growth_Rate_%']
#     if all(col in data.columns for col in required_columns):
#         # Group by district and calculate mean values for relevant factors
#         district_growth = data.groupby('District')[['Temperature (°C)', 'Rainfall (mm)', 'Agricultural_Growth_Rate_%']].mean()
#
#         # Normalize each factor and calculate a growth score
#         district_growth['growth_score'] = (
#             district_growth['Temperature (°C)'].apply(lambda x: (x - data['Temperature (°C)'].min()) / (data['Temperature (°C)'].max() - data['Temperature (°C)'].min())) +
#             district_growth['Rainfall (mm)'].apply(lambda x: (x - data['Rainfall (mm)'].min()) / (data['Rainfall (mm)'].max() - data['Rainfall (mm)'].min())) +
#             district_growth['Agricultural_Growth_Rate_%'].apply(lambda x: (x - data['Agricultural_Growth_Rate_%'].min()) / (data['Agricultural_Growth_Rate_%'].max() - data['Agricultural_Growth_Rate_%'].min()))
#         ) / 3  # Average the scores
#
#         # Find the district with the highest growth score
#         best_district = district_growth['growth_score'].idxmax()
#         best_score = district_growth.loc[best_district, 'growth_score']
#
#         print("\n-------------------------------------------------------------")
#         print(f"Best District for Rice Growth: {best_district}")
#         print(f"Growth Score: {best_score:.2f}")
#         print("-------------------------------------------------------------")
#     else:
#         print("\n-------------------------------------------------------------")
#         print("Dataset does not contain required columns: District, Temperature (°C), Rainfall (mm), Agricultural_Growth_Rate_%.")
#         print("Please ensure the dataset has these columns to perform this analysis.")
#         print("-------------------------------------------------------------")



