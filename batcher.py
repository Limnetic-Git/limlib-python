import numpy as np


MAX_SPRITES_IN_BATCH = 1_000_000

class SpriteBatcher:
    def __init__(self, max_sprites=MAX_SPRITES_IN_BATCH):
        self.data = np.zeros(max_sprites, dtype=[
            ('offset_x', 'f4'), ('offset_y', 'f4'),
            ('size_w', 'f4'), ('size_h', 'f4'),
            ('rotation', 'f4'),
            ('tint_r', 'f4'), ('tint_g', 'f4'), ('tint_b', 'f4'), ('tint_a', 'f4'),
        ])
        self.count = 0
        self.max_sprites = max_sprites

    def add(self, x, y, w, h, rot, r, g, b, a):
        if self.count >= self.max_sprites:
            return
        self.data[self.count] = (x, y, w, h, rot, r, g, b, a)
        self.count += 1

    def add_batch(self, sprites):
        n = len(sprites)
        if self.count + n > self.max_sprites:
            n = self.max_sprites - self.count
        temp = self.data.view(np.float32).reshape(self.max_sprites, 9)
        temp[self.count:self.count+n] = sprites
        self.count += n

    def clear(self):
        self.count = 0
