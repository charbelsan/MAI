import logging
from logging.handlers import RotatingFileHandler
import pygame.mixer
import random
import pandas as pd

pygame.mixer.init()
def play_mp3(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def setup_logging(log_file):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=5)
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger

def get_circuits(datacsv, only_circuit=True, circuit_name=None):
    data = pd.read_csv(datacsv)
    list_circuits = data["circuit"].unique().tolist()
    if only_circuit and circuit_name == None:
        circuit = random.choice(list_circuits)
        print('random select circuit : ', circuit)
        names = data[data["circuit"] == circuit]["name"].tolist()
        longitudes = data[data["circuit"] == circuit]["longitude"].tolist()
        latitudes = data[data["circuit"] == circuit]["latitude"].tolist()
        resultats= "name"+str(names) + "lat" + str(latitudes) + "lon" + str(longitudes)
    elif only_circuit and circuit_name != None:
        print('select circuit by name : ', circuit_name)
        circuit = circuit_name
        names = data[data["circuit"] == circuit]["name"].tolist()
        longitudes = data[data["circuit"] == circuit]["longitude"].tolist()
        latitudes = data[data["circuit"] == circuit]["latitude"].tolist()
        resultats= "name"+str(names) + "lat" + str(latitudes) + "lon" + str(longitudes)
        
    else:
        print('select all circuits')
        resultats = ""
        for circuit in list_circuits:
            names = data[data["circuit"] == circuit]["name"].tolist()
            longitudes = data[data["circuit"] == circuit]["longitude"].tolist()
            latitudes = data[data["circuit"] == circuit]["latitude"].tolist()
            resultats += "name"+str(names) + "lat" + str(latitudes) + "lon" + str(longitudes) + "#"
    
    return resultats