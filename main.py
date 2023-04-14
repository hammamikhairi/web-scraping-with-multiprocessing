
from Scraper         import Scraper
from Parser          import Parser
from Countries_Setup import set_up_countries
from json            import dump
from time            import sleep
from os              import path, environ
from AzureClient     import AzureClient

COUNTRIES_PATH = "countries.json"
COUNTRIES_PATH = "ct2.json"
LOG_FILE       = "temp_log.log"

if __name__ == "__main__":

    # Checking for countries
    if not path.isfile(COUNTRIES_PATH):
        print(">> SETTING UP COUNTRIES:")
        set_up_countries(COUNTRIES_PATH)
    
    # Declaring Managers
    sc = Scraper(LOG_FILE, COUNTRIES_PATH, 1)
    pr = Parser(LOG_FILE)

    # load scraping data
    sc.load_data()

    # Scape Data
    print(">> SCRAPING DATA:")
    sc.start()
    

    # Parse The Scraped Data
    print(">> PARSING DATA:")
    temp_values = pr.parse()

    print(">> Saving Data:")
    client = AzureClient(environ.get("YOUR_SQL_SERVER_PASSWORD"))
    client.exec_push(temp_values)