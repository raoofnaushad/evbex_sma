from flask import Flask, render_template, request
import requests
from datetime import datetime, date

from libs.utils import *

app = Flask(__name__)


@app.route('/')
def home():
    newses = get_data_from_mongo(str(date.today()))
    print(str(date.today()))
    flag_date  = 0
    return render_template('index_new.html', newses = newses, flag_date = flag_date, ads = 1, link = "http://127.0.0.1:5000")


@app.route('/', methods=['POST'])
def home_date_selected():
    post_on_date = []
    user_selected_date = datetime.strptime(request.form['date'],"%Y-%m-%d").strftime("%d-%m-%Y")
    newses = get_data_from_mongo(request.form['date'])
    print(request.form['date'])
    
    try:
        for news in newses:
            if news["date"] == user_selected_date:
                post_on_date.append(news)
        return render_template("index_new.html", newses = post_on_date, flag = len(post_on_date), date = user_selected_date, link = "http://127.0.0.1:5000")
    except:
        return render_template("index_new.html", flag=0, date = "choose a valid date!")


@app.route("/subscribe", methods=['POST'])
def subs():
    newses = get_data_from_mongo(str(date.today()))
    name = request.form['name']
    mail = request.form['mail']
    add_subscribers(name, mail)
    return render_template("index_new.html", newses = newses[:10], subs = 1)



@app.route("/unsubscribe", methods=['POST'])
def unsubs():
    newses = get_data_from_mongo(str(date.today()))
    mail = request.form['mail']
    remove_subscribers(mail)
    return render_template("index_new.html", newses = newses[:10], subs = -1)


if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=8080)
    