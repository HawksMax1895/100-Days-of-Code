import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client
import time

load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stocks_api = os.environ.get("ALPHAVANTAGE_API_KEY")
news_api = os.environ.get("NEWS_API_KEY")
account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stocks_url = 'https://www.alphavantage.co/query'
param_stocks = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": stocks_api
}
stocks = requests.get(stocks_url, params=param_stocks)
stocks.raise_for_status()

data = stocks.json().get("Time Series (Daily)")
print(data)

sorted_dates = sorted(data.keys(), reverse=True)
yesterday_date = sorted_dates[0]
day_before_date = sorted_dates[1]

yesterday_close = float(data[yesterday_date]["4. close"])
day_before_close = float(data[day_before_date]["4. close"])
difference = abs(float(yesterday_close - day_before_close))
difference_rel = difference / yesterday_close

if difference_rel > 0.1:
    news_url = "https://newsapi.org/v2/everything"
    param_news = {
        "q": COMPANY_NAME,
        "apiKey": news_api,
        "pageSize": 3
    }

    client = Client(account_sid, auth_token)

    message_sms = ""
    difference_rel_round = round(difference_rel*100, 1)

    if yesterday_close > day_before_close:
        message_sms = f"{STOCK}: 🔺{difference_rel_round}%"
    else:
        message_sms = f"{STOCK}: 🔻{difference_rel_round}%"

    message1 = client.messages.create(
        body=f"{message_sms}",
        from_="+12315946472",
        to="+4917645999428",
    )

    news = requests.get(news_url, params=param_news)
    news.raise_for_status()
    data_news = news.json()

    for article in data_news["articles"]:
        title = article.get("title", "No Title")
        description = article.get("description", "No Description")
        print(f"Title: {title}\nDescription: {description}\n")
        message2 = client.messages.create(
            body=f"Headline: {title}",
            from_="+12315946472",
            to="+4917645999428",
        )
        time.sleep(2)
        message3 = client.messages.create(
            body=f"Brief: {description}",
            from_="+12315946472",
            to="+4917645999428",
        )

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

