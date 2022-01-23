import codecs
import tkinter as tk
import csv
import tkinter.filedialog
import main

window = tk.Tk()
window.winfo_toplevel().title("pyCSV Reader for RBC statements")
window.configure(background="#CBCBCB")

mainLabel = tk.Label(text='To view a .csv file, click the "Open CSV" button.', bg="#CBCBCB", fg="black")
mainLabel.pack()

net_label = None

fileOpened = False
fileReader = main.csvReader


def putStatsToGui(rows):
    global net_label
    temp = 0
    for row in rows:
        temp += float(row[6]) * 100
    temp = temp / 100
    if net_label is None:
        net_label = tk.Label(
            text='Your net gain over this period of time was $' + str(temp) + ". \n (A negative number "
                                                                              "means a net loss.)",
            bg="#CBCBCB", fg="black")
    else:
        net_label.config(
            text='Your net gain over this period of time was $' + str(temp) + ". \n (A negative number "
                                                                              "means a net loss.)",
            bg="#CBCBCB", fg="black")

    net_label.pack()
    csvButton.config(text="Open new CSV",
                     width=8,
                     height=2,
                     fg="black",
                     bg="#8A8989",
                     command=openFilePicker
                     )
    return


def displayStats(creader):
    header = next(creader)
    rows = []
    for row in creader:
        rows.append(row)
    putStatsToGui(rows)


def openFilePicker():
    global fileOpened
    name = tkinter.filedialog.askopenfilename(title="Select CSV file", filetypes=(("CSV files", "*.csv"),))
    filename = codecs.open(name, encoding='latin-1')
    fileReader.file = filename
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

csvButton.pack()

window.mainloop()
