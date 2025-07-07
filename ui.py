# ui.py
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class AppUI:
    def __init__(self, start_callback):
        self.root = tb.Window(themename="flatly")
        self.root.title("🖐️ AI Hand Gesture Mouse Controller")
        self.root.geometry("600x500")
        self.root.resizable(True, True)

        self.root.configure(background="#f0f0f0")

        tb.Label(self.root,
                 text="🖥️ Control Your Mouse with Hand Gestures",
                 font=("Segoe UI", 20, "bold"),
                
                 ).pack(pady=(30, 20))
        tb.Button(self.root,
                  text="▶ Start Hand Control",
                  bootstyle="success",
                  command=start_callback,
                  width=30
                  ).pack(pady=20)

        tb.Label(self.root,
                 text="📘 Supported Gestures:",
                 font=("Segoe UI", 16, "bold"),
                 bootstyle="info"
                 ).pack(pady=(20, 20))

        info = (
            "🖱️ Move Mouse → Index Finger\n\n"
            "👆 Click → Pinch (Thumb + Index Tip)\n\n"
            "📜 Scroll Up → Index + Middle Up\n\n"
            "📥 Scroll Down → Index Up, Middle Down\n\n"
            "🔍 Zoom In → Pinch (Thumb + Middle)\n\n"
            "🔎 Zoom Out → Pinch (Thumb + Ring)\n\n"
            "❌ Quit → Press 'q' on keyboard"
        )

        tb.Label(self.root,
                 text=info,
                 font=("Segoe UI", 11),
                 bootstyle="secondary",
                 justify="left"
                 ).pack(padx=30, pady=10)

    def run(self):
        self.root.mainloop()
