import pyautogui

import win32gui

import os


class Camera:
    _instance = None

    def __init__(self, window_title):
        self.window_title = window_title
        self.game_window = None
        self.find_game_window()

    def __new__(cls, window_title):
        if cls._instance is None:
            print("Creating new Camera instance")
            cls._instance = super(Camera, cls).__new__(cls)
            cls._instance.window_title = window_title
            cls._instance.game_window = None
        else:
            print("Using existing Camera instance")
        return cls._instance

    def find_game_window(self):
        title = self.window_title
        self.game_window = win32gui.FindWindow(None, title)
        if self.game_window:
            print(f"Window '{title}' found, handle {self.game_window}")
        else:
            print(f"Window '{title}' not found.")

    def take_screenshot(self, area=None, save_image=False, action="ufo"):
        if not self.game_window or not win32gui.IsWindowVisible(self.game_window):
            print("Game window not found or not visible. Cannot take screenshot.")
            return None

        window_rect = win32gui.GetWindowRect(self.game_window)
        if area:
            region = (
                window_rect[0] + area[0],
                window_rect[1] + area[1],
                area[2],
                area[3],
            )
        else:
            region = window_rect

        screenshot = pyautogui.screenshot(region=region)

        if save_image:
            if not os.path.exists("screenshots"):
                os.makedirs("screenshots")
            file_path = os.path.join(
                "screenshots", f"{pyautogui.time.time()}_{action}.png"
            )
            screenshot.save(file_path)
            print(f"Screenshot saved to {file_path}")

        return screenshot
