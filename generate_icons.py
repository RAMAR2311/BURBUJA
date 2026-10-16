import os
import math
from PIL import Image, ImageDraw, ImageFilter

def draw_3d_bubble(draw, cx, cy, radius, primary_color=(255, 23, 68), specular_color=(255, 255, 255)):
    """
    Dibuja una burbuja esférica 3D con relieve, degradado concéntrico y brillo especular.
    """
    r, g, b = primary_color
    # Base con sombra difusa perimetral
    steps = 14
    for i in range(steps):
        factor = i / steps
        cur_r = radius * (1.0 - factor * 0.45)
        # Tinte que oscurece hacia el borde y aclara hacia el centro superior
        cur_col = (
            min(255, int(r + (255 - r) * (1 - factor) * 0.45)),
            min(255, int(g + 60 * (1 - factor) * 0.45)),
            min(255, int(b + 60 * (1 - factor) * 0.45)),
            int(255 * (1.0 - factor * 0.15))
        )
        offset_x = (cx - radius * 0.18 * (1 - factor))
        offset_y = (cy - radius * 0.18 * (1 - factor))
        draw.ellipse(
            [offset_x - cur_r, offset_y - cur_r, offset_x + cur_r, offset_y + cur_r],
            fill=cur_col
        )
    
    # Brillo especular 3D de alta luminosidad (destello de luz de la burbuja)
    specular_cx = cx - radius * 0.35
    specular_cy = cy - radius * 0.35
    spec_rx = radius * 0.28
    spec_ry = radius * 0.18
    draw.ellipse(
        [specular_cx - spec_rx, specular_cy - spec_ry, specular_cx + spec_rx, specular_cy + spec_ry],
        fill=(255, 255, 255, 220)
    )
    # Segundo micro-brillo reflejo en el borde inferior
    ref_cx = cx + radius * 0.28
    ref_cy = cy + radius * 0.30
    draw.ellipse(
        [ref_cx - radius * 0.12, ref_cy - radius * 0.08, ref_cx + radius * 0.12, ref_cy + radius * 0.08],
        fill=(255, 255, 255, 120)
    )

def generate_burbuja_lili_master_icon():
    canvas_size = 1024
    img = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))
    cx, cy = canvas_size // 2, canvas_size // 2

    # 1. Resplandor difuso suave de fondo (Rojo Burbuja sutil sobre fondo blanco)
    glow_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_radius = 430
    glow_draw.ellipse(
        [cx - glow_radius, cy - glow_radius, cx + glow_radius, cy + glow_radius],
        fill=(255, 23, 68, 28)
    )
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=40))
    img.alpha_composite(glow_img)

    # Re-draw para las burbujas
    draw = ImageDraw.Draw(img)

    # 2. Anillo fino perimetral de contención estética
    ring_r = 440
    draw.ellipse(
        [cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r],
        outline=(253, 232, 232, 255),
        width=8
    )

    # 3. Flor de Burbujas en Relieve 3D (Rojo Burbuja #FF1744 con centro Blanco)
    # Generamos 6 pétalos de burbujas en círculo
    num_petals = 6
    petal_distance = 185
    petal_radius = 125

    # Dibujar pétalos de burbujas 3D
    for i in range(num_petals):
        angle = math.radians(i * (360 / num_petals) - 30)
        px = cx + math.cos(angle) * petal_distance
        py = cy + math.sin(angle) * petal_distance
        draw_3d_bubble(draw, px, py, petal_radius, primary_color=(255, 23, 68))

    # Burbujas satélite exteriores decorativas más pequeñas (efecto burbujeo dinámico)
    satellites = [
        (cx + 340, cy - 230, 48),
        (cx - 330, cy - 210, 42),
        (cx + 310, cy + 240, 36),
        (cx - 320, cy + 220, 46),
        (cx, cy - 365, 32),
        (cx, cy + 365, 32)
    ]
    for sx, sy, sr in satellites:
        draw_3d_bubble(draw, sx, sy, sr, primary_color=(255, 82, 82))

    # 4. Burbuja Central (Centro Blanco brillante con núcleo rojo translúcido y relieve 3D)
    center_radius = 135
    # Sombra interna / halo del centro
    draw.ellipse(
        [cx - center_radius - 8, cy - center_radius - 8, cx + center_radius + 8, cy + center_radius + 8],
        fill=(183, 28, 28, 90)
    )
    # Esfera blanca central perlada
    steps_c = 12
    for j in range(steps_c):
        factor_c = j / steps_c
        cur_cr = center_radius * (1.0 - factor_c * 0.4)
        c_val = int(245 + 10 * factor_c)
        draw.ellipse(
            [cx - cur_cr, cy - cur_cr, cx + cur_cr, cy + cur_cr],
            fill=(c_val, c_val, c_val, 255),
            outline=(255, 23, 68, 180) if j == 0 else None,
            width=6 if j == 0 else 0
        )
    # Destello especular central
    draw.ellipse(
        [cx - 45 - 28, cy - 45 - 18, cx - 45 + 28, cy - 45 + 18],
        fill=(255, 255, 255, 255)
    )
    # Detalle de smartphone estilizado o inicial "B" en el corazón blanco
    # Dibujamos un ícono sutil de teléfono celular en rojo burbuja dentro del centro blanco
    phone_w = 46
    phone_h = 76
    draw.rounded_rectangle(
        [cx - phone_w // 2, cy - phone_h // 2, cx + phone_w // 2, cy + phone_h // 2],
        radius=12,
        fill=(255, 255, 255, 255),
        outline=(255, 23, 68, 255),
        width=5
    )
    # Pantalla interna del teléfono
    draw.rounded_rectangle(
        [cx - phone_w // 2 + 5, cy - phone_h // 2 + 7, cx + phone_w // 2 - 5, cy + phone_h // 2 - 9],
        radius=6,
        fill=(255, 23, 68, 255)
    )
    # Notch/altavoz
    draw.line([cx - 8, cy - phone_h // 2 + 3, cx + 8, cy - phone_h // 2 + 3], fill=(255, 23, 68, 255), width=2)
    # Micro botón/corazón en la pantallita
    draw.ellipse([cx - 5, cy - 2, cx + 5, cy + 8], fill=(255, 255, 255, 255))

    # Convertir a RGB puro sobre fondo blanco
    final_rgb = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    final_rgb.paste(img, (0, 0), img)

    # Crear directorios
    os.makedirs("static/img/icons", exist_ok=True)

    # Guardar Master PNG files
    final_rgb.save("static/img/BurbujaLili.png", "PNG", quality=95)
    final_rgb.save("static/img/MyCase.png", "PNG", quality=95)
    final_rgb.save("static/img/MyCase_wide.png", "PNG", quality=95)

    # Guardar tamaños PWA y Favicon
    sizes = {
        "static/img/icons/icon-512x512.png": 512,
        "static/img/icons/icon-192x192.png": 192,
        "static/img/icons/apple-touch-icon.png": 180,
        "static/img/icons/favicon-48x48.png": 48,
        "static/img/icons/favicon-32x32.png": 32,
        "static/img/icons/favicon-16x16.png": 16,
    }

    for path, sz in sizes.items():
        resized = final_rgb.resize((sz, sz), Image.Resampling.LANCZOS)
        resized.save(path, "PNG", optimize=True)

    # Guardar .ico multi-resolución
    final_rgb.save("static/favicon.ico", format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("[SUCCESS] Isotipo PWA Flor de Burbujas 3D y Favicons de Burbuja Lili generados sobre fondo 100% blanco puro (#FFFFFF).")

if __name__ == "__main__":
    generate_burbuja_lili_master_icon()
