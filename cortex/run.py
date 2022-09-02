import sys
import time
import datetime as dt
from pathlib import Path

import pygame


PHOTO_TICK = 30  # How many seconds to switch images
THIS_DIR = Path(__file__).parent
PHOTOS = """
assets/aps_aerial_photo.jpg
assets/jwst-carina-nebula.jpg
assets/anl_theta.jpg
assets/anl_tem.jpg
assets/lerix.gif
assets/earthrise.webp
assets/jwst_exoplanet.webp
assets/aps_U_high_bay.jpg
assets/breeder_reactor_bulbs.jpg
assets/skelly-s25.jpg
assets/black-hole-photo.webp
""".split()
PHOTOS = [THIS_DIR / f for f in PHOTOS]


BLACK = (0, 0, 0)
TEXT_COLOR = (0, 0, 255)


def show_image(img, screen, display):
    rects = [screen.fill(BLACK)]
    # Scale the image to fit the display
    # Calculate the rectangle needed to center the image
    xy = tuple((X-x)/2 for X, x in zip(screen.get_size(), img.get_size()))
    # Display the image
    rects.append(screen.blit(img, xy))
    # Add text
    font = pygame.font.SysFont("freesanbold.ttf", 50)
    text = font.render(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, TEXT_COLOR)
    rects.append(screen.blit(text, (5, 5)))
    # Update the display with the new image
    # display.flip()
    display.update(rects)


def resize_image(img, screen_size):
    # Determine the new size based on how much space we have
    img_size = img.get_size()
    img_aspect = img_size[0] / img_size[1]
    screen_aspect = screen_size[0] / screen_size[1]
    if screen_aspect > img_aspect:
        # Image will be shorter than the screen horizontally
        new_size = (screen_size[1]*img_aspect, screen_size[1])
    elif screen_aspect < img_aspect:
        # Image will be shorter than the screen vertically
        new_size = (screen_size[0], screen_size[0]/img_aspect)
    else:
        # Image will fill the screen
        new_size = screen_size
    # Scale the image to the new size
    img = pygame.transform.scale(img, new_size)
    return img


def main():
    pygame.init()
    display = pygame.display
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_size = screen.get_size()
    # Display the starting image
    photos = [pygame.image.load(photo).convert() for photo in PHOTOS]
    screen_size = screen.get_size()
    photos = [resize_image(photo, screen_size) for photo in photos]
    # Enter event loop waiting for the thing to exit
    t0 = time.time()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
        # Update the display with the image
        idx = int((time.time()-t0) / PHOTO_TICK) % len(photos)
        show_image(photos[idx], screen=screen, display=display)


if __name__ == "__main__":
    sys.exit(main())
