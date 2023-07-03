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
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    content = requests.get(site, headers=headers).text
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

def getfilteredContent(list1,list2,highPriorityContent_length,lowPriorityContent_legnth):
    filterd_content=[]
    if len(list1)>highPriorityContent_length and len(list2)>lowPriorityContent_legnth:
        filtered_list_1 = list1[:highPriorityContent_length]
        filtered_list_2 = list2[:lowPriorityContent_legnth]
        filterd_content.extend(filtered_list_1+filtered_list_2)
    else:
        total_list = list1+list2
        random.shuffle(total_list)
        filterd_content.extend(total_list[:(highPriorityContent_length+lowPriorityContent_legnth)])
        
    return filterd_content
    

def get_priority(contents):
    evbex_contents = []
    fmj_contents = []
    bmf_contents = []
    pfm_contents = []
    ifma_contents = []
    tomorrow_contents = []
    fmlink_contents = []
    iwfm_contents = []
    facmag_contents = []
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
        elif each['tomorrow'] == 1:
            tomorrow_contents.append(each)
        elif each['fmlink'] == 1:
            fmlink_contents.append(each)
        elif each['iwfm'] == 1:
            iwfm_contents.append(each)
        elif each['facmag'] == 1:
            facmag_contents.append(each)
            
    blog_list_1 = fmj_contents + bmf_contents + pfm_contents + ifma_contents
    blog_list_2 = tomorrow_contents + fmlink_contents + iwfm_contents + facmag_contents
    len_blog_1 = len(blog_list_1)
    len_blog_2 = len(blog_list_2)
    len_evbex_blog = len(evbex_contents)
    
    if len_evbex_blog > 0:
        if len_evbex_blog >= 2:
            random.shuffle(evbex_contents)
            new_contents.extend(evbex_contents[:2])
        else:
            new_contents.extend(evbex_contents)
            
        remaining = 5 - len(new_contents)
        high_priority_content_length = round(0.6*remaining)
        low_priority_content_length = remaining-high_priority_content_length
        filtered_content = getfilteredContent(blog_list_2, blog_list_1, high_priority_content_length, low_priority_content_length)
        new_contents.extend(filtered_content)
    
    else:
        new_contents.extend(getfilteredContent(blog_list_2, blog_list_1, 2, 1))
    
    print(json.dumps(new_contents))
    return new_contents