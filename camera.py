import pyautogui

import win32gui

import os


class Camera:
    def __init__(self, window_title):
        self.window_title = window_title
        self.game_window = None
        self.find_game_window()

    def find_game_window(self, title=None):
        if title is None:
            title = self.window_title
        self.game_window = win32gui.FindWindow(None, title)
        if self.game_window:
            print(f"Window '{title}' found, handle {self.game_window}")
        else:
            print(f"Window '{title}' not found.")

    def take_screenshot(self, area=None, save_image=False):
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
                "screenshots", f"screenshot_{pyautogui.time.time()}.png"
            )
            screenshot.save(file_path)
            print(f"Screenshot saved to {file_path}")

        return screenshot