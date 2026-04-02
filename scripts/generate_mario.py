import requests
from PIL import Image, ImageDraw
import os

USERNAME = "miguelcastell"

# cria pasta de saída
os.makedirs("output", exist_ok=True)

# API
url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"
data = requests.get(url).json()

weeks = data.get("contributions", [])

# 🔥 LIMITES PRA NÃO EXPLODIR MEMÓRIA
MAX_FRAMES = 30
STEP = 2  # pula semanas

weeks = weeks[:MAX_FRAMES]

# 🔧 CONFIG VISUAL (reduzido)
CELL = 12
PADDING = 20

width = len(weeks) * CELL + PADDING * 2
height = 7 * CELL + PADDING * 2

# cores estilo GitHub
def get_color(count):
    if count == 0:
        return (235, 237, 240)
    elif count < 3:
        return (155, 233, 168)
    elif count < 6:
        return (64, 196, 99)
    elif count < 10:
        return (48, 161, 78)
    else:
        return (33, 110, 57)

# Mario pixel art
MARIO = [
    "  RRR  ",
    " RRRRR ",
    " RRBBR ",
    " BBBBB ",
    "RBBBBBR",
    "  BB   "
]

def draw_mario(draw, x, y):
    pixel = 2  # menor ainda
    for i, row in enumerate(MARIO):
        for j, col in enumerate(row):
            if col == "R":
                color = (220, 20, 60)
            elif col == "B":
                color = (30, 144, 255)
            else:
                continue

            draw.rectangle([
                x + j * pixel,
                y + i * pixel,
                x + (j+1) * pixel,
                y + (i+1) * pixel
            ], fill=color)

frames = []

# 🔥 LOOP OTIMIZADO
for frame_idx in range(0, len(weeks), STEP):

    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # desenhar grid
    for x, week in enumerate(weeks):
        days = week.get("contributionDays", [])

        for y, day in enumerate(days):
            count = day.get("contributionCount", 0)
            color = get_color(count)

            draw.rectangle([
                PADDING + x * CELL,
                PADDING + y * CELL,
                PADDING + (x+1) * CELL - 2,
                PADDING + (y+1) * CELL - 2
            ], fill=color)

    # mario andando
    mario_x = PADDING + frame_idx * CELL
    mario_y = PADDING + 2 * CELL

    draw_mario(draw, mario_x, mario_y)

    frames.append(img)

# 🧠 fallback (evita erro se lista vazia)
if not frames:
    raise Exception("Nenhum frame foi gerado.")

# salvar gif otimizado
frames[0].save(
    "output/mario.gif",
    save_all=True,
    append_images=frames[1:],
    duration=120,
    loop=0,
    optimize=True
)

print("✅ GIF gerado com sucesso em output/mario.gif")