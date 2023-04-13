import os
import sys
import time
import threading
from PIL import Image
import pygame

pygame.init()

def show_image(image_path, duration=0):
    try:
        image = Image.open(image_path)
        screen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        screen = pygame.display.set_mode(screen_size, pygame.FULLSCREEN)

        if image.format.lower() == 'gif':
            is_gif = True
            frames = []
            try:
                while True:
                    frames.append(image.copy())
                    image.seek(len(frames))
            except EOFError:
                pass
        else:
            is_gif = False
            image = image.resize(screen_size, Image.ANTIALIAS)
            image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

        start_time = time.time()
        should_exit = False
        while not should_exit:
            if is_gif:
                for frame in frames:
                    if should_exit:
                        break

                    # Setze den Hintergrund auf Schwarz
                    screen.fill((0, 0, 0))

                    resized_frame = frame.resize(screen_size, Image.ANTIALIAS)
                    frame_surface = pygame.image.fromstring(resized_frame.tobytes(), resized_frame.size, resized_frame.mode)
                    screen.blit(frame_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(image.info['duration'])

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
                            should_exit = True
                            break

                    if duration > 0 and time.time() - start_time >= duration:
                        should_exit = True
                        break
            else:
                screen.blit(image, (0, 0))
                pygame.display.flip()

                if duration > 0 and time.time() - start_time >= duration:
                    should_exit = True
                    break

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
                    should_exit = True
                    break

        screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.time.delay(100)  # Eine kurze Verzögerung hinzufügen, um sicherzustellen, dass der schwarze Bildschirm gezeichnet wird

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

        

def close_image_after_delay(delay):
    time.sleep(delay)
    pygame.event.post(pygame.event.Event(pygame.USEREVENT))


if __name__ == "__main__":
    images = ["example.gif", "dart.gif", "match.gif", "idle.jpg"]  # Hier die Pfade zu Ihren Bildern angeben (gif, png, jpg oder jpeg)

    show_image(images[0], duration=6)

    # for image_path in images:
    #     # Starte den Thread, der das Schließen der Anzeige auslöst
    #     close_thread = threading.Thread(target=close_image_after_delay, args=(2,))  # Verzögerung in Sekunden angeben
    #     close_thread.start()

    #     show_image(image_path)

    #     close_thread.join()

    pygame.quit()
