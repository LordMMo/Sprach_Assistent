import sys
import pygame
from voice_assistant import start, stop

# Initialisieren Pygame
pygame.init()

# begrüßen 
print("Willkommen zum Sprach Assistent")

# Set up the screen
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sprach Assistent")

# Farben
white = (255, 255, 255)
green = (69, 204, 72)
red = (219, 63, 63)
light_gray = (220, 220, 220)
dark_gray = (169, 169, 169)
black = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 40)

# Hintergrund hinzufügen
bg = pygame.image.load("./Fotos/bg1.jpg")

# Start button
start_button_rect = pygame.Rect(50, 300, 200, 100)
start_button_color = green
start_button_text = font.render("Start", True, white)
start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)

# Quit button
quit_button_rect = pygame.Rect(50, 480, 200, 100)
quit_button_color = red
quit_button_text = font.render("Quit", True, white)
quit_button_text_rect = quit_button_text.get_rect(center=quit_button_rect.center)

# Flag zur Anzeige, ob der Sprachassistent ausgeführt wird
voice_assistant_running = False

# Run game loop
running = True

# Hauptschleife (Game Loop)
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            if voice_assistant_running:
                stop()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if start_button_rect.collidepoint(mouse_pos):
                    if not voice_assistant_running:
                        start()
                elif quit_button_rect.collidepoint(mouse_pos):
                    running = False
                    if voice_assistant_running:
                        stop()
                    pygame.quit()
                    sys.exit()

    # Bildschirm leeren
    screen.fill(light_gray)

    # Hintergrund zeichnen
    screen.blit(bg, (0,0))

    # Start-Button zeichnen
    pygame.draw.rect(screen, start_button_color, start_button_rect)
    screen.blit(start_button_text, start_button_text_rect)

    # Quit-Button zeichnen
    pygame.draw.rect(screen, quit_button_color, quit_button_rect)
    screen.blit(quit_button_text, quit_button_text_rect)

    # Update des Bildschirms außerhalb der Schleife
    pygame.display.flip()

# Pygame beenden
pygame.quit()
sys.exit()
