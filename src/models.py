from os.path import join, abspath, dirname
from pytesseract import pytesseract
from src.gui import CaptureGui
from pynput import keyboard
import numpy as np
import cv2 as cv
import pyautogui
import threading
import time
import os


class ScreenCapture:
    PATH = join(dirname(dirname(abspath(__file__))))

    def __init__(self):
        # Screen capturing variables
        self.capturing_thread = None
        self.frames = []

    def start_capturing(self, view: CaptureGui) -> None:
        self.capturing_thread = threading.Thread(target=self.capture_screen, args=[view])
        self.capturing_thread.start()

    def capture_screen(self, view: CaptureGui) -> None:
        # path to store screenshots
        path = ScreenCapture.file_path()

        # screen info

        width = view.capture_frm.winfo_width()
        height = view.capture_frm.winfo_height()

        # position info
        start_x = view.winfo_x() + view.capture_frm.winfo_x() + 19
        start_y = view.winfo_y() + view.capture_frm.winfo_y() + 78

        screenshot = pyautogui.screenshot(region=(start_x, start_y, width, height))
        frame = cv.cvtColor(np.array(screenshot), cv.COLOR_BGR2RGB)

        # save it to list of frames
        self.frames.append(frame)

        # save it locally

        screenshot.save(path)
        print("Screenshot Captured & Saved.")

    @staticmethod
    def file_path() -> str:
        file_name = f'captured_sc{time.strftime("%H-%M-%S_%d-%m-%Y", time.localtime())}.jpg'
        file_path = join(ScreenCapture.PATH, "screenshots")
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        final_path = join(file_path, file_name)
        return final_path


class ListenerSubject(ScreenCapture):

    def __init__(self):
        super().__init__()
        self._observers = []

    def notify(self):
        print("Notifying all observers")
        for observer in self._observers:
            observer.update(self)

    def attach(self, observer) -> None:
        print(f"Attached observer: {observer.__class__.__name__}")
        self._observers.append(observer)

    def detach(self, observer) -> None:
        print(f"Detached observer: {observer.__class__.__name__}")
        self._observers.remove(observer)


class KeyStrokeListener(ListenerSubject):

    def __init__(self):
        super().__init__()
        self.keyboard_listener = keyboard.Listener(on_press=self._handle_keystroke)
        self.keyboard_listener.start()
        print("Started Listening to KeyStrokes")
        self.activate = False

    def _handle_keystroke(self, key):

        if key == keyboard.Key.f2:
            print("F2 Key Pressed")
            if not self.activate:
                self.activate = True
                self.notify()

    def deactivate(self):
        if self.activate:
            print("Stopped Listening to KeyStrokes")
            self.keyboard_listener.stop()
            self.activate = False


class AutoTyper:

    def __init__(self):
        pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    def auto_type(self, text: str, wps=50, interval=0.03, is_delay=True):
        wpm = wps * 60 / 5
        delay = 1 / wpm * 60
        for word in text.split():
            pyautogui.typewrite(f"{word} ", interval=interval)
            if is_delay:
                time.sleep(delay)

    def extract_text(self, images) -> str:
        print("Extracting Text")
        text_lines = []
        for img in images:
            text: str = pytesseract.image_to_string(img)
            text_lines.extend(text.split("\n"))

        final_text = list(dict.fromkeys(text_lines))
        final_text = " ".join(final_text)

        return final_text

    def update(self, subject, delay=3):
        if subject.activate:
            text = self.extract_text(subject.frames)
            print("Starting to type in 3 secs...")
            time.sleep(delay)
            self.auto_type(text)

            subject.activate = False
            subject.frames = []
