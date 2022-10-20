

from src.utils import *
from src.config import *
from scrapers import fmj_scraping, iwfm_scrapping, pfm_scraping, bfm_scraping, evbex_scraping, ifma_scrapping, tomorrow_scraping,  facilitatemag, fmlink_scrapping


class Scraper():
    def __init__(self, contents):
        self.contents = contents
        
    def scrape_news(self, site):
        logger = get_logger(__name__)
        scraped = list()
        
        try:
            if site == "FMJ":
                logger.info("Scraping FMJ Journal")
                scraped = fmj_scraping.main()
                
            elif site == "PFM":
                logger.info("Scraping PFMonthnet Journal")
                scraped = pfm_scraping.main()
                
            elif site == "BFM":
                logger.info("Scraping BFM Journal")
                scraped = bfm_scraping.main()

            elif site == "TOMORROW_FM":
                logger.info("Scraping TOMORROWS FM Journal")
                scraped = tomorrow_scraping.main()
            
            elif site == "FACILITATE_MAGAZINE":
                logger.info("Scraping FACILITATE MAGAZINE Journal")
                scraped = facilitatemag.main()
            
            elif site == "FMLINK_MAGAZINE":
                logger.info("Scraping FMLINK MAGAZINE Journal")
                scraped = fmlink_scrapping.main()

            elif site == "EVBEX":
                logger.info("Scraping EVBEX Journal")
                scraped = evbex_scraping.main()

            elif site == "IFMA":
                logger.info("Scraping IFMA Journal")
                scraped = ifma_scrapping.main()
            
            elif site == "IWFM":
                logger.info("Scraping IWFM Journal")
                scraped = iwfm_scrapping.main()
                
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
            
            db = connect_mong()
            coll = db.newsletter
            coll.delete_many({"date" : today})
            logger.info(f"Data deleted from mongo for the date: {today}")
            coll.insert_many(self.contents)
            logger.info(f"{len(self.contents)} number of data inserted to mongo for the date: {today}")
            
        except Exception as ex:
            logger.exception(f"Problem with writing to db: {str(ex)}")



def start_scraping():
    logger = get_logger(__name__)
    contents = list()
    
    scrape = Scraper(contents)
    
    ## Scraping FMJ
    scrape.contents.extend(scrape.scrape_news("FMJ"))
    
    ## Scraping PFMONTHNET
    scrape.contents.extend(scrape.scrape_news("PFM"))
    
    ## Scraping BFM
    scrape.contents.extend(scrape.scrape_news("BFM"))
    
    ## Scraping BFM
    scrape.contents.extend(scrape.scrape_news("TOMORROW_FM"))

    #Scrapping Facilitate magazine
    scrape.contents.extend(scrape.scrape_news("FACILITATE_MAGAZINE"))

    # Scrapping fmlink magazine
    scrape.contents.extend(scrape.scrape_news("FMLINK_MAGAZINE"))

    ## Scraping Evbex
    scrape.contents.extend(scrape.scrape_news("EVBEX"))

    ## Scraping IFMA
    scrape.contents.extend(scrape.scrape_news("IFMA"))

    ## Scraping IFMA
    scrape.contents.extend(scrape.scrape_news("IWFM"))

    # Writing to DB
    scrape.write_news_to_db()
    
        
    file = open("scrappedcontents.txt", "w")
    file.writelines(f'Date: {today}\n')
    file.writelines("###"*10)
    file.writelines("\n")
    for scrapped_articles in scrape.contents:
        file.writelines(scrapped_articles["article"])
        file.writelines('\n')


if __name__ == "__main__":
    start_scraping()