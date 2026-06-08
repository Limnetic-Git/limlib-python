from limlib import *
import numpy as np

InitWindow(800, 600)
tex = LoadTexture('limlib.png')
tex2 = LoadTexture('texture2.png')

N = 100_000
sprites = np.zeros((N, 9), dtype=np.float32)
sprites[:, 0] = np.random.uniform(-1, 1, N)
sprites[:, 1] = np.random.uniform(-1, 1, N)
sprites[:, 2] = 0.02
sprites[:, 3] = 0.02

sprites[:, 5] = 1
sprites[:, 6] = 1
sprites[:, 7] = 1
sprites[:, 8] = 1.0

while not WindowShouldClose():
    StartDrawing()
    FillWindow(Color('#191919'))

    DrawSprites(tex, sprites)

    EndDrawing()

CloseWindow()
