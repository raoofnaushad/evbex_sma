
from pymongo import MongoClient
from datetime import date, datetime, timedelta
import random

today = str(date.today())

try:
    conn = MongoClient()
    print("Connected successfully to MongoDB")
except:  
    print("Could not connect to MongoDB")

# database
db = conn.social_media_automation

def get_subscribers_mongo():
    collection = db.subscribers
    data = collection.find() #initially it was today
    data = [d for d in data]
    subs = []
    for d in data:
        subs.append((d['email'], d['name']))
    
    return subs


def get_n_prev_date(N_DAYS_AGO):
    today = date.today()
    n_days_ago = today - timedelta(days=N_DAYS_AGO)
    return str(n_days_ago)


def get_data_from_mongo():

    collection = db.newsletter
    
    dates_req = []
    for i in range(6):
        dates_req.append(get_n_prev_date(i))

    # data = collection.find({"$and":[ {"evbex":0}, 
    #                                 {"$or":[ 
    #                                     {"date":dates_req[0]}, 
    #                                     {"date":dates_req[1]},
    #                                     {"date":dates_req[2]},
    #                                     {"date":dates_req[3]},
    #                                     {"date":dates_req[4]},
    #                                     {"date":dates_req[5]},
    #                                 ]}
    #                                 ]
    #                         },{'_id':False})
    

    # data = [each for each in data]
    
    
    data_fmj = collection.find({"$and":[ 
                                    {"evbex":0}, 
                                    {"fmj" : 1},
                                    {"$or":[ 
                                        {"date":dates_req[0]}, 
                                        {"date":dates_req[1]},
                                        {"date":dates_req[2]},
                                        {"date":dates_req[3]},
                                        {"date":dates_req[4]},
                                        {"date":dates_req[5]},
                                    ]}
                                    ]
                            },{'_id':False})
    

    data_fmj = [each for each in data]
    
    
    data_non_fmj = collection.find({"$and":[ 
                                    {"evbex":0}, 
                                    {"fmj" : 0},
                                    {"$or":[ 
                                        {"date":dates_req[0]}, 
                                        {"date":dates_req[1]},
                                        {"date":dates_req[2]},
                                        {"date":dates_req[3]},
                                        {"date":dates_req[4]},
                                        {"date":dates_req[5]},
                                    ]}
                                    ]
                            },{'_id':False})
    

    data_non_fmj = [each for each in data]
    
    # if len(data) == 0:
    #     # exit()
    #     print(f"No data found for this week: {today}")
    #     data = collection.find({"$or":[ 
    #                                     {"date":dates_req[0]}, 
    #                                     {"date":dates_req[1]},
    #                                     {"date":dates_req[2]},
    #                                     {"date":dates_req[3]},
    #                                     {"date":dates_req[4]},
    #                                     {"date":dates_req[5]},
    #                                     ]},{'_id':False})
        
    #     data = [each for each in data]
        
    # # datas = []
    # # for each in data:
    # #     if each not in datas:
    # #         datas.append(each)
    
    # data = set(data)
    if len(data_non_fmj) > 5:
        data_non_fmj = random.sample(data_non_fmj, 3)
        
    if len(data_fmj) > 5:
        data_fmj = random.sample(data_fmj, 2)
    
    data = data_non_fmj + data_fmj
    
    for each in data:
        each["text"] = ' '.join(each["text"].split()[:85]) + ' ..'
    print(f"Data found from mongo for the date: {today}")
    return data         

