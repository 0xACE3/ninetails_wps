from src.models import KeyStrokeListener, AutoTyper
from src.gui import CaptureGui


class ScreenCaptureController:
    def __init__(self):
        self.view = CaptureGui(self)
        self.keystroke_listener = KeyStrokeListener()
        self.autotyper = AutoTyper()

        # subscribing to keystroke listener
        self.keystroke_listener.attach(self.autotyper)

    def run(self):
        self.view.main()

    def on_button_click(self, event: str):
        if "capture" in event.lower():
            self.keystroke_listener.start_capturing(self.view)

        if "stop" in event.lower():
            self.keystroke_listener.deactivate()
            self.view.shutdown()


