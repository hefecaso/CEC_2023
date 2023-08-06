import ISS_Info
import turtle
import time
import threading
import math
import urllib.request as url
import json
import ephem
from datetime import datetime, timezone

from os import system
import os

screen = turtle.Screen()
screen.title("ISS TRACKER")
screen.setup(720,360)
screen.setworldcoordinates(-180,-90,180,90)
screen.bgpic("world.png")
screen.register_shape("iss.gif")

iss = turtle.Turtle()
iss.shape("iss.gif")
iss.penup()

gt = turtle.Turtle()
gt.penup()

cerco = turtle.Turtle()
cerco.speed(0)
cerco.pensize(2)
cerco.penup()

# Coordenadas del contorno de Guatemala (Ejemplo aproximado, reemplaza con las coordenadas reales)
guatemala_coords = [
    (-92.236328125, 17.22475820662464),
    (-89.033203125, 17.22475820662464),
    (-89.033203125, 15.87962060502676),
    (-92.236328125, 15.87962060502676),
    (-92.236328125, 17.22475820662464),  # Regresamos al punto inicial para cerrar el cerco
]

def dibujar_cerco():
    for i, coord in enumerate(guatemala_coords):
        lon, lat = coord
        if i == 0:
            cerco.goto(lon, lat)
            cerco.pendown()
        else:
            cerco.goto(lon, lat)

def pasoISS():
    try:
        latitud = 15.783471  # Latitud de Guatemala
        longitud = -90.230759  # Longitud de Guatemala
        n = 6  # número de veces que pasará la ISS
        Pass = url.Request('http://api.open-notify.org/iss-pass.json?lat={}&lon={}&n={}'.format(latitud, longitud, n))
        response_Pass = url.urlopen(Pass)
        Pass_obj = json.loads(response_Pass.read())
        if "response" in Pass_obj:
            pass_list = []
            for count, item in enumerate(Pass_obj["response"], start=0):
                pass_list.append(item['risetime'])
                print("Proximos pases sobre Guatemala")
                print(datetime.fromtimestamp(item['risetime']).strftime('%d-%m-%Y %H:%M:%S'))
        else:
            print("Error: No se encontró la clave 'response' en el objeto recibido.")
    except Exception as e:
        print("Error al obtener los datos de la API:", str(e))


def tracker():
    try:
        latitud = 15.783471  # Latitud de Guatemala
        longitud = -90.230759  # Longitud de Guatemala

        while True:
            location = ISS_Info.iss_current_loc()
            lat = location['iss_position']['latitude']
            lon = location['iss_position']['longitude']
            screen.title("ISS TRACKER: (Latitude: {},  Longitude: {})".format(lat, lon))
            iss.goto(float(lon), float(lat))
            iss.pencolor("red")
            iss.dot()

            cerco.pencolor("magenta")
            cerco.dot(cerco.goto(float(-107.324236), float(19.819178)))
            cerco.dot(cerco.goto(float(-76.671761), float(20.143828)))
            cerco.dot(cerco.goto(float(-76.671761), float(10.808493)))
            cerco.dot(cerco.goto(float(-109.107194), float(6.09958)))
            cerco.dot(cerco.goto(float(-107.324236), float(19.819178)))

            
            time.sleep(0.5)

    except Exception as e:
        print("Error en el seguimiento de la ISS:", str(e))



system(f"gnome-terminal -- python3 EFIS_4.py ")
# La creación del hilo debe pasarse sin los paréntesis para que el target sea la función, no su resultado.
t = threading.Thread(target=tracker)
t.start()

# Ocultar la flecha de la ISS
#iss.hideturtle()

# Dibujar el cerco al inicio
dibujar_cerco()

# Llamamos pasoISS fuera del hilo para obtener los pases sobre Guatemala.
pasoISS()

turtle.done()