import pdfquery as pq
import pandas as pd
import os

def scrapePdf(pdfPath):
    pdf = pq.PDFQuery(pdfPath)
    pdf.load()
    pdfData = pd.DataFrame({
            "countryName":  pdf.pq('LTTextLineHorizontal:overlaps_bbox("138.98, 686.86, 211.513, 697.9")').text(),
            "EPRETRSectorCode": pdf.pq('LTTextLineHorizontal:overlaps_bbox("180.26, 643.3, 185.857, 654.34")').text(),
            "eptrSectorName": pdf.pq('LTTextLineHorizontal:overlaps_bbox("210.29, 643.3, 471.936, 654.34")').text().split(" ", 1)[1],
            "EPRTRAnnexIMainActivityCode": pdf.pq('LTTextLineHorizontal:overlaps_bbox("52.8, 614.26, 157.097, 625.3")').text().split(" ", 1)[1],
            "EPRTRAnnexIMainActivityLabel": "",
            "FacilityInspireID": pdf.pq('LTTextLineHorizontal:overlaps_bbox("52.8, 715.9, 266.172, 726.94")').text().split(" ", 1)[1],
            "facilityName": pdf.pq('LTTextLineHorizontal:overlaps_bbox("52.8, 730.42, 343.076, 741.46")').text().split(" ", 2)[2],
            "City": pdf.pq('LTTextLineHorizontal:overlaps_bbox("138.98, 672.34, 221.195, 683.38")').text(),
            "CITY ID": pdf.pq('LTTextLineHorizontal:overlaps_bbox("138.98, 175.7, 312.518, 186.74")').text(),
            "targetRelease": pdf.pq('LTTextLineHorizontal:overlaps_bbox("138.98, 570.67, 154.094, 581.71")').text(),
            "pollutant": pdf.pq('LTTextLineHorizontal:overlaps_bbox("306.17, 570.67, 406.325, 581.71")').text(),
            "emission": pdf.pq('LTTextLineHorizontal:overlaps_bbox("152.06, 556.15, 185.857, 567.19")').text(),
            "DAY": pdf.pq('LTTextLineHorizontal:overlaps_bbox("174.62, 527.11, 185.857, 538.15")').text(),
            "MONTH": pdf.pq('LTTextLineHorizontal:overlaps_bbox("347.47, 527.11, 384.086, 538.15")').text().split(" ", 1)[0],
            "reportingYear": pdf.pq('LTTextLineHorizontal:overlaps_bbox("461.38, 527.11, 483.897, 538.15")').text(),
            "CONTINENT": pdf.pq('LTTextLineHorizontal:overlaps_bbox("437.02, 686.86, 473.96, 697.9")').text(),
            "max_wind_speed": pdf.pq('LTTextLineHorizontal:overlaps_bbox("52.8, 452.11, 185.806, 463.15")').text().split(" ", 1)[1],
            "avg_wind_speed": pdf.pq('LTTextLineHorizontal:overlaps_bbox("316.87, 452.11, 483.846, 463.15")').text().split(" ", 2)[2],
            "min_wind_speed": pdf.pq('LTTextLineHorizontal:overlaps_bbox("316.87, 452.11, 483.846, 463.15")').text().split(" ", 1)[0],
            "max_temp": pdf.pq('LTTextLineHorizontal:overlaps_bbox("144.02, 388.01, 185.806, 399.05")').text(),
            "avg_temp":  pdf.pq('LTTextLineHorizontal:overlaps_bbox("442.06, 388.01, 483.846, 399.05")').text(),
            "min_temp": pdf.pq('LTTextLineHorizontal:overlaps_bbox("311.23, 388.01, 405.714, 399.05")').text().split(" ", 1)[0],
            "DAYS WITH FOG": pdf.pq('LTTextLineHorizontal:overlaps_bbox("174.62, 323.93, 185.857, 334.97")').text(),
            "REPORTER NAME": pdf.pq('LTTextLineHorizontal:overlaps_bbox("356.95, 233.81, 504.706, 244.85")').text().split(":", 1)[1]
            }, index=[0])
    return pdfData


def getPdfNames():
    files = [f for f in os.listdir('.') if os.path.isfile(os.path.join('.', f))]
    for file in files:
        if file.split(".")[1] != 'pdf':
            files.remove(file)
    return files

def exportPdfsToCsv():
    master = pd.DataFrame()
    files = getPdfNames()
    for file in files:
        master = pd.concat([master, scrapePdf(file)], axis=0)
    master.to_csv('pdfs.csv', index=False)

exportPdfsToCsv()

