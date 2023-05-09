import os
from  configparser import SafeConfigParser
import logging.config
from datetime import date
from time import sleep
from pymongo import MongoClient
import requests
import random
import json

from src.config import *

today = str(date.today()) ## Getting date for each day
# today = "2022-10-20"

def get_logger(name="root"):
    '''
    This function used for logging the error and other information
    '''
    base_path = os.path.join(os.getcwd(), 'logs')
    
    ## Create logs folder if not present
    log_file = os.path.join(base_path, 'log.conf')
    logging.config.fileConfig(fname=log_file, disable_existing_loggers=False)

    return logging.getLogger(name)

        

def connect_mong():

    logger = get_logger(__name__)
    try:
        conn = MongoClient()
        logger.info("Connected successfully to MongoDB")
    except:  
        logger.exception("Could not connect to MongoDB. Quitting the program!!")
        exit()

    # database
    db = conn.social_media_automation
    return db

def get_html_content(site):
    content = requests.get(site).text
    return content

def string_present(str1, str2):
    if str1.find(str2) > 0:
        return True
    
    
def user_download(url, filename):
    r = requests.get(url)
    base_path = '/'.join(os.path.abspath(os.getcwd()).split('/')[:-1]) + IMG_PATH
    # filename = filename.replace('/', '_')
    # filename = filename.replace(' ', '')
    out_path = base_path + filename + ".png"
    with open(out_path, 'wb') as f:
        f.write(r.content)
    return out_path

def format_pfm_date(date):
    split_date = date.split(' ')
    day = split_date[0]
    month = MONTH_MAP[split_date[1].lower()]
    year = split_date[2]
    final_date = year + '-' + month + '-' + day
    
    return final_date

def format_fmlink_date(month, date, year):
    date = date[0:2]
    month = MONTH_MAP_SHORT[month.lower()]
    final_date = year + '-' + month + '-' + date
    
    return final_date

def format_facilitate_date(date):
    split_date = date.split(' ')
    day = split_date[1][0:len(split_date[1])-2]
    if(len(day)==1):
        day = '0'+day
    month = MONTH_MAP[split_date[2].lower()]
    year = split_date[3]
    final_date = year + '-' + month + '-' + day
    
    return final_date
    

def format_bfm_date(date):
    split_date = date.split(' ')

    day = split_date[1][:-1]
    month = MONTH_MAP[split_date[0].lower()]
    year = split_date[2]
    final_date = year + '-' + month + '-' + day
    
    return final_date


def format_tmrw_date(date):
    date = date.split(' ')[-1]
    split_date = date.split('/')
    day = split_date[0]
    month = split_date[1]
    year = split_date[2]
    
    final_date = year + '-' + month + '-' + day
    
    return final_date

def format_iwfm_date(month, date, year):
    date = date[0:2]
    month = MONTH_MAP[month.lower()]
    final_date = year + '-' + month + '-' + date
    
    return final_date


def get_priority(contents):
    evbex_contents = []
    fmj_contents = []
    bmf_contents = []
    pfm_contents = []
    ifma_contents = []
    new_contents = []
    
    # Categorize contents based on flags
    for each in contents:
        if each['fmj'] == 1:
            fmj_contents.append(each)
        elif each['evbex'] == 1:
            evbex_contents.append(each)
        elif each['bmf'] == 1:
            bmf_contents.append(each)
        elif each['pfm'] == 1:
            pfm_contents.append(each)
        elif each['ifma'] == 1:
            ifma_contents.append(each)
    
    # Select 2 evbex_contents if available
    if len(evbex_contents) >= 2:
        new_contents.extend(random.sample(evbex_contents, 2))
    
    # Select the remaining contents from other arrays
    remaining = 3 - len(new_contents)
    other_contents = fmj_contents + bmf_contents + pfm_contents + ifma_contents
    if remaining > 0 and len(other_contents) > 0:
        sampled = random.sample(other_contents, min(remaining, len(other_contents)))
        random.shuffle(sampled)
        new_contents.extend(sampled)
    
    print(json.dumps(new_contents))
    return new_contents