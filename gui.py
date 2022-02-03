import codecs
import tkinter as tk
import csv
import tkinter.filedialog


# This window represents the main one, from which one can load in an RBC bank statement and analyze spending data
window = tk.Tk()
window.winfo_toplevel().title("pyCSV Reader for RBC statements")
window.configure(background="#CBCBCB")

mainLabel = tk.Label(text='To view a .csv file, click the "Open CSV" button.', bg="#CBCBCB", fg="black")
mainLabel.pack()

net_label = None
rows = []

fileOpened = False


# Reacts to the command the user has typed into the "sort by" field
def reactToEntry():
    global net_label
    text = commandEntry.get()
    match text:
        case "gain":  # only values not starting with '-' are counted

            temp = 0
            count = 0
            for row in rows:
                if float(row[6]) * 100 > 0:
                    temp += float(row[6]) * 100
                    count += 1
            temp = temp / 100
            if net_label is None:
                net_label = tk.Label(
                    text='You made ' + str(count) + ' gains over this period of time.\nThese total to $' + str(
                        temp) + ".",
                    bg="#CBCBCB", fg="black")
            else:
                net_label.config(
                    text='You made ' + str(count) + ' gains over this period of time.\nThese total to $' + str(
                        temp) + ".",
                    bg="#CBCBCB", fg="black")

        case "loss":  # only values starting with '-' are counted

            temp = 0
            count = 0
            for row in rows:
                if float(row[6]) * 100 < 0:
                    temp += float(row[6]) * 100
                    count += 1
            temp = temp / 100
            if net_label is None:
                net_label = tk.Label(
                    text='You made ' + str(count) + ' losses over this period of time.\nThese total to $' + str(
                        temp) + ".",
                    bg="#CBCBCB", fg="black")
            else:
                net_label.config(
                    text='You made ' + str(count) + ' losses over this period of time.\nThese total to $' + str(
                        temp) + ".",
                    bg="#CBCBCB", fg="black")

        case "none":  # go back to not sorting by anything
            temp = 0
            count = 0
            for row in rows:
                temp += float(row[6]) * 100
                count += 1
            temp = temp / 100
            if net_label is None:
                net_label = tk.Label(
                    text='You made ' + str(
                        count) + ' transactions over this period of time.\nYour net gain/loss was $' + str(
                        temp) + ". \n (A negative number "
                                "means a net loss.)",
                    bg="#CBCBCB", fg="black")
            else:
                net_label.config(
                    text='You made ' + str(
                        count) + ' transactions over this period of time.\nYour net gain/loss was $' + str(
                        temp) + ". \n (A negative number "
                                "means a net loss.)",
                    bg="#CBCBCB", fg="black")

        case "place":
            openDropdownPicker(text)
        case "date":
            openDropdownPicker(text)


# changes label on main window after a specific place/date is chosen
def putNewStatsToGui(cat, strg):
    global net_label
    match cat:
        case "place":  # only transactions from place with name matching strg is counted
            temp = 0
            count = 0
            for row in rows:
                if row[5] == strg:
                    temp += float(row[6]) * 100
                    count += 1
            temp = temp / 100
            if net_label is None:
                net_label = tk.Label(
                    text='You made ' + str(
                        count) + ' transactions over this period of time, at this place.\nYour net gain/loss was '
                                 '$' + str(
                        temp) + ". \n (A negative number "
                                "means a net loss.)",
                    bg="#CBCBCB", fg="black")
            else:
                net_label.config(
                    text='You made ' + str(
                        count) + ' transactions over this period of time, at this place.\nYour net gain/loss was '
                                 '$' + str(
                        temp) + ". \n (A negative number "
                                "means a net loss.)",
                    bg="#CBCBCB", fg="black")
        case "date":  # only transactions with date matching strg are counted
            temp = 0
            count = 0
            for row in rows:
                if row[2] == strg:
                    temp += float(row[6]) * 100
                    count += 1
            temp = temp / 100
            if net_label is None:
                net_label = tk.Label(
                    text='You made ' + str(
                        count) + ' transactions on this date.\nYour net gain/loss was $' + str(
                        temp) + ". \n (A negative number "
                                "       means a net loss.)",
                    bg="#CBCBCB", fg="black")
            else:
                net_label.config(
                    text='You made ' + str(
                        count) + ' transactions on this date.\nYour net gain/loss was $' + str(
                        temp) + ". \n (A negative number "
                                "means a net loss.)",
                    bg="#CBCBCB", fg="black")


# opens the window with a dropdown menu from which the user can sort by specific date or place
def openDropdownPicker(cat):
    new_window = tk.Toplevel(window)  # this represents the new window created for this purpose
    new_window.title = "Select category"
    new_window.configure(background="#CBCBCB")
    choices = []
    # fill dropdown picker with dates or places, depeding on cat parameter
    match cat:
        case "place":
            for row in rows:
                if row[5] not in choices and row[5] != "":
                    choices.append(row[5])
        case "date":
            for row in rows:
                if row[2] not in choices and row[2] != "":
                    choices.append(row[2])

    variable = tk.StringVar(new_window, "Select...")
    # this button updates labels on main gui
    chosen_button = tk.Button(
        new_window,
        text="Go",
        width=5,
        height=1,
        fg="black",
        bg="#CBCBCB",
        command=lambda: putNewStatsToGui(cat, variable.get())

    )
    # this button closes the secondary window
    back_button = tk.Button(
        new_window,
        text="Back",
        width=5,
        height=1,
        fg="black",
        bg="#CBCBCB",
        command=lambda: new_window.destroy()
    )

    dropdown = tk.OptionMenu(new_window, variable, *choices)
    dropdown.pack()

    chosen_button.pack()
    back_button.pack()


# once a .csv is loaded in, label on main gui is updated with default sort settings ("none").
def putStatsToGui():
    global net_label
    temp = 0
    count = 0
    for row in rows:
        temp += float(row[6]) * 100
        count += 1
    temp = temp / 100
    if net_label is None:
        net_label = tk.Label(
            text='You made ' + str(count) + ' transactions over this period of time.\nYour net gain/loss was $' + str(
                temp) + ". \n (A negative number "
                        "means a net loss.)",
            bg="#CBCBCB", fg="black")
    else:
        net_label.config(
            text='You made ' + str(count) + ' transactions over this period of time.\nYour net gain/loss was $' + str(
                temp) + ". \n (A negative number "
                        "means a net loss.)",
            bg="#CBCBCB", fg="black")

    net_label.pack()
    commandEntry.pack()
    sortButton.pack()
    tipLabel.pack()
    csvButton.config(text="Open new CSV",
                     width=8,
                     height=1,
                     fg="black",
                     bg="#CBCBCB",
                     command=openFilePicker
                     )
    return


# creates 'rows' array that can be analyzed further
def displayStats(creader):
    global rows
    next(creader)
    rows = []
    for row in creader:
        rows.append(row)
    putStatsToGui()


# opens the file picker screen upon clicking "open csv" button
def openFilePicker():
    global fileOpened
    name = tkinter.filedialog.askopenfilename(title="Select CSV file", filetypes=(("CSV files", "*.csv"),))
    filename = codecs.open(name, encoding='latin-1')
    csvreader = csv.reader(filename, )
    fileOpened = True
    displayStats(csvreader)
    return


# this button opens file picker screen
csvButton = tk.Button(
    text="Open CSV",
    width=5,
    height=1,
    fg="black",
    bg="#CBCBCB",
    command=openFilePicker
)

commandEntry = tk.Entry()
commandEntry.insert("end", "<insert command here>")

# this button allows user to sort by certain categories
sortButton = tk.Button(
    text="Sort by...",
    width=5,
    height=1,
    fg="black",
    bg="#CBCBCB",
    command=reactToEntry
)

tipLabel = tk.Label(text='(Sort by "place", "date", "gain", "loss", or "none".)', bg="#CBCBCB", fg="black")

csvButton.pack()

window.mainloop()
