import time
import math
import random
import win32api
import win32gui
import win32con
import keyboard

# Fetch full virtual screen bounds (supports multi-monitor setups)
WIDTH = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
HEIGHT = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
LEFT = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
TOP = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# --- BASE GDI EFFECTS (1 - 8) ---

def effect_color_invert():
    """1: Flips screen colors to opposite (Invert)."""
    hdc = win32gui.GetDC(0)
    win32gui.PatBlt(hdc, LEFT, TOP, WIDTH, HEIGHT, win32con.DSTINVERT)
    win32gui.ReleaseDC(0, hdc)


def effect_screen_melt(iterations=15):
    """2: Grabs random vertical strips and shifts them down (Melt)."""
    hdc = win32gui.GetDC(0)
    for _ in range(iterations):
        x = random.randint(LEFT, WIDTH - 100)
        y_offset = random.randint(10, 40)
        strip_w = random.randint(50, 150)
        strip_h = HEIGHT - y_offset
        win32gui.BitBlt(hdc, x, y_offset, strip_w, strip_h, hdc, x, 0, win32con.SRCCOPY)
    win32gui.ReleaseDC(0, hdc)


def effect_tunnel_zoom(iterations=12):
    """3: Shrinks and centers the display repeatedly (Tunnel Zoom)."""
    hdc = win32gui.GetDC(0)
    for _ in range(iterations):
        margin_x = 30
        margin_y = 20
        win32gui.StretchBlt(
            hdc, margin_x, margin_y, WIDTH - (margin_x * 2), HEIGHT - (margin_y * 2),
            hdc, 0, 0, WIDTH, HEIGHT, win32con.SRCCOPY
        )
        time.sleep(0.02)
    win32gui.ReleaseDC(0, hdc)


def effect_glitch_shake(iterations=20):
    """4: Rapidly shakes the screen randomly across X/Y axes."""
    hdc = win32gui.GetDC(0)
    for _ in range(iterations):
        dx = random.randint(-25, 25)
        dy = random.randint(-25, 25)
        win32gui.BitBlt(hdc, dx, dy, WIDTH, HEIGHT, hdc, 0, 0, win32con.SRCCOPY)
        time.sleep(0.01)
    win32gui.ReleaseDC(0, hdc)


def effect_sine_wave():
    """5: Slices the screen horizontally and applies a sine wave displacement."""
    hdc = win32gui.GetDC(0)
    slice_height = 8
    frequency = 0.05
    amplitude = 25
    for y in range(0, HEIGHT, slice_height):
        offset_x = int(math.sin(y * frequency) * amplitude)
        win32gui.BitBlt(
            hdc, LEFT + offset_x, TOP + y, WIDTH, slice_height,
            hdc, LEFT, TOP + y, win32con.SRCCOPY
        )
    win32gui.ReleaseDC(0, hdc)


def effect_xor_color_blast(iterations=10):
    """6: Uses PATINVERT with brush patterns to create glitchy XOR color trails."""
    hdc = win32gui.GetDC(0)
    for _ in range(iterations):
        color = win32api.RGB(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        brush = win32gui.CreateSolidBrush(color)
        old_brush = win32gui.SelectObject(hdc, brush)
        
        rx = random.randint(0, WIDTH - 200)
        ry = random.randint(0, HEIGHT - 200)
        rw = random.randint(100, 500)
        rh = random.randint(100, 500)
        
        win32gui.PatBlt(hdc, rx, ry, rw, rh, win32con.PATINVERT)
        win32gui.SelectObject(hdc, old_brush)
        win32gui.DeleteObject(brush)
        time.sleep(0.02)
    win32gui.ReleaseDC(0, hdc)


def effect_pixel_scatter(count=60):
    """7: Grabs small screen blocks and swaps/scatters them across the desktop."""
    hdc = win32gui.GetDC(0)
    block_size = 60
    for _ in range(count):
        x1 = random.randint(0, WIDTH - block_size)
        y1 = random.randint(0, HEIGHT - block_size)
        x2 = random.randint(0, WIDTH - block_size)
        y2 = random.randint(0, HEIGHT - block_size)
        win32gui.BitBlt(hdc, x2, y2, block_size, block_size, hdc, x1, y1, win32con.SRCCOPY)
    win32gui.ReleaseDC(0, hdc)


def effect_pixelate():
    """8: Downscales the screen into low-resolution blocks then stretches it back."""
    hdc = win32gui.GetDC(0)
    scale = 16
    win32gui.StretchBlt(
        hdc, 0, 0, WIDTH // scale, HEIGHT // scale,
        hdc, 0, 0, WIDTH, HEIGHT, win32con.SRCCOPY
    )
    win32gui.StretchBlt(
        hdc, 0, 0, WIDTH, HEIGHT,
        hdc, 0, 0, WIDTH // scale, HEIGHT // scale, win32con.SRCCOPY
    )
    win32gui.ReleaseDC(0, hdc)


# --- BRAND NEW GDI EFFECTS (9 - 12) ---

def effect_spiral_vortex(iterations=15):
    """9: Shrinks and rotates desktop slices in an offset spiral sequence."""
    hdc = win32gui.GetDC(0)
    for i in range(iterations):
        offset = (i + 1) * 12
        win32gui.StretchBlt(
            hdc, offset, offset, WIDTH - (offset * 2), HEIGHT - (offset * 2),
            hdc, 0, 0, WIDTH, HEIGHT, win32con.SRCINVERT
        )
        time.sleep(0.02)
    win32gui.ReleaseDC(0, hdc)


def effect_curtain_split():
    """10: Splits the left and right halves of the screen outward."""
    hdc = win32gui.GetDC(0)
    half_width = WIDTH // 2
    shift = 40
    
    # Left half shifted left
    win32gui.BitBlt(hdc, LEFT - shift, TOP, half_width, HEIGHT, hdc, LEFT, TOP, win32con.SRCCOPY)
    # Right half shifted right
    win32gui.BitBlt(hdc, LEFT + half_width + shift, TOP, half_width, HEIGHT, hdc, LEFT + half_width, TOP, win32con.SRCCOPY)
    
    win32gui.ReleaseDC(0, hdc)


def effect_glitch_lines(count=40):
    """11: Generates colorful single-pixel high scanlines across the display."""
    hdc = win32gui.GetDC(0)
    for _ in range(count):
        y = random.randint(0, HEIGHT - 1)
        h = random.randint(1, 5)
        offset_x = random.randint(-80, 80)
        
        # Shift line horizontally
        win32gui.BitBlt(hdc, offset_x, y, WIDTH, h, hdc, 0, y, win32con.SRCPAINT)
    win32gui.ReleaseDC(0, hdc)


def effect_swirl_shake(iterations=12):
    """12: Alternates between StretchBlt expanding and shrinking to create an elastic pulsation."""
    hdc = win32gui.GetDC(0)
    for i in range(iterations):
        delta = 25 if i % 2 == 0 else -25
        win32gui.StretchBlt(
            hdc, -delta, -delta, WIDTH + (delta * 2), HEIGHT + (delta * 2),
            hdc, 0, 0, WIDTH, HEIGHT, win32con.SRCCOPY
        )
        time.sleep(0.02)
    win32gui.ReleaseDC(0, hdc)


def redraw_screen():
    """Redraws the desktop"""
    win32gui.RedrawWindow(
        0, None, None,
        win32con.RDW_INVALIDATE | win32con.RDW_ERASE | win32con.RDW_ALLCHILDREN
    )


# --- MAIN CONTROL LOOP ---

def main():
    print("=========================================")
    print("      ULTIMATE GDI CONTROLLER           ")
    print("=========================================")
    print(" [1] Color Invert     [7] Block Scatter")
    print(" [2] Screen Melt      [8] Retro Pixelate")
    print(" [3] Tunnel Zoom      [9] Spiral Vortex")
    print(" [4] Glitch Shake     [0] Curtain Split")
    print(" [5] Sine Wave        [-] Glitch Lines")
    print(" [6] XOR Color Blast  [=] Swirl Pulse")
    print("-----------------------------------------")
    print(" Press 'r'   -> Clean Screen / Clear Artifacts")
    print(" Press 'esc' -> Exit Script")
    print("=========================================")

    # Hotkey Mappings
    keyboard.add_hotkey('1', effect_color_invert)
    keyboard.add_hotkey('2', effect_screen_melt)
    keyboard.add_hotkey('3', effect_tunnel_zoom)
    keyboard.add_hotkey('4', effect_glitch_shake)
    keyboard.add_hotkey('5', effect_sine_wave)
    keyboard.add_hotkey('6', effect_xor_color_blast)
    keyboard.add_hotkey('7', effect_pixel_scatter)
    keyboard.add_hotkey('8', effect_pixelate)
    keyboard.add_hotkey('9', effect_spiral_vortex)
    keyboard.add_hotkey('0', effect_curtain_split)
    keyboard.add_hotkey('-', effect_glitch_lines)
    keyboard.add_hotkey('=', effect_swirl_shake)
    keyboard.add_hotkey('r', redraw_screen)

    keyboard.wait('esc')
    redraw_screen()
    print("Exited cleanly.")


if __name__ == "__main__":
    main()