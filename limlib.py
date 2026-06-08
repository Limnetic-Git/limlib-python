import moderngl
import glfw
import os
import time
import numpy as np
from color import *
from batcher import SpriteBatcher
from PIL import Image

WINDOW = None
CTX = None
QUAD_VBO = None
SHADERS = {}
BATCHERS = {}

BATCH_ARRAYS = {}
BATCH_COUNTS = {}

SPRITE_VBO = None
SPRITE_VAO = None
MAX_SPRITES = 1_000_000

FPS = 0
FPS_COUNTER = 0
FPS_COUNTER_START_TIME = time.time()

def InitWindow(width: int, height: int, title: str = "Limlib window") -> None:
    global WINDOW, CTX, QUAD_VBO, SPRITE_VBO, SPRITE_VAO
    if not glfw.init():
        raise RuntimeError("GLFW is not running")
    WINDOW = glfw.create_window(width, height, title, None, None)
    glfw.make_context_current(WINDOW)
    glfw.swap_interval(0)
    CTX = moderngl.create_context()
    CTX.enable(moderngl.BLEND)
    CTX.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)
    LoadShaders()

    quad = np.array([
        0,0, 0,1,  1,0, 1,1,  1,1, 1,0,
        0,0, 0,1,  1,1, 1,0,  0,1, 0,0,
    ], dtype='f4')
    QUAD_VBO = CTX.buffer(quad.tobytes())

    proj = np.eye(4, dtype='f4')
    SHADERS['sprite']['u_projection'].write(proj.tobytes())

    SPRITE_VBO = CTX.buffer(reserve=MAX_SPRITES * 9 * 4)
    SPRITE_VAO = CTX.vertex_array(
        SHADERS['sprite'],
        [
            (QUAD_VBO, '2f 2f', 'in_vert', 'in_tex'),
            (SPRITE_VBO, '2f 2f 1f 4f/i', 'in_offset', 'in_size', 'in_rotation', 'in_tint'),
        ],
    )

def WindowShouldClose() -> bool:
    return glfw.window_should_close(WINDOW)

def FillWindow(color: Color) -> None:
    CTX.clear(*color())

def StartDrawing() -> None:
    global FPS, FPS_COUNTER, FPS_COUNTER_START_TIME
    global BATCH_COUNTS

    glfw.poll_events()
    FPS_COUNTER += 1

    elapsed = time.time() - FPS_COUNTER_START_TIME
    if elapsed >= 1.0:
        FPS = int(FPS_COUNTER / elapsed)
        FPS_COUNTER = 0
        FPS_COUNTER_START_TIME = time.time()
        glfw.set_window_title(WINDOW, f"Limlib - {FPS} FPS")

    for tex in BATCH_COUNTS:
        BATCH_COUNTS[tex] = 0

def EndDrawing() -> None:
    global BATCH_COUNTS, SPRITE_VBO, SPRITE_VAO
    for tex in BATCH_ARRAYS:
        count = BATCH_COUNTS.get(tex, 0)
        if count == 0:
            continue
        if tex not in BATCHERS:
            BATCHERS[tex] = SpriteBatcher()
        BATCHERS[tex].add_batch(BATCH_ARRAYS[tex][:count])

    program = SHADERS['sprite']

    for tex, batcher in BATCHERS.items():
        if batcher.count == 0:
            continue
        tex.use()
        data = batcher.data[:batcher.count].tobytes()
        SPRITE_VBO.write(data)
        SPRITE_VAO.render(moderngl.TRIANGLES, instances=batcher.count)

        batcher.clear()

    glfw.swap_buffers(WINDOW)

def CloseWindow() -> None:
    glfw.terminate()

def LoadShaders(path: str = 'shaders') -> None:
    global SHADERS
    for filename in os.listdir(f'{path}/vertex'):
        if not filename.endswith('.vert'):
            continue
        shader_name = filename.split('.')[0]

        with open(f'{path}/vertex/{filename}') as f:
            vertex_src = f.read()
        with open(f'{path}/fragment/{shader_name}.frag') as f:
            fragment_src = f.read()

        SHADERS[shader_name] = CTX.program(
            vertex_shader=vertex_src,
            fragment_shader=fragment_src,
        )

def LoadTexture(path: str, filter_mode: str = 'NEAREST') -> moderngl.Texture:
    img = Image.open(path).convert('RGBA')
    texture = CTX.texture(img.size, 4, img.tobytes())

    if filter_mode == 'NEAREST':
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
    else:
        texture.filter = (moderngl.LINEAR, moderngl.LINEAR)

    return texture

def DrawSprite(
    texture: moderngl.Texture,
    x: float, y: float,
    width: float = 0.3, height: float = 0.3,
    rotation: float = 0.0,
    tint: Color = WHITE) -> None:

    if texture not in BATCH_ARRAYS:
        BATCH_ARRAYS[texture] = np.zeros((MAX_SPRITES, 9), dtype=np.float32)
        BATCH_COUNTS[texture] = 0

    idx = BATCH_COUNTS[texture]
    t = tint()
    BATCH_ARRAYS[texture][idx] = (x, y, width, height, rotation, t[0], t[1], t[2], t[3])
    BATCH_COUNTS[texture] = idx + 1

def DrawSprites(texture: moderngl.Texture, sprites: np.ndarray) -> None:
    if texture not in BATCHERS:
        BATCHERS[texture] = SpriteBatcher()
    BATCHERS[texture].add_batch(sprites)
