from tkinter import *
from tkinter.ttk import *
import time
from tkinter import messagebox
import json


# UI -------------------------------------------------------------------------------------------------------------------
class TypingUI(Tk):
    def __init__(self):
        # Initialize Tk
        super().__init__()
        # Initialize Tk window (self is window now)
        self.title("Watermarker")
        self.config(padx=40, pady=40)

        # Read the best time from best_time.json
        self.best_cpm = self.read_best_speed()
        # Test text
        self.test_text = "Some very interesting text to read and type as fast as you possibly can."

        # Main UI
        self.label_description = Label(text="Type the following text precisely:", font=("Segoe UI", 12))
        self.label_description.grid(column=0, row=1, columnspan=2, pady=(0, 40), sticky="EW")
        self.label_text = Label(text=self.test_text, wraplength=600, font=("Segoe UI", 12, "bold"))
        self.label_text.grid(column=0, row=2, columnspan=2, pady=(0, 40), sticky="EW")
        self.textarea = Text(self, width=70, height=10, relief="solid", font=("Segoe UI", 12))
        self.textarea.grid(column=0, row=3, columnspan=2, sticky="EW")
        # Tag for wrongly typed characters
        self.textarea.tag_configure("mistake", foreground="red")
        # Set focus on textarea
        self.textarea.focus_set()
        # Best CPM
        self.label_best = Label(text=f"Your best:  {self.best_cpm} CPM", wraplength=600, font=("Segoe UI", 12))
        self.label_best.grid(column=1, row=4, sticky="E")

        # Detect keypress to start the test
        self.textarea.bind("<KeyPress>", self.start_test)
        # Detect keyrelease for ending the test
        self.textarea.bind("<KeyRelease>", self.writing)
        # Variable to record the starting time
        self.start_time = 0
        # Variable to know if this is the first time a key was pressed inside textarea
        self.key_stroke = 0

    def start_test(self, event=None):
        """Starts counting time of the test."""
        # Reset time, when one test finishes and another starts
        if self.key_stroke == 0:
            self.key_stroke += 1
            print("start")
            # Make sure textarea is focused
            self.textarea.focus_set()
            # Start counting time
            self.start_time = time.time()

    def writing(self, event=None):
        """Gets triggered with <KeyRelease> event. Calls self.stop_test, when the text is correctly typed.
        Receives event object as parameter."""
        # if self.key_stroke == 0:
        #     self.start_test()
        #     self.key_stroke += 1
        typed_text = self.textarea.get("1.0", END)
        # Text length is always length of the actual text + 1
        if len(self.test_text) + 1 == len(typed_text):
            self.compare_text(typed_text)
            self.stop_test()

    def compare_text(self, typed_text):
        mistake_pos = []
        line_index = 0

        for i in range(len(self.test_text)):
            if typed_text[i] != self.test_text[i]:
                mistake_pos.append(i)
                self.textarea.tag_add("mistake", f"1.{i}")

        print(mistake_pos)

    def stop_test(self):
        """Stops the test and shows results."""
        # Reset key_stroke when test finishes, so another can start
        self.key_stroke = 0
        end_time = time.time()
        result_time = end_time - self.start_time
        final_time = "{:.2f}".format(result_time)
        cpm_speed = int(len(self.test_text) / (result_time / 60))
        result_window = messagebox.showinfo(title="Results", message=f"Your time is: {final_time}s. \n"
                                                                     f"Your typing speed is {cpm_speed}CPM (characters "
                                                                     f"per minute).")
        # Write the new record
        if cpm_speed > self.best_cpm:
            self.write_best_speed(cpm_speed)
        # Update Best SPM Label with the new record
        self.label_best.config(text=f"Your best:  {self.read_best_speed()} CPM")
        print(final_time)

    def read_best_speed(self) -> int:
        """Reads the best CPM speed from JSON file id there is any.
        Return:
        best_time : int"""
        try:
            with open("best_time.json", "r", encoding="utf-8") as file:
                best_time = json.load(file)
            # String has to be converted first to float and then to integer, in case it has floating point
            return int(float(best_time["best_cpm"]))
        # If the file is empty, do nothing
        except (json.decoder.JSONDecodeError, FileNotFoundError) as exception:
            return 0

    def write_best_speed(self, cpm_speed: int):
        """Writes the new best cpm_speed in JSON file."""
        best_cpm_dict = {
            "best_cpm": cpm_speed,
        }
        # If this is the best or first time, write it to best_time.json
        with open("best_time.json", "w", encoding="utf-8") as file:
            json.dump(best_cpm_dict, file, indent=4)
