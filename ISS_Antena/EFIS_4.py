import pygame
import requests
import time
import math

pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Altitud máxima en km
MAX_ALTITUDE = 420

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electronic Flight Instrument System (EFIS)")

font_large = pygame.font.SysFont("Arial", 32)
font_small = pygame.font.SysFont("Arial", 24)

# Coordenadas del centro del círculo de azimut
center_x, center_y = 400, 350

# Coordenadas del contorno de Guatemala (Ejemplo aproximado)
guatemala_coords = [
    (-107.324236, 19.819178),
    (-76.671761, 20.143828),
    (-76.671761, 10.808493),
    (-109.107194, 6.09958),
    (-107.324236, 19.819178),  # Regresamos al punto inicial para cerrar el cerco
]

# Definimos los límites del cerco virtual de Guatemala
min_lon = min(coord[0] for coord in guatemala_coords)
max_lon = max(coord[0] for coord in guatemala_coords)
min_lat = min(coord[1] for coord in guatemala_coords)
max_lat = max(coord[1] for coord in guatemala_coords)

# Tamaño del círculo de azimut (1/5 de la pantalla)
azimuth_radius = HEIGHT // 4

def is_iss_over_guatemala(latitude, longitude):
    # Verificar si las coordenadas de la ISS están dentro del cerco virtual de Guatemala
    return min_lon <= longitude <= max_lon and min_lat <= latitude <= max_lat

def draw_efis(speed, altitude, latitude, longitude):
    screen.fill(BLACK)

    # Dibuja la pantalla EFIS
    pygame.draw.rect(screen, WHITE, (50, 50, 700, 500), 2)

    # Dibuja los indicadores de velocidad y altitud
    speed_indicator = font_large.render(str(speed) + " km/h", True, BLUE)
    screen.blit(speed_indicator, (100, 100))

    altitude_indicator = font_large.render(str(round(altitude, 2)) + " km", True, GREEN)
    screen.blit(altitude_indicator, (600, 100))

    # Dibuja los datos de posición de la ISS
    position_text = font_small.render("Latitude: {:.4f}°  Longitude: {:.4f}°".format(latitude, longitude), True, WHITE)
    screen.blit(position_text, (100, 570))

    # Dibuja la barra de altitud
    altitude_bar_height = int((altitude / MAX_ALTITUDE) * 450)
    pygame.draw.rect(screen, GREEN, (750, 100 + 450 - altitude_bar_height, 20, altitude_bar_height))

    # Dibuja el círculo de azimut solo si la ISS está sobre Guatemala
    #if is_iss_over_guatemala(latitude, longitude):
    draw_azimuth_circle()

    pygame.display.flip()

def draw_azimuth_circle():
    azimut = math.degrees(math.atan2(center_y - max_lat, center_x - min_lon))
    azimut = (azimut + 360) % 360

    pygame.draw.circle(screen, RED, (center_x, center_y), azimuth_radius, 2)
    pygame.draw.arc(screen, RED, (center_x - azimuth_radius, center_y - azimuth_radius, 2 * azimuth_radius, 2 * azimuth_radius), math.radians(0), math.radians(azimut), 2)

def get_iss_data():
    try:
        url = "https://api.wheretheiss.at/v1/satellites/25544"
        response = requests.get(url)
        data = response.json()

        latitude = data.get("latitude", 0)
        longitude = data.get("longitude", 0)
        velocity = data.get("velocity", 0)  # Velocidad en km/h
        altitude = data.get("altitude", 0)  # Altitud en km

        return latitude, longitude, velocity, altitude

    except requests.exceptions.RequestException as e:
        print("Error al obtener los datos de la ISS:", str(e))
        return 0, 0, 0, 0

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        latitude, longitude, velocity, altitude = get_iss_data()

        if latitude is not None and longitude is not None:
            draw_efis(velocity, altitude, latitude, longitude)

        time.sleep(1)

    pygame.quit()

if __name__ == "__main__":
    main()
