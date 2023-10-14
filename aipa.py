import requests
import json
from PIL import Image
from io import BytesIO
import os
from bardapi import Bard
import time
import matplotlib.pyplot as plt
import numpy as np

c = []

BING_MAPS_API_KEY = 'AkRrxqNaArEmDTjYpWqNJnPWA8Yd0amlUU24Y48bRDid-qKEc98D_00jacJDLo0v'

def get_distance_and_time(origin, destination):
    url = f"https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?"
   
    params = {
        'origins': origin,
        'destinations': destination,
        'travelMode': 'driving',
        'key': BING_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    response_data = response.json()

    if response_data.get("resourceSets"):
        distance = response_data["resourceSets"][0]["resources"][0]["results"][0]["travelDistance"]
        duration = response_data["resourceSets"][0]["resources"][0]["results"][0]["travelDuration"]
        return distance, duration
    else:
        return None, None

# Function to geocode the address string to coordinates
def geocode_address(address):
    url = f"https://dev.virtualearth.net/REST/v1/Locations?"
   
    params = {
        'q': address,
        'key': BING_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    response_data = response.json()

    if response_data.get("resourceSets") and response_data["resourceSets"][0].get("resources"):
        coordinates = response_data["resourceSets"][0]["resources"][0]["point"]["coordinates"]
        return ",".join(map(str, coordinates))
    else:
        return None



    

def get_map_image(origin, destination):
    url = f"https://dev.virtualearth.net/REST/v1/Imagery/Map/Road/Routes?"
   
    params = {
        'wp.0': origin,
        'wp.1': destination,
        'key': BING_MAPS_API_KEY,
        'mapSize': '500,500',
        'format': 'png'
    }

    response = requests.get(url, params=params)
   
    return response.content, response.status_code


def get_distance(origin_address,destination_address):
    
    origin_coordinates = geocode_address(origin_address)
    destination_coordinates = geocode_address(destination_address)

    if origin_coordinates and destination_coordinates:
        distance, duration = get_distance_and_time(origin_coordinates, destination_coordinates)
        if distance is not None and duration is not None:
            hours, minutes = divmod(duration, 60)
            c.append(distance)
            print(f"Distance between {origin_address} and  {destination_address}: {distance} km")
            print(f"Time taken to drive: {int(hours)} hours {int(minutes)} minutes")
       
   
       
            image_data,status_code = get_map_image(origin_coordinates, destination_coordinates)
            tus_code = get_map_image(origin_coordinates, destination_coordinates)
            if status_code == 200:
               
                image = Image.open(BytesIO(image_data))
                image_path = "route_map.png"
                image.save(image_path)
                os.startfile(image_path)
            else:
                print(f"Error fetching image. Status code: {status_code}")


# Main script execution
if __name__ == '__main__':

    os.environ['_BARD_API_KEY']='cAhsae9pR98Ix3KfEgo6PTy1Lzsxr8DfyEoFXFawiuyXzZvn1bNCV5pcfuB6IefFb4SPZw.'
    print("enter location of property")
    a = input()
    print("enter city")
    b = input()

    print(Bard().get_answer("price per square feet of plot 10 years ago in " + a + "in single line")['content'])
    print("\n\n\n\n\n")
    print(Bard().get_answer("current price per square feet of plot in " + a + "in single line" )['content'])
    print("\n\n\n\n\n")
    print(Bard().get_answer("upcoming public projects and price per square feet of plot after 10 years in " + a + "in five lines" )['content'])
    print("\n\n\n\n\n")

    



    
    destination = "chennai central station " 
    get_distance(a, destination)

    destination = "koyambedu bus terminus"
    get_distance(a, destination)

    destination = b + " airport"
    get_distance(a, destination)

    destination = "government hostpital"
    get_distance(a, destination)

def plot_distance_circle(distances, destinations, origin_name):
    # Number of bars
    N = len(distances)

    # Set up the theta values (equally spaced)
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)

    # Colors for the bars
    colors = plt.cm.viridis(np.linspace(0, 1, N))

    # Create the figure and axis
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # Create the bars
    bars = ax.bar(theta, distances, align='center', alpha=0.6, color=colors)

    # Adjust destination labels to give more space for distance values
    ax.set_xticks(theta)
    ax.set_xticklabels(destinations, y=0.01)

    # Add labels with values next to each bar, adjusting positions based on angle
    for i, (angle, r, label) in enumerate(zip(theta, distances, destinations)):
        radial_distance = r + 2
        if angle < np.pi/2:
            ax.text(angle - 0.1, radial_distance, f'{r:.2f}', ha='right', va='center', fontsize=12)
        elif np.pi/2 <= angle < np.pi:
            ax.text(angle + 0.1, radial_distance, f'{r:.2f}', ha='left', va='center', fontsize=12)
        elif np.pi <= angle < 3*np.pi/2:
            ax.text(angle - 0.1, r - 2, f'{r:.2f}', ha='right', va='center', fontsize=12)
        else:
            ax.text(angle + 0.1, r - 2, f'{r:.2f}', ha='left', va='center', fontsize=12)

    # Set a title for the plot
    ax.set_title("Distances from " + a)

    # Display the plot
    plt.show()

# Example data
destinations = ["Chennai Central Station", "Koyambedu Bus Terminus", "Chennai Airport", "Government Hospital"]
distances = c
origin_name = "Your Location"

plot_distance_circle(distances, destinations, a)


