import os
from  configparser import SafeConfigParser
import logging.config
from datetime import date, timedelta, datetime
from time import sleep
from pymongo import MongoClient
import requests
import random
import json
from PIL import Image
from io import BytesIO

from colorama import Fore, Back, Style

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

def get_html_content(site, isHeadersNeeded=True):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    # print(content)
    if isHeadersNeeded:
        content=requests.get(site, headers=headers).text
    else:
        content=requests.get(site).text
   
    return content

def string_present(str1, str2):
    if str1.find(str2) > 0:
        return True
    
    
def user_download(url, filename, isHeadersNeeded=True):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
    if isHeadersNeeded:
        r=requests.get(url,headers=headers)
    else:
        r=requests.get(url)

    # Check if the response was successful
    if r.status_code != 200:
        raise Exception("Error occurred while downloading the image")

    base_path = '/'.join(os.path.abspath(os.getcwd()).split('/')[:-1]) + IMG_PATH
    out_path = base_path + filename + ".png"

    # Convert WebP image to PNG
    with Image.open(BytesIO(r.content)) as img:
        img.save(out_path, "PNG")

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

def format_fmi_date(date_string):
    # Parse the input date string
    date_object = datetime.strptime(date_string, "%d %B %Y")
    # Format the date in the desired format
    formatted_date = date_object.strftime("%Y-%m-%d")
    return formatted_date
    

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


def format_upkeep_date(date_string):
    date_string = date_string.replace('Publish Date: ', '')
    
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date_string, '%B %d, %Y')
    
    # Convert the datetime object to the desired format 'YYYY-MM-DD'
    formatted_date = date_obj.strftime('%Y-%m-%d')
    
    return formatted_date

def format_qad_date(date_string):
    date_obj = datetime.strptime(date_string, '%B %d, %Y')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    
    return formatted_date

def format_upkeep_date_togetData(date_string):
    date_string = date_string.replace('Published on ', '')
    
    # Parse the date string into a datetime object
    date_obj = datetime.strptime(date_string, '%B %d, %Y')
    
    # Convert the datetime object to the desired format 'YYYY-MM-DD'
    formatted_date = date_obj.strftime('%Y-%m-%d')
    
    return formatted_date

def format_facilio_date(input_date): #Input "Jul 28, 2023" -> Output: "2023-07-28"
    try:
        # Parse the input date string into a datetime object
        date_obj = datetime.strptime(input_date, '%b %d, %Y')
        # Format the date object into the desired output format
        formatted_date = date_obj.strftime('%Y-%m-%d')
        return formatted_date
    except ValueError:
        return "Invalid date format. Please provide a date in the format 'Jul 28, 2023'."
    
def format_facilitiesnet_date(date_string):
    # Convert input date string to a datetime object
    input_date = datetime.strptime(date_string, '%m/%d/%Y')    
    # Format the datetime object as 'YYYY-MM-DD'
    formatted_date = input_date.strftime('%Y-%m-%d')    
    return formatted_date

def format_fmnaz_date(input_date): #Input "July 28, 2023" -> Output: "2023-07-28
    try:
        date_obj = datetime.strptime(input_date, "%B %d, %Y")
        output_date = date_obj.strftime("%Y-%m-%d")
        return output_date
    except ValueError:
        # Handle invalid input format
        return "Invalid input date format"

def getfilteredContent(list1,list2,highPriorityContent_length,lowPriorityContent_legnth):
    filterd_content=[]
    if len(list1)>highPriorityContent_length and len(list2)>lowPriorityContent_legnth:
        filtered_list_1 = list1[:highPriorityContent_length]
        filtered_list_2 = list2[:lowPriorityContent_legnth]
        filterd_content.extend(filtered_list_1+filtered_list_2)
    elif (len(list1) > 0):
        filtered_list_1 = list1
        # A total of 5 blogs are there excluding evbex blogs, as his requrement is to show 5 blogs from other Jonor=uals and 2 from evbex
        left_blog_count = 5 - len(list1) 
        filtered_list_2 = list2[:left_blog_count]
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
    fmi_contents = []
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
        elif each['fmi'] == 1:
            fmi_contents.append(each)
            
    blog_list_1 = fmj_contents + bmf_contents + ifma_contents
    blog_list_2 = tomorrow_contents + fmlink_contents + iwfm_contents + facmag_contents + pfm_contents + fmi_contents
    print(Fore.YELLOW + Back.BLUE +"Min priority Blog Length:", len(blog_list_1))
    print(Fore.YELLOW + Back.BLUE +"Max priority Blog Length:", len(blog_list_2), Style.RESET_ALL)
    len_evbex_blog = len(evbex_contents)
    
    if len_evbex_blog > 0:
        if len_evbex_blog >= 2:
            random.shuffle(evbex_contents)
            new_contents.extend(evbex_contents[:2])
        else:
            new_contents.extend(evbex_contents)
            
        remaining = 7 - len(new_contents)
        high_priority_content_length = round(0.6*remaining)
        low_priority_content_length = remaining-high_priority_content_length
        filtered_content = getfilteredContent(blog_list_2, blog_list_1, high_priority_content_length, low_priority_content_length)
        new_contents.extend(filtered_content)
    
    else:
        new_contents.extend(getfilteredContent(blog_list_2, blog_list_1, 3, 2))
    
    print(json.dumps(new_contents))
    return new_contents