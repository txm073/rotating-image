import os, sys
import subprocess
import random

try:
    import pygame
    import numpy as np
except ImportError:
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'pygame', 'numpy'])
    import pygame
    import numpy as np

os.chdir(os.path.dirname(__file__))

"""
arr = cv2.imread("smaller.jpg")
arr = cv2.resize(arr, (300, 300))
arr = cv2.hconcat([arr, arr, arr])
np.savez_compressed("image.npz", array=arr)
"""

class Window:

    def __init__(self):
        os.chdir(os.path.dirname(sys.argv[0]) if os.path.dirname(sys.argv[0]) else ".")
        self.win = pygame.display.set_mode((900, 750))
        self.array = np.load("image.npz")["array"]
        image = pygame.transform.rotate(pygame.surfarray.make_surface(self.array), 270)
        self.top_array = self.bottom_array = pygame.surfarray.array3d(image)
        self.fps = 60
        self.game_clock = pygame.time.Clock()
        self.velocity = 3
        self.angle_gen = self.get_angle()
        self.images = []
        self.sprites = pygame.sprite.Group()

    def move_bg_image(self, arr, direction):
        axis = 0 if direction in ["right", "left"] else 1
        vel = -self.velocity if direction in ["up", "left"] else self.velocity
        return np.roll(arr, shift=vel, axis=axis)      

    def background(self):
        self.top_array = self.move_bg_image(self.top_array, "left")
        self.win.blit(self.resize(pygame.surfarray.make_surface(self.top_array), (900, 200)), (0, 0))
        self.bottom_array = self.move_bg_image(self.bottom_array, "right")
        self.win.blit(self.resize(pygame.surfarray.make_surface(self.bottom_array), (900, 200)), (0, 550))

    def get_angle(self):
        while True:
            for i in range(1, 360, self.velocity):
                yield i

    def blit_center(self, surface, pos):
        x = pos[0] // 2 - surface.get_width() // 2
        y = pos[1] // 2 - surface.get_height() // 2
        cover_surface = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        cover_surface.blit(surface, (0, 0))
        self.win.blit(cover_surface, (x, y))

    def center(self, surface, pos):
        self.blit_center(pygame.transform.rotate(surface, next(self.angle_gen)), pos)

    def resize(self, img, size):
        return pygame.transform.scale(img, size)

    def create_new_image(self):
        surface = self.resize(pygame.transform.rotate(self.center_surface, random.randint(-360, 360)), (random.randint(100, 550), random.randint(100, 550)))
        pos = (random.randint(0, 750), random.randint(0, 600))
        return surface, pos

    def keypress(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if len(self.images) > 3:
                ...#del self.images[0]
            self.images.append(self.create_new_image())
            pygame.time.delay(50)
        elif keys[pygame.K_ESCAPE]:
            self.images = []

    def run(self):
        self.center_surface = pygame.surfarray.make_surface(self.array[:, :300, :]).convert_alpha()
        middle = pygame.Surface((900, 350))
        middle.blit(self.resize(self.center_surface, (350, 350)), (0, 0))
        middle.blit(self.resize(self.center_surface, (350, 350)), (300, 0))
        middle.blit(self.resize(self.center_surface, (350, 350)), (600, 0))
        while True:
            self.win.blit(middle, (0, 200))
            self.game_clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            self.keypress()
            self.background()
            self.center(self.center_surface, (900, 750))
            for image, pos in self.images:
                self.win.blit(image, pos)
            pygame.display.update()
            

if __name__ == "__main__":
    win = Window()
    win.run()

