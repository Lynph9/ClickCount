"""GUI tool for tracking left mouse clicks in 200-click batches.

The tool listens for global left mouse button presses, counts up to 200,
plays a system bell when the batch target is reached, and resets the
per-batch counter while incrementing a batch total.
"""
import tkinter as tk
from queue import SimpleQueue
from typing import NoReturn

from pynput import mouse

BATCH_TARGET = 200
POLL_MS = 50


class ClickCounterApp:
    """Tkinter application that tracks global left-click counts."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Click Counter")
        self.root.geometry("320x160")
        self.root.resizable(False, False)

        self.current_clicks = 0
        self.completed_batches = 0
        self.events = SimpleQueue[str]()

        self._build_ui()
        self.listener = mouse.Listener(on_click=self._on_click)
        self.listener.start()

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self._poll_events()

    def _build_ui(self) -> None:
        header = tk.Label(
            self.root,
            text="Left-click tracker",
            font=("Arial", 14, "bold"),
            pady=10,
        )
        header.pack()

        self.batch_label = tk.Label(
            self.root,
            text="Completed batches: 0",
            font=("Arial", 12),
            pady=5,
        )
        self.batch_label.pack()

        self.current_label = tk.Label(
            self.root,
            text=f"Current batch: 0 / {BATCH_TARGET}",
            font=("Arial", 12),
            pady=5,
        )
        self.current_label.pack()

        info = tk.Label(
            self.root,
            text=(
                "Counts only left mouse clicks.\n"
                "Each 200 clicks resets and increments batches."
            ),
            font=("Arial", 10),
            pady=10,
        )
        info.pack()

    def _on_click(self, _x: int, _y: int, button: mouse.Button, pressed: bool) -> None:
        if pressed and button == mouse.Button.left:
            self.events.put("click")

    def _poll_events(self) -> None:
        while not self.events.empty():
            self._handle_event(self.events.get())
        self.root.after(POLL_MS, self._poll_events)

    def _handle_event(self, event: str) -> None:
        if event != "click":
            return
        self.current_clicks += 1
        if self.current_clicks >= BATCH_TARGET:
            self.completed_batches += 1
            self.current_clicks = 0
            self.root.bell()
        self._refresh_labels()

    def _refresh_labels(self) -> None:
        self.batch_label.config(text=f"Completed batches: {self.completed_batches}")
        self.current_label.config(
            text=f"Current batch: {self.current_clicks} / {BATCH_TARGET}"
        )

    def run(self) -> NoReturn:
        self.root.mainloop()

    def _on_close(self) -> None:
        if self.listener is not None:
            self.listener.stop()
        self.root.destroy()


def main() -> None:
    app = ClickCounterApp()
    app.run()


if __name__ == "__main__":
    main()
