import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from graphviz import Digraph


dfCountriesContinents = pd.DataFrame()
dfDocuments = pd.DataFrame()


def startProcess():
    n = len(sys.argv)
    print("Total arguments passed:", n)
    print("\nArguments passed:", end=" ")
    for i in range(1, n):
        print(sys.argv[i], end=" ")

    if n == 9:
        documentUUID = ""
        visitorUUID = ""
        taskID = ""
        fileName = ""

        for i in range(1, n):
            if i % 2 != 0 and sys.argv[i] == "-d":
                documentUUID = sys.argv[i + 1]
            elif i % 2 != 0 and sys.argv[i] == "-u":
                visitorUUID = sys.argv[i + 1]
            elif i % 2 != 0 and sys.argv[i] == "-t":
                taskID = sys.argv[i + 1]
            elif i % 2 != 0 and sys.argv[i] == "-f":
                fileName = sys.argv[i + 1]

        print("Document UUID: " + documentUUID + "\n")
        print("Visitor UUID: " + visitorUUID + "\n")
        print("Task ID: " + taskID + "\n")
        print("File Name: " + fileName + "\n")

        if taskID == "2a" or taskID == "2A":
            loadJson(fileName)
            Func2a(documentUUID)
        elif taskID == "2b" or taskID == "2B":
            loadCountriesContinents()
            loadJson(fileName)
            Func2b(documentUUID)
        elif taskID == "3a" or taskID == "3A":
            loadJson(fileName)
            Func3a(documentUUID)
        elif taskID == "3b" or taskID == "3B":
            loadJson(fileName)
            Func3b()
        elif taskID == "4":
            loadJson(fileName)
            Func4()
        elif taskID == "5d" or taskID == "5D":
            loadJson(fileName)
            Func5d(documentUUID, visitorUUID)
        elif taskID == "6":
            loadJson(fileName)
            Func6(documentUUID, visitorUUID)
        elif taskID == "7":
            Func7()


def loadCountriesContinents():
    global dfCountriesContinents

    f = open("CountriesContinents.json", "r")
    data = json.load(f)
    dfCountriesContinents = pd.DataFrame(data)

    print(dfCountriesContinents)


def loadJson(fileName):
    if len(fileName) > 0:
        global dfDocuments

        f = open(fileName, "r")
        data = json.load(f)
        dfDocuments = pd.DataFrame(data)

        print(str(len(dfDocuments)) + " records loaded successfully.")

        f.close()


def Func2a(documentUUID):
    plt.clf()

    global dfDocuments

    # Filter by Document UUID
    filter = dfDocuments["env_doc_id"] == documentUUID
    dfSearch = dfDocuments.where(filter)

    # Group By Country then Count By Viewers
    df1 = dfSearch.groupby(["visitor_country"])["visitor_uuid"].count()

    countries = dfSearch.visitor_country.unique()
    counts = df1.value_counts().sort_values()

    lstCountries = []
    for c in countries:
        if isinstance(c, str):
            lstCountries.append(c)

    w = 200
    plt.hist(
        lstCountries,
        bins=np.arange(min(counts), max(counts) + w, w),
        edgecolor="yellow",
        color="green",
    )

    # plt.hist(lstCountries, bins=counts, edgecolor="yellow", color="green")

    plt.title("Views by Country", fontweight="bold")
    plt.xlabel("Countries")
    plt.ylabel("Number of views")
    # plt.xticks(countries)
    # plt.yticks(counts)
    plt.legend(prop={"size": 10}, loc="upper right")
    plt.show()


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
    df1 = dfResult.groupby(["continent"])["visitor_uuid"].count()

    continents = dfResult.continent.unique()
    counts = df1.value_counts().sort_values()

    lstContinents = []
    for c in continents:
        if isinstance(c, str):
            lstContinents.append(c)

    plt.hist(lstContinents, bins=counts, edgecolor="yellow", color="green")

    plt.title("Views by Continents", fontweight="bold")
    plt.xlabel("Continents")
    plt.ylabel("Number of views")
    # plt.xticks(continents)
    # plt.yticks(counts)
    plt.legend(prop={"size": 10}, loc="upper right")
    plt.show()


def Func3a():
    plt.clf()

    global dfDocuments

    df1 = dfDocuments.groupby(["visitor_useragent"])["visitor_useragent"].count()

    useragents = dfDocuments.visitor_useragent.unique()
    counts = df1.value_counts().sort_values()

    plt.hist(useragents, bins=counts, edgecolor="yellow", color="green")

    plt.title("Views by Browser", fontweight="bold")
    plt.xlabel("Browsers")
    plt.ylabel("Number of views")
    # plt.xticks(useragents)
    # plt.yticks(counts)
    plt.legend(prop={"size": 10}, loc="upper right")
    plt.show()


def Func3b():
    plt.clf()

    global dfDocuments

    df1 = dfDocuments.groupby(["visitor_useragent"])["visitor_useragent"].count()

    useragents = dfDocuments.visitor_useragent.unique()
    counts = df1.value_counts().sort_values()

    browsers = []
    for ug in useragents:
        b = ug.split("/")[0].strip()
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


def Func4():
    global dfDocuments

    filter = dfDocuments["event_type"] == "pagereadtime"
    dfSearch = dfDocuments.where(filter)
    dfResult = dfSearch.groupby(["visitor_uuid"])["event_readtime"].sum()

    print(dfResult.sort_values(ascending=False).head(10))


def Func5d(documentUUID, visitorUUID):
    documentUUIDs = []
    visitorUUIDs = []

    vUUIDs = getVisitorUUIDs(documentUUID)
    for v in vUUIDs:
        if isinstance(v, str):
            visitorUUIDs.append(v)

    print(visitorUUIDs)
    print("\n")

    if len(visitorUUID) > 0:
        dUUIDs = getDocumentUUIDs(visitorUUID)
        for d in dUUIDs:
            if isinstance(d, str):
                documentUUIDs.append(d)

    for v in visitorUUIDs:
        if isinstance(v, str):
            dUUIDs = getDocumentUUIDs(v)
            for d in dUUIDs:
                if isinstance(d, str):
                    documentUUIDs.append(d)

    print(documentUUIDs)
    print("\n")

    showAlsoLikes1Top10Documents(documentUUIDs)


def getVisitorUUIDs(documentUUID):
    global dfDocuments

    filter = dfDocuments["env_doc_id"] == documentUUID
    dfResult = dfDocuments.where(filter)

    return dfResult.visitor_uuid.unique()


def getDocumentUUIDs(visitorUUID):
    global dfDocuments

    filter = dfDocuments["visitor_uuid"] == visitorUUID
    dfResult = dfDocuments.where(filter)

    return dfResult.env_doc_id.unique()


def showAlsoLikes1Top10Documents(documentUUIDs):
    global dfDocuments

    dfResult = dfDocuments[dfDocuments["env_doc_id"].isin(documentUUIDs)]

    df1 = dfResult.groupby(["env_doc_id"])["visitor_uuid"].count()

    print("\n")
    print(df1.sort_values(ascending=False).head(10))
    print("\n")


def Func6(documentUUID, visitorUUID):
    global dfDocuments

    documentUUIDs = []
    visitorUUIDs = []

    vUUIDs = getVisitorUUIDs(documentUUID)
    for v in vUUIDs:
        if isinstance(v, str):
            visitorUUIDs.append(v)

    print(visitorUUIDs)
    print("\n")

    if len(visitorUUID) > 0:
        dUUIDs = getDocumentUUIDs(visitorUUID)
        for d in dUUIDs:
            if isinstance(d, str):
                documentUUIDs.append(d)

    for v in visitorUUIDs:
        if isinstance(v, str):
            dUUIDs = getDocumentUUIDs(v)
            for d in dUUIDs:
                if isinstance(d, str):
                    documentUUIDs.append(d)

    print(documentUUIDs)
    print("\n")

    dot = Digraph(comment="Also likes graph")

    for d in documentUUIDs:
        if isinstance(d, str):
            strd = str(d[-4:])
            dot.node(strd, strd)

    for v in visitorUUIDs:
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


def Func7():
    print("Func7")


startProcess()