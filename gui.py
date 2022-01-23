import codecs
import tkinter as tk
import csv
import tkinter.filedialog
import tkinter.ttk as ttk

window = tk.Tk()
window.winfo_toplevel().title("pyCSV Reader for RBC statements")
window.configure(background="#CBCBCB")

mainLabel = tk.Label(text='To view a .csv file, click the "Open CSV" button.', bg="#CBCBCB", fg="black")
mainLabel.pack()

net_label = None
rows = []

fileOpened = False


def reactToEntry():
    global net_label
    text = commandEntry.get()
    match text:
        case "gain":

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

        case "loss":

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

        case "none":
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
        case "type":
            openDropdownPicker(text)


def openDropdownPicker(cat):
    new_window = tk.Toplevel(window)
    new_window.title = "Select category"
    choices = []
    match cat:
        case "place":
            for row in rows:
                choices.append(row[5])
        case "date":
            for row in rows:
                choices.append(row[2])
        case "type":
            for row in rows:
                choices.append(row[4])

    chosen_button = tk.Button(
        text="Go",
        width=5,
        height=2,
        fg="black",
        bg="#8A8989",
    )


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
                     height=2,
                     fg="black",
                     bg="#8A8989",
                     command=openFilePicker
                     )
    return


def displayStats(creader):
    global rows
    header = next(creader)
    rows = []
    for row in creader:
        rows.append(row)
    putStatsToGui()


def openFilePicker():
    global fileOpened
    name = tkinter.filedialog.askopenfilename(title="Select CSV file", filetypes=(("CSV files", "*.csv"),))
    filename = codecs.open(name, encoding='latin-1')
    csvreader = csv.reader(filename, )
    fileOpened = True
    displayStats(csvreader)
    return


csvButton = tk.Button(
    text="Open CSV",
    width=5,
    height=2,
    fg="black",
    bg="#8A8989",
    command=openFilePicker
)

commandEntry = tk.Entry()
commandEntry.insert("end", "<insert command here>")

sortButton = tk.Button(
    text="Sort by...",
    width=5,
    height=2,
    fg="black",
    bg="#8A8989",
    command=reactToEntry
)

tipLabel = tk.Label(text='(Sort by "place", "date", "type", "gain", "loss", or "none".)', bg="#CBCBCB", fg="black")

csvButton.pack()

window.mainloop()
