# Reads csv data files and transforms them to usable form

import sys
import os
import csv

INDICATOR_CODES = ["EG.CFT.ACCS.ZS", "EG.ELC.ACCS.RU.ZS", "EG.ELC.ACCS.UR.ZS",
    "EG.ELC.ACCS.ZS", "EG.ELC.COAL.ZS", "EG.ELC.FOSL.ZS", "EG.ELC.HYRO.ZS",
    "EG.ELC.LOSS.ZS", "EG.ELC.NGAS.ZS", "EG.ELC.NUCL.ZS", "EG.ELC.PETR.ZS",
    "EG.ELC.RNEW.ZS", "EG.ELC.RNWX.KH", "EG.ELC.RNWX.ZS", "EG.FEC.RNEW.ZS",
    "EG.IMP.CONS.ZS", "EG.USE.COMM.CL.ZS", "EG.USE.COMM.FO.ZS", "EG.USE.CRNW.ZS",
    "EG.USE.ELEC.KH.PC", "EN.ATM.CO2E.EG.ZS", "EN.ATM.CO2E.GF.KT",
    "EN.ATM.CO2E.GF.ZS", "EN.ATM.CO2E.KT", "EN.ATM.CO2E.LF.KT", "EN.ATM.CO2E.LF.ZS",
    "EN.ATM.CO2E.PC", "EN.ATM.CO2E.SF.KT", "EN.ATM.CO2E.SF.ZS", "EN.ATM.GHGO.KT.CE",
    "EN.ATM.GHGO.ZG", "EN.ATM.GHGT.KT.CE", "EN.ATM.GHGT.ZG", "EN.ATM.METH.EG.KT.CE",
    "EN.ATM.METH.EG.ZS", "EN.ATM.METH.KT.CE", "EN.ATM.METH.ZG",
    "EN.ATM.NOXE.EG.KT.CE", "EN.ATM.NOXE.EG.ZS", "EN.ATM.NOXE.KT.CE",
    "EN.ATM.NOXE.ZG", "EN.ATM.PM25.MC.M3", "EN.ATM.PM25.MC.T1.ZS",
    "EN.ATM.PM25.MC.T2.ZS", "EN.ATM.PM25.MC.T3.ZS", "EN.ATM.PM25.MC.ZS",
    "EN.CO2.BLDG.ZS", "EN.CO2.ETOT.ZS", "EN.CO2.MANF.ZS", "EN.CO2.OTHX.ZS",
    "EN.CO2.TRAN.ZS"]


def parseFile(filename):

    country = ""
    countryCode = ""
    indicators = []
    data = []
    indicatorsLeft = len(INDICATOR_CODES)

    # Get data directory
    parentDir = os.getcwd()
    filePath = os.path.join(parentDir, "data", filename)

    try:
        file = open(filePath, "r")
    except FileNotFoundError:
        print(f"-CRITICAL- File {filename} not found!")
        sys.exit(0)

    lines = file.readlines()[5:]
    lines = [line.strip() for line in lines]

    # Skip info lines in file
    for _ in range(5):
        file.readline()

    line = file.readline().split(",")
    country = line[0][1:-1]
    countryCode = line[1][1:-1]
    
    while True:
        if line[3][1:-1] in INDICATOR_CODES:

            print(f"Found {line[3]}")

            # Save indicator info
            indicator = [line[3][1:-1], line[2][1:-1]]
            indicators.append(indicator)

            # Save indicator data
            metrics = []
            for value in line[4:]:
                # If value is not empty, add it
                if value != "\"\"":
                    metrics.append(value[1:-1])
                else:
                    metrics.append("-")
            data.append(metrics)

            indicatorsLeft -= 1
            if indicatorsLeft == 0:
                break
        
        nextLine = file.readline()
        if not nextLine:
            print("-WARNING- Not all selected indicators found!")
            break
        line = nextLine.split(",")

    print("Data parsed successfully\n")
    print(f"{country} {countryCode}\n")

    for i, d in zip(indicators, data):
        print(f"{i[0]} {i[1]}")
        print(*d)
        print()

    file.close()

parseFile("greece.csv")