import requests

from bs4 import BeautifulSoup
from datetime import datetime


def main():
    url = "https://andelenergi.dk/kundeservice/aftaler-og-priser/timepris/"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")
    match = soup.find(name="canvas", attrs={"class": "hourly-price__chart-canvas"})

    monitoredDinnerHours = [
        "18:00",
        "19:00",
        "20:00",
        "21:00",
    ]
    monitoredWashingHours = [
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
        "22:00",
        "23:00",
    ]
    headings = match.get("data-headings").strip('"[]')
    prices = match.get("data-prices").strip('"[]')

    dinnerHours = {}
    washingHours = {}

    for idx, heading in enumerate(headings.split(",")):
        heading = heading.strip('"')
        price = prices.split(",")[idx].strip('"')

        if heading in monitoredDinnerHours:
            dinnerHours[heading] = round(float(price), 2)

        if heading in monitoredWashingHours:
            washingHours[heading] = round(float(price), 2)

    dinnerString = ""
    for i, item in enumerate(sorted(dinnerHours.items(), key=lambda x: x[1])):
        dinnerString += str(item[0]) + ": " + str(item[1]) + " Kr/kWh"

        if i != len(dinnerHours.items()) - 1:
            dinnerString += "\n"

    washingString = ""
    for i, item in enumerate(sorted(washingHours.items(), key=lambda x: x[1])[:5]):
        washingString += str(item[0]) + ": " + str(item[1]) + " Kr/kWh"

        if i != len(washingHours.items()) - 1:
            washingString += "\n"

    return (
        "Energy prices for "
        + datetime.now().strftime("%d.%m.%Y")
        + "\n\nBest times to cook dinner:\n"
        + dinnerString
        + "\n\nBest time to wash:\n"
        + washingString
    )


main()
