#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import find_cheapest_flight
import time
from datetime import datetime, timedelta
from notification_manager import NotificationManager

sheet = DataManager()
sheet_data = sheet.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY = "FRA"


for items in sheet_data:
    if items["iataCode"] == "":
        city = items["city"]
        code = flight_search.get_destination_codes(city)
        items["iataCode"] = code
        time.sleep(2)

sheet.destination_data = sheet_data
sheet.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_months_from_today = datetime.now() + timedelta(days=(6*30))

for destinations in sheet_data:
    print(f"Getting Flights for {destinations['city']} ...")
    flights = flight_search.check_flights(
        ORIGIN_CITY,
        destinations['iataCode'],
        from_time=tomorrow,
        to_time=six_months_from_today,
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destinations['city']}: {cheapest_flight.price} EUR")
    time.sleep(2)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destinations["lowestPrice"]:
        print(f"Lower price flight found to {destinations['city']}!")

        notification_manager.send_sms(
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
                         f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        )