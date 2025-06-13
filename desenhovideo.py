from moviepy.editor import *
from PIL import Image, ImageDraw
import numpy as np

# Carrega o desenho
base_image = Image.open("desenho.png").convert("L")
video_size = base_image.size

# Gera frames da animação
frames = []
for i in range(30):
    frame = base_image.copy()
    draw = ImageDraw.Draw(frame)

    # "Zzz" saindo da cabeça
    if i % 10 == 0:
        draw.text((30, 30 - (i % 30)), "Z", fill=255)
    elif i % 10 == 5:
        draw.text((35, 15 - (i % 30)), "Z", fill=255)

    # Baba descendo
    baba_y = 160 + i // 3
    draw.line((80, 160, 80, baba_y), fill=255, width=1)

    # Bolinho movendo
    if i % 10 < 5:
        draw.ellipse((300, 140, 320, 160), fill=255)
    else:
        draw.ellipse((310, 160, 330, 180), fill=255)

    # Converter P&B para RGB
    rgb_frame = np.stack((np.array(frame),) * 3, axis=-1)
    frames.append(rgb_frame)

# Criar clipe de vídeo
clip = ImageSequenceClip(frames, fps=10)

# Adicionar som (senoide como simulação do arroto)
burp_audio = AudioClip(lambda t: 0.5 * np.sin(2 * np.pi * 220 * t) * (t > 2.5), duration=3)
clip = clip.set_audio(burp_audio)

# Exportar vídeo
clip.write_videofile("florzinha_final.mp4", codec="libx264", fps=10)