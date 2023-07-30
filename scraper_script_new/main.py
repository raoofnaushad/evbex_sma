

from src.utils import *
from src.config import *
import random
from scrapers import upkeep_scraping, fmi_scrapping, qad_scrapping

class Scraper():
    def __init__(self, contents):
        self.contents = contents
        
    def scrape_news(self, site):
        logger = get_logger(__name__)
        scraped = list()
        
        try:
            if site == "UPKEEP":
                logger.info("Scraping UPKEEP Journal")
                scraped = upkeep_scraping.main()
            
            elif site == "QAD":
                logger.info("Scraping QAD Journal")
                scraped = qad_scrapping.main()

                
            logger.info(f"Scraped contents from {site} is: {len(scraped)}")
            return scraped

        except Exception as ex:
            logger.exception(f"Problem with Scraping: {str(ex)}")
            return scraped
    
    def write_news_to_db(self):
        logger = get_logger(__name__)
        try:
            if not self.contents:
                logger.info(f'No data scraped. Thus nothing to write')
                exit()
                
            self.contents = get_priority(self.contents) # To add previous data
            
            db = connect_mong()
            coll = db.new_newsletter
            coll.delete_many({"date" : today})
            logger.info(f"Data deleted from mongo for the date: {today}")
            random.shuffle(self.contents)
            coll.insert_many(self.contents)
            logger.info(f"{len(self.contents)} number of data inserted to mongo for the date: {today}")
            
        except Exception as ex:
            logger.exception(f"Problem with writing to db: {str(ex)}")



def start_scraping():
    logger = get_logger(__name__)
    contents = list()
    
    scrape = Scraper(contents)
    
    ## Scraping UPKEEP
    scrape.contents.extend(scrape.scrape_news("UPKEEP"))
    
    # Scraping QAD
    scrape.contents.extend(scrape.scrape_news("QAD"))
    

    # Writing to DB
    scrape.write_news_to_db()


if __name__ == "__main__":
    start_scraping()