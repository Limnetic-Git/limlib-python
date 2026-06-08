from limlib import *
import numpy as np

InitWindow(800, 600)
tex = LoadTexture('limlib.png')

while not WindowShouldClose():
    StartDrawing()
    FillWindow(Color('#1a1a2e'))

    for i in range(10_000):
        DrawSprite(tex,
                   np.random.uniform(-1, 1),
                   np.random.uniform(-1, 1),
                   0.05, 0.05)

    EndDrawing()

CloseWindow()
