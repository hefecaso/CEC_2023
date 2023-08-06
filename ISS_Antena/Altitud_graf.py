import pygame
import math
import random
import time

pygame.init()

# Dimensiones de la ventana
WIDTH, HEIGHT = 800, 600

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electronic Flight Instrument System (EFIS)")

font = pygame.font.SysFont("Arial", 24)

def draw_efis(speed, altitude, heading):
    screen.fill(BLACK)

    # Dibuja la pantalla EFIS
    pygame.draw.rect(screen, WHITE, (50, 50, 700, 500), 2)

    # Dibuja las agujas de los indicadores
    pygame.draw.rect(screen, WHITE, (400, 150, 10, 200))
    pygame.draw.rect(screen, WHITE, (450, 150, 10, 200))
    pygame.draw.rect(screen, WHITE, (300, 295, 200, 10))
    pygame.draw.polygon(screen, WHITE, [(400, 300), (410, 280), (390, 280)])
    pygame.draw.polygon(screen, WHITE, [(450, 300), (460, 280), (440, 280)])

    # Dibuja las escalas
    for i in range(0, 200, 20):
        pygame.draw.rect(screen, WHITE, (390, 150 + i, 20, 2))
        pygame.draw.rect(screen, WHITE, (440, 150 + i, 20, 2))
    for i in range(0, 200, 50):
        pygame.draw.rect(screen, WHITE, (390, 150 + i, 30, 2))
        pygame.draw.rect(screen, WHITE, (430, 150 + i, 30, 2))

    # Dibuja los valores de los indicadores
    speed_text = font.render("Speed: {} kts".format(speed), True, BLUE)
    screen.blit(speed_text, (100, 100))

    altitude_text = font.render("Altitude: {} ft".format(altitude), True, GREEN)
    screen.blit(altitude_text, (100, 150))

    heading_text = font.render("Heading: {}°".format(heading), True, RED)
    screen.blit(heading_text, (100, 200))

    pygame.display.flip()

def main():
    speed = 0
    altitude = 0
    heading = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Generar datos simulados para velocidad, altitud y rumbo
        speed = random.randint(100, 500)
        altitude = random.randint(5000, 35000)
        heading = random.randint(0, 360)

        draw_efis(speed, altitude, heading)
        time.sleep(1)

    pygame.quit()

if __name__ == "__main__":
    main()
