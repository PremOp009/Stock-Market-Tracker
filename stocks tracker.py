import requests
from twilio.rest import Client

api_key = "XY6F5VHPJH8XB7B5"
url= "https://www.alphavantage.co/query"
NEWS_API_KEY = "718b2cecf7a545ffadb6a6bd314b8fe8"
News_Url = "https://newsapi.org/v2/everything"
COMPANY_NAME  = "TSLA"
TWILIO_SID = "AC3ed4ed4c595dd4df416a28367678bec0"
TWILIO_AUTH_TOKEN = "b7165c08e97060749231c91f7afcf207"
TWILIO_PHONE_NUM = "+14789998269"
MY_PHONE = "+917990195921"




parameters ={
    "function":"TIME_SERIES_INTRADAY",
    "symbol":"TSLA",
    "interval":"30min",
    "apikey":"XY6F5VHPJH8XB7B5",
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

