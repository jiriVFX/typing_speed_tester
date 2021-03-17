from tkinter import *
from tkinter.ttk import *
import time
from tkinter import messagebox


# from timeit import default_timer as timer


# UI -------------------------------------------------------------------------------------------------------------------
class TypingUI(Tk):
    def __init__(self):
        # Initialize Tk
        super().__init__()
        # Initialize Tk window (self is window now)
        self.title("Watermarker")
        self.config(padx=40, pady=40)

        self.test_text = "Some very interesting text to read and type as fast as you possibly can."
        # Main UI
        self.label_text = Label(text=self.test_text, wraplength=600, font=("Segoe UI", 12))
        self.label_text.grid(column=0, row=0, columnspan=2, pady=(0, 40), sticky="EW")
        self.textarea = Text(self, width=70, height=10, relief="solid", font=("Segoe UI", 12))
        self.textarea.grid(column=0, row=1, columnspan=2, sticky="EW")
        self.textarea.focus_set()
        # self.button_start = Button(text="Press Enter to Start", command=self.start_test)
        # self.button_start.focus_set()
        # self.button_start.grid(column=0, row=2, columnspan=2, pady=(40, 0), sticky="EW")
        # self.grid_columnconfigure(0, weight=1)

        # Detect Enter being pressed - start test
        # self.button_start.bind("<Return>", self.start_test)
        # Detect keypress
        self.textarea.bind("<KeyPress>", self.writing)
        # Variable to record the starting time
        self.start_time = 0
        # Variable to know if this is the first time a key was pressed inside textarea
        self.key_stroke = 0

    def start_test(self, event=None):
        # Reset time, when one test finishes and another starts
        self.start_time = 0
        print("start")
        # Make textarea focused
        self.textarea.focus_set()
        # Start counting time
        self.start_time = time.time()

    def writing(self, event):
        if self.key_stroke == 0:
            self.start_test()
            self.key_stroke += 1
        if len(self.test_text) == len(self.textarea.get("1.0", END)):
            self.stop_test()

    def stop_test(self):
        # Reset key_stroke when test finishes, so another can start
        self.key_stroke = 0
        end_time = time.time()
        result_time = end_time - self.start_time
        final_time = "{:.2f}".format(result_time)
        cpm_speed = "{:.2f}".format(len(self.test_text) / (result_time / 60))
        result_window = messagebox.showinfo(title="Results", message=f"Your time is: {final_time}s. \n"
                                                                      f"Your typing speed is {cpm_speed} characters "
                                                                      f"per minute.")
        print(final_time)
