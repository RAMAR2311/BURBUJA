import os
import math
from PIL import Image, ImageDraw, ImageFilter

def create_heart_polygon(cx, cy, size):
    """Generates points for a smooth parametric heart."""
    points = []
    # Parametric equations for a heart:
    # x = 16 * sin(t)^3
    # y = -(13 * cos(t) - 5 * cos(2t) - 2 * cos(3t) - cos(4t))
    scale = size / 35.0
    for deg in range(0, 360, 2):
        t = math.radians(deg)
        x = 16 * (math.sin(t) ** 3)
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        px = cx + x * scale
        py = cy + y * scale
        points.append((px, py))
    return points

def generate_mycase_master_icon():
    # Render at high resolution (1024x1024) for supreme antialiased quality
    canvas_size = 1024
    img = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    cx, cy = canvas_size // 2, canvas_size // 2

    # 1. Subtle Neon Ambient Glow layer
    glow_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_radius = 420
    glow_draw.ellipse(
        [cx - glow_radius, cy - glow_radius, cx + glow_radius, cy + glow_radius],
        outline=(255, 20, 147, 80),
        width=40
    )
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=25))
    img.alpha_composite(glow_img)

    # Re-obtain draw after composite
    draw = ImageDraw.Draw(img)

    # 2. Outer Circular Neon Ring (#FF1493)
    ring_radius = 410
    draw.ellipse(
        [cx - ring_radius, cy - ring_radius, cx + ring_radius, cy + ring_radius],
        outline=(255, 20, 147, 255),
        width=24
    )

    # Accent thin inner ring for Metallic Glam vibe
    inner_ring_radius = ring_radius - 22
    draw.ellipse(
        [cx - inner_ring_radius, cy - inner_ring_radius, cx + inner_ring_radius, cy + inner_ring_radius],
        outline=(244, 114, 182, 140),
        width=6
    )

    # 3. Smartphone Silhouette in Center
    # Phone dimensions
    phone_w = 340
    phone_h = 560
    phone_x0 = cx - phone_w // 2
    phone_y0 = cy - phone_h // 2
    phone_x1 = cx + phone_w // 2
    phone_y1 = cy + phone_h // 2
    corner_radius = 52

    # Phone outer frame (White filled with Neon Pink border)
    draw.rounded_rectangle(
        [phone_x0, phone_y0, phone_x1, phone_y1],
        radius=corner_radius,
        fill=(255, 255, 255, 255),
        outline=(255, 20, 147, 255),
        width=18
    )

    # Phone Inner Screen
    screen_pad = 26
    screen_x0 = phone_x0 + screen_pad
    screen_y0 = phone_y0 + screen_pad + 20
    screen_x1 = phone_x1 - screen_pad
    screen_y1 = phone_y1 - screen_pad - 20
    draw.rounded_rectangle(
        [screen_x0, screen_y0, screen_x1, screen_y1],
        radius=30,
        fill=(255, 245, 250, 255), # Ultra-subtle glam blush tint
        outline=(244, 114, 182, 180),
        width=6
    )

    # Top Speaker Pill / Dynamic Island
    speaker_w = 70
    speaker_h = 10
    draw.rounded_rectangle(
        [cx - speaker_w // 2, phone_y0 + 20, cx + speaker_w // 2, phone_y0 + 20 + speaker_h],
        radius=5,
        fill=(255, 20, 147, 220)
    )

    # Bottom Home Indicator Bar
    bar_w = 90
    bar_h = 6
    draw.rounded_rectangle(
        [cx - bar_w // 2, phone_y1 - 22, cx + bar_w // 2, phone_y1 - 22 + bar_h],
        radius=3,
        fill=(244, 114, 182, 200)
    )

    # 4. Heart in Center of Screen (#FF1493 Neon Heart)
    heart_points = create_heart_polygon(cx, cy - 8, size=150)
    draw.polygon(heart_points, fill=(255, 20, 147, 255))

    # Glam specular highlight on upper left of heart
    hl_points = create_heart_polygon(cx - 10, cy - 20, size=75)
    # Draw small accent dot/glow
    draw.ellipse([cx - 40, cy - 40, cx - 18, cy - 18], fill=(255, 255, 255, 200))

    # Tiny decorative stars / sparkles around the phone
    def draw_star(sx, sy, r, color):
        points = [
            (sx, sy - r), (sx + r * 0.3, sy - r * 0.3),
            (sx + r, sy), (sx + r * 0.3, sy + r * 0.3),
            (sx, sy + r), (sx - r * 0.3, sy + r * 0.3),
            (sx - r, sy), (sx - r * 0.3, sy - r * 0.3)
        ]
        draw.polygon(points, fill=color)

    draw_star(cx + 240, cy - 220, 26, (255, 20, 147, 255))
    draw_star(cx - 240, cy + 200, 22, (244, 114, 182, 255))
    draw_star(cx + 220, cy + 240, 16, (255, 102, 178, 220))
    draw_star(cx - 220, cy - 240, 18, (255, 20, 147, 220))

    # Convert to pure RGB on white background
    final_rgb = Image.new("RGB", (canvas_size, canvas_size), (255, 255, 255))
    final_rgb.paste(img, (0, 0), img)

    # Create target directories
    os.makedirs("static/img/icons", exist_ok=True)

    # Save Master PNG files
    final_rgb.save("static/img/MyCase.png", "PNG", quality=95)
    final_rgb.save("static/img/Maripocell.png", "PNG", quality=95)
    final_rgb.save("static/img/Maripocell_wide.png", "PNG", quality=95)
    final_rgb.save("static/img/MyCase_wide.png", "PNG", quality=95)

    # Save PWA and Favicon sizes
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

    # Save .ico with multi-resolution
    final_rgb.save("static/favicon.ico", format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("[SUCCESS] Todos los iconos PWA, Isotipo y Favicons de My Case generados sobre fondo 100% blanco puro (#FFFFFF).")

if __name__ == "__main__":
    generate_mycase_master_icon()
