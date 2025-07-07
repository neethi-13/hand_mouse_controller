# main.py
from hand_controller import HandMouseController
from ui import AppUI

def start_controller():
    controller = HandMouseController()
    controller.start_control()

if __name__ == "__main__":
    app = AppUI(start_controller)
    app.run()
