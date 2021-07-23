from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0  # global variable - used to get countdown timer to count down from a different number of minutes
timer = None
# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    start_button.config(state="normal")
    # reset checkmarks, stop the timer, text inside the timer, and change the title text to the original title
    window.after_cancel(timer)   # cancels the timer previously set up with after()
    canvas.itemconfig(timer_text, text="00:00")  # reset timer
    timer_label.config(text="pomodoro timer", font=("Bahnschrift", 30), fg=GREEN)  # reset timer label
    checkmark_label.config(text="")  # reset checkmarks
    global reps
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    # responsible for calling count_down
    # will be triggered after start button is pressed
    # pass in the starting count (# minutes * 60 secs), needs to be called after canvas is made
    global reps

    start_button.config(state="disabled")
    reps += 1
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # if it's the 8th rep, take a long 20 minute break
    if reps % 8 == 0:
        timer_label.config(text="take a long break!\nyou deserve it!", font=("Bahnschrift", 30), fg=RED, width=15,
                           height=2)
        count_down(long_break_sec)

    # if it's the 2nd, 4th, 6th rep, take a short 5 minute break
    elif reps % 2 == 0:
        timer_label.config(text="take a quick break!", font=("Bahnschrift", 30), fg=PINK, width=15, height=2)
        count_down(short_break_sec)

    # if it's the 1st, 3rd, 5th, 7th rep, work for 25 minutes
    else:
        timer_label.config(text="get to work!", font=("Bahnschrift", 30), fg=GREEN, width=15, height=2)
        count_down(work_sec)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# event-driven GUI program: will constantly refresh and listen for events. once it happens, has to react to the event.
# driven through window.mainloop() - every millisecond it's checking to see if something's happened
# this is why another loop can't be used in the program - it won't reach the mainloop, and the program won't even launch


def count_down(count):
    global reps
    count_min = math.floor(count / 60)  # get minutes by rounding down to get rid of remainder
    count_sec = count % 60  # get remaining seconds after minutes are taken away
    if count_sec < 10:  # account for when remainder seconds is less than 10
        count_sec = f"0{count_sec}"  # dynamic typing: changing a variable's data type by changing variable content

    # to get looping behavior, put window.after in a countdown function and have it call itself while passing a count #
    # change canvas text to current count -> needs to be in a variable first
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)  # takes the time in ms it should wait, before function call
    else:
        window.attributes('-topmost', 1)    # brings window in front of all other windows
        window.attributes('-topmost', 0)    # immediately disables the above - click window and minimize it after
        start_timer()   # start the next timer after the current timer counts to 0
        work_sessions_completed = math.floor(reps / 2)  # add a checkmark after every work timer is finished
        checkmarks = ""
        for check in range(0, work_sessions_completed):
            checkmarks += "✔"
        checkmark_label.config(text=checkmarks)

        if reps % 8 == 0:
            reps = 0


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=50, pady=30, bg=YELLOW)  # make the screen a little bigger, change background color

# upload a background image
# canvas widget: allows you to layer things, one on top of the other - like a background image with text on top
# roughly same size as tomato.png, with even numbers. changing canvas bg color to match window bg, removes canvas edges
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
# tkinter class that's a way to read through a file and get hold of a particular image
tomato_img = PhotoImage(file="tomato.png")
# x and y positions of the image in the canvas; half of x/y is at center, expects a PhotoImage
canvas.create_image(100, 112, image=tomato_img)  # can shifted over to the left/right to avoid being cut off by padding
timer_text = canvas.create_text(103, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold"))
canvas.grid(column=1, row=1)

# adding widgets
# Hint 1: fg is used to color the foreground, useful for text or symbols
# Hint 2: Copy-paste the checkmark symbol in a string
# Hint 3: use grid instead of pack
timer_label = Label(text="pomodoro timer", font=("Bahnschrift", 30), fg=GREEN, bg=YELLOW, pady=10, width=15, height=2)
timer_label.grid(column=1, row=0)

start_button = Button(text="start", command=start_timer, bg=GREEN, fg="white", relief=GROOVE, bd=0, padx=5, pady=5)
start_button.grid(column=0, row=2)

reset_button = Button(text="reset", command=reset_timer, bg=GREEN, fg="white", relief=GROOVE, bd=0, padx=5, pady=5)
reset_button.grid(column=2, row=2)

checkmark_label = Label(font=(FONT_NAME, 25), fg=GREEN, bg=YELLOW)  # no text; start out as empty
checkmark_label.grid(column=1, row=3)


window.mainloop()
