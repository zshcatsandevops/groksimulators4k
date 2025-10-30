#!/usr/bin/env python3
"""
switch_one_full_pygame.py
Complete Nintendo Switch One GUI simulation with all major features.
- Clickable home menu with 12 icons leading to dedicated screens
- Settings: Brightness, volume, Bluetooth, calibration, etc.
- eShop: Fake store with purchasable games
- Album: Screenshot gallery (fake images)
- News: Fake news feed
- Profile: User info and Mii placeholder
- Controllers: Pairing simulation
- System: Version info, updates
- Data Management: Fake storage stats
- Help: FAQ list
- Online features: Fake friends list, Nintendo Switch Online
- Sleep mode, lock screen
- Video capture simulation (press 'C' key)
- Mario Kart demo in Games
- GameShare and Virtual Game Cards placeholders
"""

import pygame
import pygame.freetype
from pygame import Rect
import datetime
import math
import random

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------
WIN_W, WIN_H = 600, 400
SCREEN_W, SCREEN_H = 460, 260
SCREEN_X = (WIN_W - SCREEN_W) // 2
SCREEN_Y = 70
BEZEL_RADIUS = 20
BG_COLOR = (20, 20, 25)
HUD_COLOR = (10, 10, 10)
TEXT_COLOR = (255, 255, 255)
ACCENT_COLOR = (0, 200, 255)
JOYCON_L = (0, 120, 200)
JOYCON_R = (255, 59, 48)
POWER_ON = (0, 220, 100)
POWER_OFF = (100, 100, 100)
HIGHLIGHT = (255, 255, 255, 80)
DIM_ALPHA = 128  # For brightness simulation

# ------------------------------------------------------------
# Pygame Init
# ------------------------------------------------------------
pygame.init()
pygame.freetype.init()
screen = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Switch One – Complete GUI Simulation")
clock = pygame.time.Clock()

# Fonts
FONT_SMALL = pygame.freetype.SysFont("segoeui", 16)
FONT_BIG = pygame.freetype.SysFont("segoeui", 22, bold=True)
FONT_ICON = pygame.freetype.SysFont("segoeui", 48, bold=True)
FONT_LABEL = pygame.freetype.SysFont("segoeui", 14)

# State
simulation_on = True
selected_icon = None
hovered_icon = None
power_pressed = False
current_screen = "home"  # home, lock, games, eshop, album, settings, news, profile, themes, stats, controllers, system, data, help, gamechat
brightness = 1.0  # 0.0 to 1.0
volume_level = 0.7  # 0.0 to 1.0
album_images = []  # List of fake screenshot rects
friends = ["Friend1", "Friend2", "Friend3"]  # Fake friends list
virtual_games = ["Mario Kart 8", "Zelda BOTW"]  # Fake virtual game cards
detached_joycons = True  # Toggle for attached/detached

# Lock screen state
locked = False
lock_time = 0  # Initialize to 0

# ------------------------------------------------------------
# Icon Definitions for Home and Submenus
# ------------------------------------------------------------
ICONS = [
    {"emoji": "🎮", "label": "Games", "id": "games"},
    {"emoji": "🛍️", "label": "eShop", "id": "eshop"},
    {"emoji": "📸", "label": "Album", "id": "album"},
    {"emoji": "⚙️", "label": "Settings", "id": "settings"},
    {"emoji": "🌐", "label": "News", "id": "news"},
    {"emoji": "👤", "label": "Profile", "id": "profile"},
    {"emoji": "🎨", "label": "Themes", "id": "themes"},
    {"emoji": "📊", "label": "Stats", "id": "stats"},
    {"emoji": "📱", "label": "Controllers", "id": "controllers"},
    {"emoji": "🔧", "label": "System", "id": "system"},
    {"emoji": "💾", "label": "Data", "id": "data"},
    {"emoji": "❓", "label": "Help", "id": "help"},
]

SETTINGS_ICONS = [
    {"emoji": "☀️", "label": "Brightness", "id": "brightness"},
    {"emoji": "🔊", "label": "Volume", "id": "volume"},
    {"emoji": "🎧", "label": "Bluetooth", "id": "bluetooth"},
    {"emoji": "🕹️", "label": "Calibration", "id": "calibration"},
    {"emoji": "🌐", "label": "Internet", "id": "internet"},
]

ICON_SIZE = 70
ICON_SPACING = 85
ICON_START_X = SCREEN_X + 30
ICON_START_Y = SCREEN_Y + 50

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------
def clamp_color(val):
    return max(0, min(255, int(val)))

def draw_rounded_rect(surf, rect, color, radius=20):
    pygame.draw.rect(surf, color, rect, border_radius=radius)

def get_icon_rect(index, start_x=ICON_START_X, start_y=ICON_START_Y, spacing=ICON_SPACING, cols=6):
    row = index // cols
    col = index % cols
    x = start_x + col * spacing
    y = start_y + row * spacing
    return pygame.Rect(x, y, ICON_SIZE, ICON_SIZE)

def apply_brightness(surf):
    dim_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
    dim_surf.fill((0, 0, 0, int(255 * (1 - brightness))))
    surf.blit(dim_surf, (0, 0))

# ------------------------------------------------------------
# Draw Joy-Cons (with detachment simulation)
# ------------------------------------------------------------
def draw_joycons(surface):
    if detached_joycons:
        l_rect = Rect(20, 100, 80, 200)
        draw_rounded_rect(surface, l_rect, JOYCON_L, 30)
        pygame.draw.circle(surface, (30, 30, 30), (60, 180), 25)
        for dx, dy in [(35,140), (55,160), (75,140), (55,120)]:
            pygame.draw.circle(surface, (50,50,50), (dx, dy), 10)

        r_rect = Rect(WIN_W - 100, 100, 80, 200)
        draw_rounded_rect(surface, r_rect, JOYCON_R, 30)
        pygame.draw.circle(surface, (30, 30, 30), (WIN_W - 60, 180), 25)
        for dx, dy in [(WIN_W-75,140), (WIN_W-55,160), (WIN_W-35,140), (WIN_W-55,120)]:
            pygame.draw.circle(surface, (50,50,50), (dx, dy), 10)
    else:
        # Attached simulation (simplified)
        pygame.draw.rect(surface, JOYCON_L, (SCREEN_X - 40, SCREEN_Y, 40, SCREEN_H))
        pygame.draw.rect(surface, JOYCON_R, (SCREEN_X + SCREEN_W, SCREEN_Y, 40, SCREEN_H))

# ------------------------------------------------------------
# Draw Screen Content
# ------------------------------------------------------------
def draw_screen(surface):
    bezel_rect = Rect(SCREEN_X - 10, SCREEN_Y - 10, SCREEN_W + 20, SCREEN_H + 20)
    draw_rounded_rect(surface, bezel_rect, (15, 15, 15), BEZEL_RADIUS + 10)
    draw_rounded_rect(surface, Rect(SCREEN_X, SCREEN_Y, SCREEN_W, SCREEN_H), (5, 5, 5), BEZEL_RADIUS)

    game_surf = pygame.Surface((SCREEN_W, SCREEN_H))
    game_surf.fill((10, 20, 30) if simulation_on else (5, 5, 5))

    if not simulation_on:
        FONT_BIG.render_to(game_surf, (SCREEN_W//2 - 90, SCREEN_H//2 - 30), "OFF", (60, 60, 60))
    elif locked:
        FONT_BIG.render_to(game_surf, (SCREEN_W//2 - 100, SCREEN_H//2 - 30), "Locked - Click to Unlock", (200, 200, 200))
    elif current_screen == "game":
        draw_game_demo(game_surf)
    elif current_screen == "home":
        draw_home_menu(game_surf)
    elif current_screen == "eshop":
        draw_eshop(game_surf)
    elif current_screen == "album":
        draw_album(game_surf)
    elif current_screen == "settings":
        draw_settings(game_surf)
    elif current_screen == "news":
        draw_news(game_surf)
    elif current_screen == "profile":
        draw_profile(game_surf)
    elif current_screen == "themes":
        draw_themes(game_surf)
    elif current_screen == "stats":
        draw_stats(game_surf)
    elif current_screen == "controllers":
        draw_controllers(game_surf)
    elif current_screen == "system":
        draw_system(game_surf)
    elif current_screen == "data":
        draw_data(game_surf)
    elif current_screen == "help":
        draw_help(game_surf)
    elif current_screen == "gamechat":
        draw_gamechat(game_surf)

    apply_brightness(game_surf)
    surface.blit(game_surf, (SCREEN_X, SCREEN_Y))

# Individual draw functions for each screen
def draw_home_menu(surf):
    overlay = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    for i, icon in enumerate(ICONS):
        rect = get_icon_rect(i)
        if hovered_icon == i:
            overlay.fill(HIGHLIGHT)
            surf.blit(overlay, (rect.topleft[0] - SCREEN_X, rect.topleft[1] - SCREEN_Y))
        if selected_icon == i:
            pygame.draw.rect(surf, ACCENT_COLOR, (rect.left - SCREEN_X, rect.top - SCREEN_Y, rect.width, rect.height), 4, border_radius=12)
        FONT_ICON.render_to(surf, (rect.centerx - SCREEN_X - 20, rect.centery - SCREEN_Y - 30), icon["emoji"], TEXT_COLOR)
        label_w = FONT_LABEL.get_rect(icon["label"]).width
        FONT_LABEL.render_to(surf, (rect.centerx - SCREEN_X - label_w//2, rect.centery - SCREEN_Y + 20), icon["label"], TEXT_COLOR)

def draw_game_demo(surf):
    for y in range(SCREEN_H):
        r = clamp_color(100 + 50 * math.sin(y / 30))
        g = clamp_color(180 + 30 * math.cos(y / 40))
        b = clamp_color(50 + 70 * math.sin(y / 50))
        pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_W, y))
    track_y = SCREEN_H - 80
    pygame.draw.rect(surf, (80, 80, 80), (0, track_y, SCREEN_W, 80))
    for i in range(0, SCREEN_W, 40):
        pygame.draw.rect(surf, (255, 255, 0), (i, track_y + 35, 25, 8))
    t = pygame.time.get_ticks() / 1000
    for i in range(4):
        x = (t * 80 + i * 100) % (SCREEN_W + 100) - 50
        y = track_y - 20 + 5 * math.sin(t * 3 + i)
        kart = pygame.Surface((40, 30), pygame.SRCALPHA)
        color = [(255,0,0), (0,255,0), (0,0,255), (255,255,0)][i]
        pygame.draw.ellipse(kart, color, (5, 5, 30, 20))
        pygame.draw.circle(kart, (30,30,30), (10, 25), 6)
        pygame.draw.circle(kart, (30,30,30), (30, 25), 6)
        surf.blit(kart, (x, y))
    FONT_BIG.render_to(surf, (SCREEN_W//2 - 100, 20), "MARIO KART 8", (255, 220, 0))

def draw_eshop(surf):
    FONT_BIG.render_to(surf, (20, 20), "Nintendo eShop", TEXT_COLOR)
    # Fake games
    for i in range(5):
        pygame.draw.rect(surf, ACCENT_COLOR, (20 + (i%3)*150, 60 + (i//3)*140, 120, 120), border_radius=10)
        FONT_LABEL.render_to(surf, (30 + (i%3)*150, 190 + (i//3)*140), f"Game {i+1} - ${random.randint(20,60)}.99", TEXT_COLOR)

def draw_album(surf):
    FONT_BIG.render_to(surf, (20, 20), "Album", TEXT_COLOR)
    # Fake screenshots
    for i, img in enumerate(album_images):
        col = i % 4
        row = i // 4
        pygame.draw.rect(surf, img["color"], (20 + col*110, 60 + row*110, 100, 80))

def draw_settings(surf):
    FONT_BIG.render_to(surf, (20, 20), "System Settings", TEXT_COLOR)
    overlay = pygame.Surface((ICON_SIZE, ICON_SIZE), pygame.SRCALPHA)
    for i, icon in enumerate(SETTINGS_ICONS):
        rect = get_icon_rect(i, start_x=40, start_y=80, spacing=90, cols=3)
        if hovered_icon == i + 100:  # Offset for settings hover
            overlay.fill(HIGHLIGHT)
            surf.blit(overlay, (rect.left, rect.top))
        FONT_ICON.render_to(surf, (rect.centerx - 20, rect.centery - 30), icon["emoji"], TEXT_COLOR)
        label_w = FONT_LABEL.get_rect(icon["label"]).width
        FONT_LABEL.render_to(surf, (rect.centerx - label_w//2, rect.centery + 20), icon["label"], TEXT_COLOR)
    # Brightness slider
    pygame.draw.rect(surf, (60,60,60), (20, 200, 200, 20), border_radius=10)
    pygame.draw.rect(surf, ACCENT_COLOR, (20, 200, int(200 * brightness), 20), border_radius=10)
    # Volume slider
    pygame.draw.rect(surf, (60,60,60), (20, 230, 200, 20), border_radius=10)
    pygame.draw.rect(surf, ACCENT_COLOR, (20, 230, int(200 * volume_level), 20), border_radius=10)

def draw_news(surf):
    FONT_BIG.render_to(surf, (20, 20), "News", TEXT_COLOR)
    news_articles = ["Latest Switch 2 Updates", "New Game Releases", "System Patch Notes", "Upcoming Events"]
    for i, article in enumerate(news_articles):
        FONT_SMALL.render_to(surf, (20, 60 + i*40), f"{article}: Details here.", TEXT_COLOR)

def draw_profile(surf):
    FONT_BIG.render_to(surf, (20, 20), "Profile", TEXT_COLOR)
    pygame.draw.circle(surf, (100,100,100), (SCREEN_W//2, 80), 50)  # Mii placeholder
    FONT_SMALL.render_to(surf, (20, 140), "User: GrokPlayer", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 160), "Friends:", TEXT_COLOR)
    for i, friend in enumerate(friends):
        FONT_SMALL.render_to(surf, (40, 180 + i*20), friend, TEXT_COLOR)

def draw_themes(surf):
    FONT_BIG.render_to(surf, (20, 20), "Themes", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 60), "Select theme: Light / Dark / Custom", TEXT_COLOR)

def draw_stats(surf):
    FONT_BIG.render_to(surf, (20, 20), "Play Stats", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 60), "Hours played: 100", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 80), "Games completed: 5", TEXT_COLOR)

def draw_controllers(surf):
    FONT_BIG.render_to(surf, (20, 20), "Controllers", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 60), "Paired: Left Joy-Con, Right Joy-Con", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 80), "Find Controllers: Vibrate", TEXT_COLOR)

def draw_system(surf):
    FONT_BIG.render_to(surf, (20, 20), "System Info", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 60), "Version: 20.5.0", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 80), "Update available? No", TEXT_COLOR)

def draw_data(surf):
    FONT_BIG.render_to(surf, (20, 20), "Data Management", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 60), "Storage: 32GB used / 64GB total", TEXT_COLOR)

def draw_help(surf):
    FONT_BIG.render_to(surf, (20, 20), "Help & FAQ", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 60), "Q: How to play? A: Click icons.", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 80), "Q: Battery issues? A: Charge console.", TEXT_COLOR)

def draw_gamechat(surf):
    FONT_BIG.render_to(surf, (20, 20), "GameChat", TEXT_COLOR)
    FONT_SMALL.render_to(surf, (20, 60), "Voice chat rooms: Room 1 (0/12)", TEXT_COLOR)

# ------------------------------------------------------------
# Draw HUD
# ------------------------------------------------------------
def draw_hud(surface):
    hud_rect = Rect(0, 0, WIN_W, 50)
    pygame.draw.rect(surface, HUD_COLOR, hud_rect)
    pygame.draw.line(surface, (60,60,60), (0,50), (WIN_W,50), 1)

    FONT_BIG.render_to(surface, (15, 8), "Switch One", TEXT_COLOR)

    profile_rect = Rect(15, 5, 40, 40)
    pygame.draw.circle(surface, (100,100,100), profile_rect.center, 18)
    if hovered_icon == -1:
        pygame.draw.circle(surface, ACCENT_COLOR, profile_rect.center, 18, 3)
    FONT_ICON.render_to(surface, (25, -5), "👤", TEXT_COLOR)

    wifi_x = WIN_W - 140
    for i, r in enumerate([30, 20, 10]):
        pygame.draw.arc(surface, TEXT_COLOR, (wifi_x + 15 + 6*i, 12 + 6*i, r, r), 0, 1.6, 2)

    bat_x = WIN_W - 80
    pygame.draw.rect(surface, TEXT_COLOR, (bat_x, 18, 28, 12), 2)
    pygame.draw.rect(surface, TEXT_COLOR, (bat_x + 28, 21, 3, 6))
    fill = 22 if simulation_on else 10
    pygame.draw.rect(surface, ACCENT_COLOR if simulation_on else POWER_OFF,
                     (bat_x + 3, 21, fill, 6))

    now = datetime.datetime.now().strftime("%H:%M")
    FONT_SMALL.render_to(surface, (WIN_W - 100, 15), now, TEXT_COLOR)

# ------------------------------------------------------------
# Draw Bottom Bar
# ------------------------------------------------------------
def draw_bottom_bar(surface):
    bar_rect = Rect(0, WIN_H - 50, WIN_W, 50)
    pygame.draw.rect(surface, HUD_COLOR, bar_rect)
    pygame.draw.line(surface, (60,60,60), (0, WIN_H-50), (WIN_W, WIN_H-50), 1)

    home_x = WIN_W // 2 - 25
    pygame.draw.circle(surface, (60,60,60), (home_x, WIN_H - 25), 18)
    pygame.draw.circle(surface, ACCENT_COLOR, (home_x, WIN_H - 25), 18, 3)
    FONT_ICON.render_to(surface, (home_x - 12, WIN_H - 43), "🏠", ACCENT_COLOR)

    power_x = WIN_W - 80
    power_y = WIN_H - 25
    pygame.draw.circle(surface, (40,40,40), (power_x, power_y), 18)
    pygame.draw.circle(surface, POWER_ON if simulation_on else POWER_OFF, (power_x, power_y), 18, 3)
    FONT_ICON.render_to(surface, (power_x - 10, power_y - 18), "⏻", POWER_ON if simulation_on else POWER_OFF)

    vol_x = 60
    pygame.draw.rect(surface, (60,60,60), (vol_x, WIN_H - 35, 100, 20), border_radius=10)
    pygame.draw.rect(surface, ACCENT_COLOR, (vol_x, WIN_H - 35, int(100 * volume_level), 20), border_radius=10)

# ------------------------------------------------------------
# Main Loop
# ------------------------------------------------------------
running = True
dragging_brightness = False
dragging_volume = False
while running:
    mx, my = pygame.mouse.get_pos()
    hovered_icon = None

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:  # Capture screenshot
                if simulation_on and not locked:
                    album_images.append({"color": (random.randint(0,255), random.randint(0,255), random.randint(0,255))})
                    print(">>> Screenshot captured")

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if locked:
                locked = False
                print(">>> Unlocked")
                continue

            # Toggle Joy-Con mode (click on left Joy-Con area)
            if detached_joycons and Rect(20, 100, 80, 200).collidepoint(mx, my):
                detached_joycons = not detached_joycons
                print(">>> Joy-Cons attached/detached")

            # Profile click
            if pygame.Rect(15, 5, 40, 40).collidepoint(mx, my):
                current_screen = "profile"
                print(">>> Profile clicked")

            # Home icons
            if current_screen == "home":
                for i in range(len(ICONS)):
                    if get_icon_rect(i).collidepoint(mx, my):
                        selected_icon = i
                        current_screen = ICONS[i]["id"]
                        print(f">>> {ICONS[i]['label']} selected")
                        break

            # Settings sub-icons
            elif current_screen == "settings":
                for i in range(len(SETTINGS_ICONS)):
                    rect = get_icon_rect(i, start_x=SCREEN_X + 40, start_y=SCREEN_Y + 80, spacing=90, cols=3)
                    if rect.collidepoint(mx, my):
                        print(f">>> Settings: {SETTINGS_ICONS[i]['label']} selected")
                        # For example, open sub-screen if needed

            # Brightness slider drag
            if current_screen == "settings" and pygame.Rect(SCREEN_X + 20, SCREEN_Y + 200, 200, 20).collidepoint(mx, my):
                dragging_brightness = True
            # Volume slider drag (bottom bar)
            if pygame.Rect(60, WIN_H - 35, 100, 20).collidepoint(mx, my):
                dragging_volume = True

            # Home button
            home_btn = pygame.Rect(WIN_W//2 - 25 - 9, WIN_H - 25 - 9, 36, 36)
            if home_btn.collidepoint(mx, my):
                current_screen = "home"
                selected_icon = None
                print(">>> Home")

            # Power button
            power_btn = pygame.Rect(WIN_W - 100, WIN_H - 45, 40, 40)
            if power_btn.collidepoint(mx, my):
                power_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_brightness = False
            dragging_volume = False
            if power_pressed:
                power_btn = pygame.Rect(WIN_W - 100, WIN_H - 45, 40, 40)
                if power_btn.collidepoint(mx, my):
                    simulation_on = not simulation_on
                    locked = not simulation_on
                    print(f">>> Simulation {'ON' if simulation_on else 'OFF'}")
                power_pressed = False

        elif event.type == pygame.MOUSEMOTION:
            # Hover
            if current_screen == "home":
                for i in range(len(ICONS)):
                    if get_icon_rect(i).collidepoint(mx, my):
                        hovered_icon = i
                        break
            elif current_screen == "settings":
                for i in range(len(SETTINGS_ICONS)):
                    rect = get_icon_rect(i, start_x=SCREEN_X + 40, start_y=SCREEN_Y + 80, spacing=90, cols=3)
                    if rect.collidepoint(mx, my):
                        hovered_icon = i + 100
                        break
            if pygame.Rect(15, 5, 40, 40).collidepoint(mx, my):
                hovered_icon = -1

            if dragging_brightness:
                slider_x = max(0, min(200, mx - SCREEN_X - 20))
                brightness = slider_x / 200
            if dragging_volume:
                slider_x = max(0, min(100, mx - 60))
                volume_level = slider_x / 100

    # Sleep mode simulation
    if simulation_on and not locked and pygame.time.get_ticks() - lock_time > 30000:  # 30 sec idle
        locked = True
        lock_time = pygame.time.get_ticks()

    screen.fill(BG_COLOR)
    draw_joycons(screen)
    draw_screen(screen)
    draw_hud(screen)
    draw_bottom_bar(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
