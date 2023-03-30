
from Scraper         import Scraper
from Parser          import Parser
from Countries_Setup import set_up_countries
from json            import dump
from time            import sleep
from os              import path
from utils           import notification, get_date

COUNTRIES_PATH = "countries.json"
LOG_FILE       = "weather.log"

if __name__ == "__main__":

    # Checking for countries
    if not path.isfile(COUNTRIES_PATH):
        print(">> SETTING UP COUNTRIES:")
        set_up_countries(COUNTRIES_PATH)
    
    # Declaring Managers
    sc = Scraper(LOG_FILE, COUNTRIES_PATH, 64)
    pr = Parser(LOG_FILE)

    # load scraping data
    sc.load_data()

    # Scape Data
    print(">> SCRAPING DATA:")
    sc.start()

    # Parse The Scraped Data
    print(">> PARSING DATA:")
    temp_dict, temp_rel, avg = pr.parse()
    print(temp_dict, temp_rel, avg, sep="\n\n")

    print(">> Saving Data:")
    file_base = "Data/" + get_date().replace(" ", "_")
    # in case we want to save the data for later processing
    # with open(file_base + "-all.json", "w") as f:
    #     dump(temp_dict, f)
    # with open(file_base + "-per_country.json", "w") as f:
    #     dump(temp_rel, f)

    # Clear weather.log for next iteration
    print(">> CLEARING LOG:")
    tmp = open("weather.log", "w")
    tmp.close()

    print(">> SENDING NOTIFICATION:")
    notification(avg)