from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageTk, Image
from io import BytesIO
from graphviz import Digraph

root = Tk()
root.wm_title("Data Analysis of a Document Tracker")
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w - 20, h - 100))

fontLabel = ("Calibri", 20)
fontButton = ("Calibri", 15, "bold")

dfCountriesContinents = pd.DataFrame()
dfDocuments = pd.DataFrame()


def clearFrame():
    for widget in frame.winfo_children():
        widget.destroy()

    frame.grid_forget()


def resizeFrame():
    col_count, row_count = frame.grid_size()

    for col in range(col_count):
        frame.grid_columnconfigure(col, minsize=50)

    for row in range(row_count):
        frame.grid_rowconfigure(row, minsize=50)


def loadCountriesContinents():
    global dfCountriesContinents

    f = open("CountriesContinents.json", "r")

    data = json.load(f)

    dfCountriesContinents = pd.DataFrame(data)

    print(dfCountriesContinents)


def btnLoadJsonClick():
    global dfDocuments

    filePath = filedialog.askopenfilename(
        initialdir="/",
        title="Document Tracker : Browse JSON file",
        filetypes=(("JSON files", "*.json"), ("JSON files", "*.json")),
    )

    if len(filePath) > 0:
        btnLoadJson["state"] = "disabled"
        btnLoadJson["text"] = "Please wait..."
        btnLoadJson.update()

        f = open(filePath, "r")
        data = json.load(f)
        dfDocuments = pd.DataFrame(data)

        strSuccess = str(len(dfDocuments)) + " records loaded successfully."
        btnLoadJson["text"] = strSuccess
        messagebox.showinfo("Document Tracker", strSuccess)

        f.close()

        btnLoadJson["state"] = "normal"
        btnLoadJson["text"] = "Load Json"


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master

        menu = Menu(self.master)
        self.master.config(menu=menu)

        menu1 = Menu(menu)
        menu1.add_command(
            label="Country Report", font=fontLabel, command=self.loadCountryReportPage
        )
        menu1.add_command(
            label="Browser Report", font=fontLabel, command=self.loadBrowserReportPage
        )
        menu1.add_command(
            label="Readers Report", font=fontLabel, command=self.loadReaderReportPage
        )
        menu.add_cascade(label="Reports", menu=menu1)

        menu2 = Menu(menu)
        menu2.add_command(
            label="Also likes functionality",
            font=fontLabel,
            command=self.loadAlsoLikes1Page,
        )
        menu2.add_command(
            label="Also likes graph", font=fontLabel, command=self.loadAlsoLikes2Page
        )
        menu.add_cascade(label="Also likes", menu=menu2)

        loadCountriesContinents()

    def loadCountryReportPage(self):
        clearFrame()
        frame.configure(text="Document Tracker : Country Report")

        lblDocumentUUID = Label(frame, text="Document UUID: ", font=fontLabel)
        lblDocumentUUID.grid(row=0, column=0)

        self.txtDocumentUUID = Entry(frame, font=fontLabel)
        self.txtDocumentUUID.grid(row=0, column=1)

        btnSearchCountryReport = Button(
            frame,
            text="Search by Countries",
            font=fontButton,
            command=self.btnSearchCountryReportClick,
        )
        btnSearchCountryReport.grid(row=1, column=0)

        btnSearchContinentReport = Button(
            frame,
            text="Search by Continents",
            font=fontButton,
            command=self.btnSearchContinentReportClick,
        )
        btnSearchContinentReport.grid(row=1, column=1)

        frame.grid(row=2, column=0)

        resizeFrame()

    def btnSearchCountryReportClick(self):
        documentUUID = self.txtDocumentUUID.get()
        Func2a(documentUUID)

    def btnSearchContinentReportClick(self):
        documentUUID = self.txtDocumentUUID.get()
        Func2b(documentUUID)

    def loadBrowserReportPage(self):
        clearFrame()
        frame.configure(text="Document Tracker : Browser Report")

        btnViewBrowserReport1 = Button(
            frame,
            text="View Browser Report 1",
            font=fontButton,
            command=self.btnViewBrowserReport1Click,
        )
        btnViewBrowserReport1.grid(row=0, column=0)

        btnViewBrowserReport2 = Button(
            frame,
            text="View Browser Report 2",
            font=fontButton,
            command=self.btnViewBrowserReport2Click,
        )
        btnViewBrowserReport2.grid(row=0, column=1)

        frame.grid(row=1, column=0)

        resizeFrame()

    def btnViewBrowserReport1Click(self):
        Func3a()

    def btnViewBrowserReport2Click(self):
        Func3b()

    def loadReaderReportPage(self):
        clearFrame()
        frame.configure(text="Document Tracker : Top 10 Reader Report")

        btnViewReaderReport = Button(
            frame,
            text="View Reader Report",
            font=fontButton,
            command=self.btnViewReaderReportClick,
        )
        btnViewReaderReport.grid(row=0, column=0)

        frame.grid(row=1, column=0)

        resizeFrame()

    def btnViewReaderReportClick(self):
        Func4()

    def loadPlot(self):
        img_data = BytesIO()
        plt.savefig(img_data)

        load = Image.open(img_data)
        render = ImageTk.PhotoImage(load)
        img = Label(frame, image=render)
        img.image = render
        img.grid(row=1, column=0, columnspan=2)

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

        resizeFrame()

    def btnSearchAlsoLikes1Click(self):
        documentUUID = self.txtDocumentUUID.get()
        visitorUUID = self.txtVisitorUUID.get()

        Func5d(documentUUID, visitorUUID)

    def loadAlsoLikes2Page(self):
        clearFrame()

        frame.configure(text="Document Tracker : Also likes graph")

        lblDocumentUUID = Label(frame, text="Document UUID: ", font=fontLabel)
        lblDocumentUUID.grid(row=0, column=0)

        self.txtDocumentUUID = Entry(frame, font=fontLabel)
        self.txtDocumentUUID.grid(row=0, column=1)

        lblVisitorUUID = Label(frame, text="Visitor UUID: ", font=fontLabel)
        lblVisitorUUID.grid(row=1, column=0)

        self.txtVisitorUUID = Entry(frame, font=fontLabel)
        self.txtVisitorUUID.grid(row=1, column=1)

        btnSearchAlsoLikes2 = Button(
            frame,
            text="Show Also likes graph",
            font=fontButton,
            command=self.btnSearchAlsoLikes2Click,
        )
        btnSearchAlsoLikes2.grid(row=2, column=0)

        frame.grid(row=1, column=0)

        resizeFrame()

    def btnSearchAlsoLikes2Click(self):
        documentUUID = self.txtDocumentUUID.get()
        visitorUUID = self.txtVisitorUUID.get()

        Func6(documentUUID, visitorUUID)


def Func2a(documentUUID):
    plt.clf()

    global dfDocuments

    # Filter by Document UUID
    filter = dfDocuments["env_doc_id"] == documentUUID
    dfSearch = dfDocuments.where(filter)

    # Group By Country then Count By Viewers
    df = (
        dfSearch.groupby(["visitor_country"], dropna=True)["visitor_uuid"]
        .count()
        .reset_index(name="count")
    )

    lstCountryCounts = []
    lstCountries = []
    lstCounts = []
    for c in df.value_counts().axes[0]:
        lstCountryCounts.append(c)
        lstCountries.append(c[0])
        lstCounts.append(c[1])

    lstCounts.sort()

    df["count"].hist(by=df["visitor_country"])
    plt.show()

    # plt.hist(lstCountries, bins=lstCounts)

    # plt.title("Views by Country", fontweight="bold")
    # plt.xlabel("Countries")
    # plt.ylabel("Number of views")
    # plt.xticks(lstCountries)
    ## plt.yticks(counts)
    # plt.legend(prop={"size": 10}, loc="upper right")
    # plt.show()


def Func2b(documentUUID):
    plt.clf()

    global dfDocuments
    global dfCountriesContinents

    # Filter by Document UUID
    filter = dfDocuments["env_doc_id"] == documentUUID
    dfSearch = dfDocuments.where(filter)

    # Join with Countries Continents
    dfResult = pd.merge(
        dfSearch,
        dfCountriesContinents,
        how="inner",
        on=["visitor_country"],
    )

    # Group By Continent then Count By Viewers
    df = (
        dfResult.groupby(["continent"], dropna=True)["visitor_uuid"]
        .count()
        .reset_index(name="count")
    )

    lstlstContinentCounts = []
    lstContinents = []
    lstCounts = []
    for c in df.value_counts().axes[0]:
        lstlstContinentCounts.append(c)
        lstContinents.append(c[0])
        lstCounts.append(c[1])

    lstCounts.sort()

    df["count"].hist(by=df["continent"])
    plt.show()

    # plt.hist(lstContinents, bins=lstCounts)

    # plt.title("Views by Continents", fontweight="bold")
    # plt.xlabel("Continents")
    # plt.ylabel("Number of views")
    # plt.xticks(lstContinents)
    ## plt.yticks(counts)
    # plt.legend(prop={"size": 10}, loc="upper right")
    # plt.show()


def Func3a():
    plt.clf()

    global dfDocuments

    # Group By Useragent then Count By Viewers
    df = (
        dfDocuments.groupby(["visitor_useragent"], dropna=True)[
            "visitor_useragent"
        ].count()
        # .reset_index(name="count")
    )

    useragents = dfDocuments.visitor_useragent.unique()
    counts = df.value_counts().sort_values()

    browsers = []
    for ug in useragents:
        b = ug.split(")")[0].strip()
        if b not in browsers:
            browsers.append(b)

    plt.hist(browsers, bins=counts, edgecolor="yellow", color="green")

    plt.title("Views by Browser", fontweight="bold")
    plt.xlabel("Browsers")
    plt.ylabel("Number of views")
    # plt.xticks(useragents)
    # plt.yticks(counts)
    plt.legend(prop={"size": 10}, loc="upper right")
    plt.show()


def getBrowserName(row):
    return row.visitor_useragent.to_string().split("/")[0].strip()


def Func3b():
    plt.clf()

    global dfDocuments

    # Group By Useragent then Count By Viewers
    df = (
        dfDocuments.groupby(["visitor_useragent"], dropna=True)
        # .apply(getBrowserName)
        ["visitor_useragent"].count()
        # .reset_index(name="count")
    )

    useragents = dfDocuments.visitor_useragent.unique()
    counts = df.value_counts().sort_values()

    browsers = []
    for ug in useragents:
        b = ug.split("/")[0].strip()
        if b not in browsers:
            browsers.append(b)

    #lstCounts = []
    #for c in df.value_counts().axes[0]:
    #    lstCounts.append(c[1])

    #lstCounts.sort()

    plt.hist(browsers, bins=counts, edgecolor="yellow", color="green")

    plt.title("Views by Browser", fontweight="bold")
    plt.xlabel("Browsers")
    plt.ylabel("Number of views")
    # plt.xticks(useragents)
    # plt.yticks(counts)
    plt.legend(prop={"size": 10}, loc="upper right")
    plt.show()


def Func4():
    global dfDocuments

    filter = dfDocuments["event_type"] == "pagereadtime"
    dfSearch = dfDocuments.where(filter)
    dfResult = dfSearch.groupby(["visitor_uuid"])["event_readtime"].sum()

    print(dfResult.sort_values(ascending=False).head(10))


def Func5d(documentUUID, visitorUUID):
    al = AlsoLikes(documentUUID, visitorUUID)

    global dfDocuments

    dfResult = dfDocuments[dfDocuments["env_doc_id"].isin(al.documentUUIDs)]

    df1 = dfResult.groupby(["env_doc_id"])["visitor_uuid"].count()

    print("\n")
    print(df1.sort_values(ascending=False).head(10))
    print("\n")


def Func6(documentUUID, visitorUUID):
    global dfDocuments

    al = AlsoLikes(documentUUID, visitorUUID)

    dot = Digraph(comment="Also likes graph")

    for d in al.documentUUIDs:
        if isinstance(d, str):
            strd = str(d[-4:])
            dot.node(strd, strd)

    for v in al.visitorUUIDs:
        strv = str(v[-4:])
        dot.node(strv, strv)

        filter = dfDocuments["visitor_uuid"] == v
        dfDocs = dfDocuments.where(filter)

        visitorDocUUIDs = dfDocs.env_doc_id.unique()

        for d in visitorDocUUIDs:
            if isinstance(d, str):
                strd = str(d[-4:])
                dot.edge(strv, strd)

    print(dot.source)

    dot.render("AlsoLikesGraph.gv.pdf", view=True)


class AlsoLikes:
    def __init__(self, documentUUID, visitorUUID):
        self.documentUUIDs = []
        self.visitorUUIDs = []

        vUUIDs = self.getVisitorUUIDs(documentUUID)
        for v in vUUIDs:
            if isinstance(v, str):
                self.visitorUUIDs.append(v)

        print(self.visitorUUIDs)
        print("\n")

        if len(visitorUUID) > 0:
            dUUIDs = self.getDocumentUUIDs(visitorUUID)
            for d in dUUIDs:
                if isinstance(d, str):
                    self.documentUUIDs.append(d)

        for v in self.visitorUUIDs:
            if isinstance(v, str):
                dUUIDs = self.getDocumentUUIDs(v)
                for d in dUUIDs:
                    if isinstance(d, str):
                        self.documentUUIDs.append(d)

        print(self.documentUUIDs)
        print("\n")

    def getVisitorUUIDs(self, documentUUID):
        global dfDocuments

        filter = dfDocuments["env_doc_id"] == documentUUID
        dfResult = dfDocuments.where(filter)

        return dfResult.visitor_uuid.unique()

    def getDocumentUUIDs(self, visitorUUID):
        global dfDocuments

        filter = dfDocuments["visitor_uuid"] == visitorUUID
        dfResult = dfDocuments.where(filter)

        return dfResult.env_doc_id.unique()


btnLoadJson = Button(root, text="Load Json", font=fontButton, command=btnLoadJsonClick)
btnLoadJson.grid(row=0, column=0)

frame = LabelFrame(root, padx=w - 1000, pady=h - 750)
frame.grid(row=1, column=0)


app = Window(root)
root.mainloop()
