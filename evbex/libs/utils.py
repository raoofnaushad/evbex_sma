from datetime import date, datetime

from pymongo import MongoClient

today = str(date.today())

try:
    conn = MongoClient()
    print("Connected successfully to MongoDB")
except:  
    print("Could not connect to MongoDB")

# database
db = conn.social_media_automation

def get_data_from_mongo(date):
    collection = db.newsletter
    data = collection.find({"date" : date}) #initially it was today
    data = date_reverse(data)
    data = img_path_correction(data)
    # data = trim_articles(data)
    for each in data:
        each["text"] = ' '.join(each["text"].split()[:85]) + ' ..'
    print(f"Data found from mongo for the date: {today}")
    print(data)
    return data

def img_path_correction(newses):
    updated_news = list()
    for news in newses:
        news["image"] = news["image"].split('/')[-1]
        updated_news.append(news)
    return updated_news


def date_reverse(newses):
    updated_news = list()
    for news in newses:
        news["date"] = datetime.strptime(news["date"], "%Y-%m-%d").strftime("%d-%m-%Y")
        updated_news.append(news)
    return updated_news

def trim_articles(newses):
    l = []
    for news in newses:
        l.append(news["text"][:270])
    return l


def add_subscribers(name, email):
    try:
        subscriber = {
            "name" : name,
            "email" : email
            }
        collection = db.subscribers
        rec_id1 = collection.insert_one(subscriber)
        print(f"Inserted a new subscriber <> name: {name}, email: {email}")
    except Exception as ex:
        print(f"Error in adding the subscriber: {ex}")

def remove_subscribers(email):
    try:
        subscriber = {
            "email" : email
            }
        collection = db.subscribers
        rec_id1 = collection.delete_one(subscriber)
        print(f"Deleted subscriber <> email: {email}")
    except Exception as ex:
        print(f"Error in adding the subscriber: {ex}")