import requests
from datetime import datetime, timedelta
from PIL import Image, ImageDraw

USERNAME = "miguelcastell"

# ---- pegar contribuições (simples via github chart) ----
url = f"https://github-contributions-api.jogruber.de/v4/{USERNAME}"
data = requests.get(url).json()

weeks = data["contributions"]

# ---- config visual ----
CELL = 20
PADDING = 20

width = len(weeks) * CELL + PADDING * 2
height = 7 * CELL + PADDING * 2

# cores estilo github
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

# ---- mario pixel art (simplificado) ----
MARIO = [
    "  RR  ",
    " RRRR ",
    " RRBB ",
    " BBBB ",
    "RBBBBR",
    "  BB  "
]

def draw_mario(draw, x, y):
    pixel = 4
    for i, row in enumerate(MARIO):
        for j, col in enumerate(row):
            if col == "R":
                color = (255, 0, 0)
            elif col == "B":
                color = (0, 0, 255)
            else:
                continue

            draw.rectangle([
                x + j * pixel,
                y + i * pixel,
                x + (j+1) * pixel,
                y + (i+1) * pixel
            ], fill=color)

# ---- gerar frames ----
frames = []

for frame_idx in range(len(weeks)):
    img = Image.new("RGB", (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    # desenhar grid
    for x, week in enumerate(weeks):
        for y, day in enumerate(week["contributionDays"]):
            color = get_color(day["contributionCount"])
            draw.rectangle([
                PADDING + x * CELL,
                PADDING + y * CELL,
                PADDING + (x+1) * CELL - 2,
                PADDING + (y+1) * CELL - 2
            ], fill=color)

    # desenhar mario andando
    mario_x = PADDING + frame_idx * CELL
    mario_y = PADDING + 2 * CELL

    draw_mario(draw, mario_x, mario_y)

    frames.append(img)

# ---- salvar gif ----
frames[0].save(
    "output/mario.gif",
    save_all=True,
    append_images=frames[1:],
    duration=80,
    loop=0
)