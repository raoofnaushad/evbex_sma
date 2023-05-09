from bs4 import BeautifulSoup
from src.config import *
from src.utils import *

def get_article_links(content):
    article_links = list()
    soup = BeautifulSoup(content, 'lxml')
    countfrdates = 0
    posts = soup.find_all('div', class_="resource-item")
    dates = soup.find_all('div', class_="resource-item-content")
    # for date in dates:
    #     print(date.text.split("\n")[2].split("\t")[4])
    for article in posts:
        link = article.a['href']
        dateofart =  dates[countfrdates].text.split("\n")[2].split("\t")[4].split(" ")
        countfrdates+=1
        formatted_date = format_iwfm_date(dateofart[1], dateofart[0], dateofart[2])   #month date and year

        if formatted_date == today:
            article_links.append(link)
    
    return article_links


def scrape_each_article(link):
    try:
        content = get_html_content(link)
        article = BeautifulSoup(content, 'lxml')
        heading = article.find('div', class_ = "entry").h1.text
        heading_cleaned = ''.join(letter for letter in heading if letter.isalnum())
        
        img_src = article.find('div', class_ = "entry").img['src']
        img_path = user_download(img_src, heading_cleaned)
        article_content = article.find_all('p')[3].text[:500]
        content = {
            "date" : today,
            "article": heading,
            "image": img_path,
            "image_src" : img_src,
            "text": article_content,
            "c2a_link": link,
            "c2a_button": "Read from Source",
            "evbex" : 0,
            "fmj" : 0,
            "bmf" : 0,
            "pfm" : 0,
            "ifma" : 0
        }
        return content
        
    except Exception as ex:
        logging.exception(f"Some error with the link: {link}")
        logging.exception(f"Error: {str(ex)}")
        logging.exception(f"***"*5)
        return None

def main():
    contents = list()

    content = get_html_content(IWFM_LINK)
    
    articles = get_article_links(content)
    
    for article in articles:
        out = scrape_each_article(article)
        if out:
            contents.append(out)
    print(f"Number of articles from IFMAScrapping: {len(contents)}")
    return contents

# main()
