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

netLabel = tk.Label(text='Your net gain in money over the period of time is: ')

fileOpened = True
fileReader = main.csvReader


def putStatsToGui(rows):
    for row in rows:
        print(row[6])
    return


def displayStats(creader):
    header = next(creader)
    rows = []
    for row in creader:
        rows.append(row)
    putStatsToGui(header, rows, creader)


def openFilePicker():
    name = tkinter.filedialog.askopenfilename(title="Select CSV file", filetypes=(("CSV files", "*.csv"),))
    filename = codecs.open(name, encoding='latin-1')
    fileReader.file = filename
    print(type(filename))
    csvreader = csv.reader(filename, )
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
