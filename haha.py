import os
import sys
import time
import threading
from PIL import Image
import pygame
import queue

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
        while not pygame.event.peek((pygame.KEYDOWN, pygame.USEREVENT)):
            if is_gif:
                for frame in frames:
                    resized_frame = frame.resize(screen_size, Image.ANTIALIAS)
                    frame_surface = pygame.image.fromstring(resized_frame.tobytes(), resized_frame.size, resized_frame.mode)
                    screen.blit(frame_surface, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(image.info['duration'])

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
                            return

                    if duration > 0 and time.time() - start_time >= duration:
                        return
            else:
                screen.blit(image, (0, 0))
                pygame.display.flip()

                if duration > 0 and time.time() - start_time >= duration:
                    return

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.USEREVENT:
                    return

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def display_images(image_queue):
    while True:
        image_path, duration = image_queue.get()
        if image_path is None:
            break
        show_image(image_path, duration)

def schedule_image(image_queue, image_path, duration):
    image_queue.put((image_path, duration))

def close_image_after_delay(delay):
    time.sleep(delay)
    pygame.event.post(pygame.event.Event(pygame.USEREVENT))

if __name__ == "__main__":
    images = [("example.gif", 5), ("dart.gif", 3), ("match.gif", 4)]  # Hier die Pfade und Anzeigedauern zu Ihren Bildern angeben (gif, png, jpg oder jpeg)

    image_queue = queue.Queue()

    # Starte den Hauptanzeigethread
    display_thread = threading.Thread(target=display_images, args=(image_queue,))
    display_thread.start()

    for image_path, duration in images:
        # Füge das Bild in die Warteschlange ein
        schedule_image(image_queue, image_path, duration)

        # Starte den Thread, der das Schließen der Anzeige auslöst
        close_thread = threading.Thread(target=close_image_after_delay, args=(duration,))
        close_thread.start()
        close_thread.join()

    # Beende den Hauptanzeigethread
    image_queue.put((None, 0))
    display_thread.join()