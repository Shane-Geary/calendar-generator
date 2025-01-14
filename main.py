"""
Calendar Maker, by Al Sweigart al@inventwithpython.com
Create monthly calendars, saved to a text file and fit for printing.
View this code at https://nostarch.com/big-book-small-python-projects
Tags: short
"""

# Shane T Geary
# ITT: 111
# 12/14/2025
# Grand Canyon University | OpenAI

import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox

# Set up the constants:
DAYS = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
        'Friday', 'Saturday')
MONTHS = ('January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December')

# Define holiday names by month and day
HOLIDAYS = {
    1: {1: "New Year's Day", 25: "Lunar New Year"},
    2: {14: "Valentine's Day"},
    3: {17: "St. Patrick's Day"},
    4: {6: "Passover"},  # Example, date may vary
    4: {9: "Easter"},  # Example, date may vary
    5: {31: "Memorial Day"},
    7: {4: "4th of July"},
    9: {4: "Labor Day"},
    10: {31: "Halloween"},
    10: {6: "Yom Kippur"},  # Example, date may vary
    12: {25: "Christmas"},
    12: {12: "Hanukkah"},  # Example, date may vary
}

# Initialize the Tkinter root (hidden main window)
root = tk.Tk()
root.withdraw()  # Hide the main window

# Get the year from the user
while True:
    year_response = simpledialog.askstring("Year Input", "Enter the year for the calendar:")
    if year_response is None:  # User pressed Cancel
        exit()
    if year_response.isdecimal() and int(year_response) > 0:
        year = int(year_response)
        break
    messagebox.showerror("Invalid Input", "Please enter a valid numeric year, like 2023.")

# Get the month from the user
while True:
    month_response = simpledialog.askstring("Month Input", "Enter the calendar month to generate (1-12):")
    if month_response is None:  # User pressed Cancel
        exit()
    if month_response.isdecimal():
        month = int(month_response)
        if 1 <= month <= 12:
            break
    messagebox.showerror("Invalid Input", "Please enter a valid month (1 for January, 12 for December).")

# Modify the column width in these sections
def getCalendarFor(year, month):
    calText = ''  # calText will contain the string of our calendar.

    # Put the month and year at the top of the calendar:
    calText += (' ' * 50) + MONTHS[month - 1] + ' ' + str(year) + '\n'

    # Add the days of the week labels to the calendar:
    calText += '       Sun              Mon              Tue              Wed              Thu              Fri              Sat \n'  # Wider column headers

    # The horizontal line string that separates weeks (expanded columns):
    weekSeparator = ('+----------------' * 7) + '+\n'  # Wider separator

    # The blank rows have extra spaces between the | day separators:
    blankRow = ('|                ' * 7) + '|\n'  # Wider blank rows

    # Get the first date in the month. (The datetime module handles all
    # the complicated calendar stuff for us here.)
    currentDate = datetime.date(year, month, 1)

    # Roll back currentDate until it is Sunday. (weekday() returns 6
    # for Sunday, not 0.)
    while currentDate.weekday() != 6:
        currentDate -= datetime.timedelta(days=1)

    while True:  # Loop over each week in the month.
        calText += weekSeparator

        # dayNumberRow is the row with the day number labels:
        dayNumberRow = ''
        holidayRow = ''  # Row for the holiday names under the days
        
        for i in range(7):
            # Adjust the alignment of the day numbers
            dayNumberLabel = str(currentDate.day).rjust(2)  # Make sure it's right-aligned within 2 spaces
            dayNumberRow += '|' + dayNumberLabel.center(16)  # Centered day number with wider columns
            
            # Check for a holiday on this day
            holiday_name = HOLIDAYS.get(month, {}).get(currentDate.day, "")
            holidayRow += '|' + holiday_name.ljust(16)[:16]  # Adjusted width for holiday names

            currentDate += datetime.timedelta(days=1)  # Go to next day.

        dayNumberRow += '|\n'  # Add the vertical line after Saturday.
        holidayRow += '|\n'  # Add the vertical line for the holidays

        # Add the day number row and holiday row to the calendar text
        calText += dayNumberRow
        calText += holidayRow
        for i in range(3):  # (!) Try changing the 4 to a 5 or 10 for more padding
            calText += blankRow

        # Check if we're done with the month:
        if currentDate.month != month:
            break

    # Add the horizontal line at the very bottom of the calendar.
    calText += weekSeparator
    return calText

# Generate the calendar text (including month/year)
calText = getCalendarFor(year, month)

# Create a new Toplevel window for the calendar display
calendar_window = tk.Toplevel(root)
calendar_window.title("Generated Calendar")

# Set the size of the window dynamically based on the length of the calendar content
window_width = max(650, len(calText.splitlines()[0]) * 8)  # Adjust width based on first line length
calendar_window.geometry(f"{window_width}x600")  # Set window width and height

# Add a label with the calendar text inside the new window
calendar_label = tk.Label(calendar_window, text=calText, font=("Courier", 10), padx=10, pady=10)
calendar_label.pack()

# Save the calendar to a text file (no change to the text here)
calendarFilename = f'calendar_{year}_{month}.txt'
with open(calendarFilename, 'w') as fileObj:
    fileObj.write(calText)  # No centering needed for the file

messagebox.showinfo("Success", f"Calendar saved to {calendarFilename}")

root.mainloop()  # Start the Tkinter event loop
