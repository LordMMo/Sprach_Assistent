import tkinter as tk
import pyttsx3


def format_time(time_value):
    return f"{time_value:02d}"


class TimerGUI:
    def __init__(self, minutes, seconds):
        self.minutes = minutes
        self.seconds = seconds
        self.root = tk.Tk()
        self.root.title("Timer")
        self.root.geometry("300x400")

        # Label für Timer-Anzeige
        self.timer_label = tk.Label(self.root, text=f"{format_time(self.minutes)}:{format_time(self.seconds)}",
                                    font=("Helvetica", 48))
        self.timer_label.pack(pady=20)

        # Variable für die Timer-ID
        self.timer_id = None

        # Timer automatisch starten
        self.start_timer()

        # Sprachausgabe-Engine initialisieren
        self.engine = pyttsx3.init()

    def update_label(self, remaining_minutes, remaining_seconds):
        self.timer_label.config(text=f"{format_time(remaining_minutes)}:{format_time(remaining_seconds)}")

    def show_timer_expired(self):
        self.timer_label.config(text="00:00")
        self.engine.say("Der Timer ist abgelaufen!")
        self.engine.runAndWait()
        self.root.after(2000, self.root.destroy)  # Warte 2 Sekunden und schließe die GUI

    def start_timer(self):
        total_seconds = self.minutes * 60 + self.seconds
        self.timer_id = self.root.after(1000, self.run_timer_callback, total_seconds)

    def run_timer_callback(self, remaining_seconds):
        self.run_timer(remaining_seconds)

    def run_timer(self, remaining_seconds):
        if remaining_seconds > 0:
            minutes, seconds = divmod(remaining_seconds, 60)
            self.update_label(minutes, seconds)
            self.timer_id = self.root.after(1000, self.run_timer_callback, remaining_seconds - 1)
        else:
            self.show_timer_expired()

    def start(self):
        self.root.mainloop()
