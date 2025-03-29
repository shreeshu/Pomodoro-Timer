import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import os

import winsound

# Play sound when the timer ends

# Pastel colour scheme
COLOURS = ["#FAEDCB", "#C9E4DE", "#C6DEF1", "#DBCDF0", "#A99ABD", "#FA9BCF"]

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x300")
        self.root.configure(bg=COLOURS[0])

        # Set defaults
        self.default_time = 30 * 60 
        self.time_left = self.default_time
        self.running = False

        # Icons for the buttons
        image_path_start = resource_path("icons/pomo_start.png")
        image_path_stop = resource_path("icons/pomo_stop.png")
        self.start_icon = ImageTk.PhotoImage(Image.open(image_path_start))
        self.stop_icon = ImageTk.PhotoImage(Image.open(image_path_stop))

        # Title and timer label
        self.label = tk.Label(root, text="Pomodoro Timer", font=("Helvetica", 24), bg=COLOURS[0], fg=COLOURS[1])
        self.label.pack(pady=20)

        # Display the remaining time on the Pomodoro timer.
        self.time_label = tk.Label(root, text=self.format_time(self.time_left), font=("Helvetica", 48), bg=COLOURS[0], fg=COLOURS[2])
        self.time_label.pack(pady=20)

        # Start, stop, and reset buttons
        self.start_button = tk.Button(root, image=self.start_icon, text="Start", command=self.start_timer, font=("Helvetica", 18), bg=COLOURS[0], borderwidth=0, highlightthickness=0)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(root, image=self.stop_icon, text="Stop", command=self.stop_timer, font=("Helvetica", 18), bg=COLOURS[0], borderwidth=0, highlightthickness=0)
        self.stop_button.pack(side=tk.RIGHT, padx=10)
        
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_timer, font=("Helvetica", 12), bg=COLOURS[3], fg="white", borderwidth=0)
        self.reset_button.pack(side=tk.BOTTOM, pady=10)

    def format_time(self, seconds):
        """
        Format the given time in seconds to a string representation of minutes and seconds.

        This function takes a total number of seconds and converts it to a formatted string
        in the format "MM:SS", where MM represents minutes and SS represents seconds.

        Parameters:
        seconds (int): The total number of seconds to be formatted.

        Returns:
        str: A string representation of the time in the format "MM:SS".
             Minutes and seconds are both zero-padded to two digits.

        Example:
        >>> format_time(125)
        '02:05'
        """
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"


    def start_timer(self):
        """
        Start the Pomodoro timer if it's not already running.

        This method sets the 'running' flag to True and initiates the timer update process.
        If the timer is already running, this method has no effect.

        Parameters:
        None

        Returns:
        None
        """
        if not self.running:
            self.running = True
            self.update_timer()


    def stop_timer(self):
        """
        Stop the Pomodoro timer if it's currently running.

        This method sets the 'running' flag to False and cancels the scheduled timer update.
        If the timer is not running, this method has no effect.

        Parameters:
        None

        Returns:
        None
        """
        if self.running:
            self.running = False
            self.root.after_cancel(self.timer_id)


    def reset_timer(self):
        """
        Reset the Pomodoro timer to its default state.

        This method stops the timer if it's running, resets the remaining time
        to the default duration, and updates the time display.

        Parameters:
        None

        Returns:
        None
        """
        self.running = False
        self.time_left = self.default_time
        self.time_label.config(text=self.format_time(self.time_left))


    def update_timer(self):
        """
        The function `update_timer` decreases the time left by 1 second, updates the time label, and
        displays a message when the time is up.
        """
        if self.running and self.time_left:
            self.time_left -= 1
            self.time_label.config(text=self.format_time(self.time_left))
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.time_left == 0:
            self.running = False
            winsound.PlaySound("alarm.wav", winsound.SND_FILENAME)
            messagebox.showinfo("Time's up!", "Your Pomodoro session is over!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()