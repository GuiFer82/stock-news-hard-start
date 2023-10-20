import datetime
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "WNJXJYB5OZ9F5UKS"
NEWS_API_KEY = "03c399e204924810bd447926e8ba38ab"

account_sid = "AC76f961dc9b718b39d422f8b0e22b31c4"
auth_token = "09e15c174e4c900135f96672c73a7cdc"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_API_KEY,
}

news_parameters = {
    "q": COMPANY_NAME,
    "apiKey": NEWS_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()

print(response.json()["Time Series (Daily)"])

daily_data = response.json()["Time Series (Daily)"]

yesterday = datetime.datetime.now() - datetime.timedelta(days = 1)
day_before = yesterday - datetime.timedelta(days=1)
yesterday_price = float(daily_data[str(yesterday.date())]["4. close"])
day_before_price = float(daily_data[str(day_before.date())]["4. close"])
difference = round(yesterday_price - day_before_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(difference) <= yesterday_price * 0.05:

    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response.raise_for_status()
    news = response.json()["articles"][:3]

    formatted_articles = [f"{STOCK}: {up_down}{difference}% \nHeadline: {item['title']}. \nURL: {item['url']}" for item in news]

    client = Client(account_sid, auth_token)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_='+13233105246',
            to='+447432054156'
        )

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

