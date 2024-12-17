from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os

root = Tk()
root.wm_title("Convert Invalid JSON file to Valid JSON file")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w - 20, h - 100))

fontLabel = ("Calibri", 20)
fontButton = ("Calibri", 15, "bold")

def btnConvertJsonClick():
    filePath = filedialog.askopenfilename(
        initialdir="/",
        title="Document Tracker : Browse Invalid JSON file",
        filetypes=(("JSON files", "*.json"), ("JSON files", "*.json")),
    )

    if len(filePath) > 0:
        btnConvertJson["state"] = "disabled"
        btnConvertJson["text"] = "Please wait..."
        btnConvertJson.update()

        fr = open(filePath, "r")
        Lines = fr.readlines()

        strDocuments = "["
        count = 1
        for line in Lines:
            if count != 1:
                strDocuments += ","
            strDocuments += line.strip()
            count += 1
        strDocuments += "]"
         
        fr.close()

        fwName = os.path.basename(filePath)
        fw = open(fwName, "w")
        fw.write(strDocuments)
        fw.close()

        strSuccess = str(count) + " records converted successfully."
        btnConvertJson["text"] = strSuccess
        messagebox.showinfo("Document Tracker", strSuccess)

        btnConvertJson["state"] = "normal"
        btnConvertJson["text"] = "Convert Json"

class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

btnConvertJson = Button(root, text="Convert Json", font=fontButton, command=btnConvertJsonClick)
btnConvertJson.grid(row=0, column=0)

app = Window(root)
root.mainloop()



