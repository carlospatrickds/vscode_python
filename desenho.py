from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Carrega o desenho base em tons de cinza
base_image = Image.open("desenho.png").convert("L")
video_size = base_image.size

# (Opcional) Fonte customizada para o "Zzz"
try:
    font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = None  # Usa fonte padrão se a customizada não estiver disponível

# Gera os frames da animação
frames = []
for i in range(30):
    frame = base_image.copy()
    draw = ImageDraw.Draw(frame)

    # "Zzz" saindo da cabeça
    if i % 10 == 0:
        y_z = max(10, 30 - (i % 30))
        draw.text((30, y_z), "Z", fill=255, font=font)
    elif i % 10 == 5:
        y_z = max(10, 15 - (i % 30))
        draw.text((35, y_z), "Z", fill=255, font=font)

    # Baba descendo (sem ultrapassar os limites)
    baba_y = min(base_image.size[1] - 1, 160 + i // 3)
    draw.line((80, 160, 80, baba_y), fill=255, width=1)

    # Bolinho se movendo ou sendo comido
    if i < 25:
        if i % 10 < 5:
            draw.ellipse((300, 140, 320, 160), fill=255)
        else:
            draw.ellipse((310, 160, 330, 180), fill=255)
    else:
        # Bolo "comido" — só contorno
        draw.ellipse((310, 160, 330, 180), outline=255)

    # Converter P&B para RGB
    rgb_frame = np.stack((np.array(frame),) * 3, axis=-1)
    frames.append(rgb_frame)

# Criar clipe de vídeo a partir dos frames
clip = ImageSequenceClip(frames, fps=10)

# Simulação de som de arroto com senoide (opcional: substituir por arquivo real)
burp_audio = AudioClip(lambda t: 0.5 * np.sin(2 * np.pi * 220 * t) * (t > 2.5), duration=3)

# Se quiser usar um arquivo real de som de arroto, descomente abaixo:
# burp_audio = AudioFileClip("arroto_real.wav").subclip(0, 1)

clip = clip.set_audio(burp_audio)

# Exportar vídeo final
clip.write_videofile("florzinha_final.mp4", codec="libx264", fps=10)
