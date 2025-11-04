import requests
from twilio.rest import Client

api_key = "Your api key"
url= "https://www.alphavantage.co/query"
NEWS_API_KEY = "Your api key"
News_Url = "https://newsapi.org/v2/everything"
COMPANY_NAME  = "TSLA"
TWILIO_SID = "Your SID"
TWILIO_AUTH_TOKEN = "Your Auth token"
TWILIO_PHONE_NUM = "your twilio phone"
MY_PHONE = "personal num"




parameters ={
    "function":"TIME_SERIES_INTRADAY",
    "symbol":"TSLA",
    "interval":"30min",
    "apikey":"your api",
}

response = requests.get(url=url,params=parameters)

#Yesterday's Closing price
data = response.json()["Time Series (30min)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]


#Day Before Yesterday's Closing Price
day_befor_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_befor_yesterday_data["4. close"]


#Difference between closing price
difference = (float(yesterday_closing_price) - float(day_before_yesterday_closing_price))
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"


diff_percent = (difference / float(yesterday_closing_price)) * 100


if abs(diff_percent) > 0.01 :
    news_params = {
        "apiKey":NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(url=News_Url,params=news_params)
    articles = news_response.json()["articles"]
    
    three_articles = articles[:3]
    

    formatted_article = [f"{COMPANY_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \n Breif:{article['description']}" for article in three_articles]
    


    client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
    for article in formatted_article:
        message = client.messages.create(
            body=article,
            from_=TWILIO_PHONE_NUM,
            to=MY_PHONE,
            
        )


