from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd

root = Tk()
root.wm_title("Data Analysis of a Document Tracker")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w - 20, h - 100))

fontLabel = ("Calibri", 20)
fontButton = ("Calibri", 15, "bold")

dfDocuments = pd.DataFrame()

def clearFrame():
    for widget in frame.winfo_children():
        widget.destroy()

    frame.grid_forget()

def btnLoadJsonClick():
    filePath = filedialog.askopenfilename(
        initialdir="/",
        title="Document Tracker : Browse JSON file",
        filetypes=(("JSON files", "*.json"), ("JSON files", "*.json")),
    )

    if len(filePath) > 0:
        f = open(filePath, "r")
        Lines = f.readlines()

        strDocuments = "["
        count = 1
        for line in Lines:
            if count != 1:
                strDocuments += ","
            strDocuments += line.strip()
            count += 1
        strDocuments += "]"

        root.dfDocuments = pd.DataFrame(eval(strDocuments))

        messagebox.showinfo(
            "Document Tracker",
            str(len(root.dfDocuments)) + " records loaded successfully.",
        )

        f.close()


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        menu = Menu(self.master)
        self.master.config(menu=menu)

        menu1 = Menu(menu)
        menu1.add_command(label="Country Report", font=fontLabel)
        menu1.add_command(label="Browser Report", font=fontLabel)
        menu1.add_command(label="Readers Report", font=fontLabel)
        menu.add_cascade(label="Reports", menu=menu1)

        menu2 = Menu(menu)
        menu2.add_command(label="Also likes functionality", font=fontLabel, command=self.loadAlsoLikes1Page)
        menu2.add_command(label="Also likes graph", font=fontLabel)
        menu.add_cascade(label="Also likes", menu=menu2)

    def loadAlsoLikes1Page(self):
        clearFrame()
        frame.configure(text="Document Tracker : Also likes functionality")

        lblDocumentUUID = Label(frame, text="Document UUID: ", font=fontLabel)
        lblDocumentUUID.grid(row=0, column=0)

        self.txtDocumentUUID = Entry(frame, font=fontLabel)
        self.txtDocumentUUID.grid(row=0, column=1)

        lblVisitorUUID = Label(frame, text="Visitor UUID: ", font=fontLabel)
        lblVisitorUUID.grid(row=1, column=0)

        self.txtVisitorUUID = Entry(frame, font=fontLabel)
        self.txtVisitorUUID.grid(row=1, column=1)

        btnSearchAlsoLikes1 = Button(
            frame,
            text="Search",
            font=fontButton,
            command=self.btnSearchAlsoLikes1Click,
        )
        btnSearchAlsoLikes1.grid(row=2, column=0, columnspan=2)

        frame.grid(row=1, column=0)

    def btnSearchAlsoLikes1Click(self):
        documentUUID = self.txtDocumentUUID.get()
        visitorUUID = self.txtVisitorUUID.get()

        visitorUUIDs = self.getVisitorUUIDs(documentUUID)
        print(visitorUUIDs)
        print("\n")

        documentUUIDs = self.getDocumentUUIDs(visitorUUID)
        print(documentUUIDs)
        print("\n")

        self.showTop10Documents(documentUUID, visitorUUID)


    def getVisitorUUIDs(self, documentUUID):
        filter = root.dfDocuments["visitor_source"] == documentUUID
        dfResult = root.dfDocuments.where(filter)
        
        #print(dfResult.head().to_html() + "\n")

        return dfResult.visitor_uuid

    def getDocumentUUIDs(self, visitorUUID):
        filter = root.dfDocuments["visitor_uuid"] == visitorUUID
        dfResult = root.dfDocuments.where(filter)
        
        #print(dfResult.head().to_html() + "\n")

        return dfResult.ts

    def showTop10Documents(self, documentUUID, visitorUUID):
        #filter = root.dfDocuments["visitor_uuid"] == visitorUUID
        #dfResult = root.dfDocuments.where(filter)
        
        df1 = root.dfDocuments.groupby(["visitor_source"])[
            "visitor_uuid"
        ].count()

        print("\n")
        print(df1.sort_values(ascending=False).head(10))
        print("\n")

btnLoadJson = Button(root, text="Load Json", font=fontButton, command=btnLoadJsonClick)
btnLoadJson.grid(row=0, column=0)

frame = LabelFrame(root, padx=w - 1000, pady=h - 750)
frame.grid(row=1, column=0)

app = Window(root)
root.mainloop()
