import requests

from bs4 import BeautifulSoup
from datetime import datetime


def main():
    url = "https://andelenergi.dk/kundeservice/aftaler-og-priser/timepris/"
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, features="html.parser")
    match = soup.find(name="canvas", attrs={"class": "hourly-price__chart-canvas"})

    monitored_dinner_hours = [
        "17:00",
        "18:00",
        "19:00",
        "20:00",
        "21:00",
    ]
    monitored_washing_hours = [
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

    dinner_hours = {}
    washing_hours = {}

    for idx, heading in enumerate(headings.split(",")):
        heading = heading.strip('"')
        price = prices.split(",")[idx].strip('"')

        if heading in monitored_dinner_hours:
            dinner_hours[heading] = round(float(price), 2)

        if heading in monitored_washing_hours:
            washing_hours[heading] = round(float(price), 2)

    dinner_string = ""
    for key, val in sorted(dinner_hours.items(), key=lambda x: x[1]):
        dinner_string += f"{key}: {val} Kr/kWh\n"

    washing_string = ""
    for key, val in sorted(washing_hours.items(), key=lambda x: x[1])[:5]:
        washing_string += f"{key}: {val} Kr/kWh\n"

    return (
        f"Energy prices for {datetime.now().strftime('%d.%m.%Y')}\n\n"
        + f"Best times to cook dinner:\n{dinner_string}\n"
        + f"Best time to wash:\n{washing_string}"
    )


main()
