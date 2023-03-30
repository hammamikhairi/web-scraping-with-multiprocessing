
import requests
from bs4 import BeautifulSoup
import json
from multiprocessing import Process, Value, Lock
from dataclasses import dataclass


class Scraper:
  BASE_URL : str 
  OUT_FILE : str
  IN_FILE : str
  MAX_THREADS : int = 1
  SOUP_TARGET : dict = {"class" : "BNeawe iBp4i AP7Wnd"}
  COUNTRIES_DICT : dict

  def __init__(self, outfile :  str, infile : str, maxthreads : int):
    self.OUT_FILE    = outfile
    self.IN_FILE     = infile
    self.MAX_THREADS = maxthreads

  def scrape(self,country, city, max_threads_counter, mutex) -> None:
      res = requests.get(f'https://www.google.com/search?q=weather+{city}+{country}+°C&hl=en')
      soup = BeautifulSoup(res.content, 'html.parser') 

      try:
        temp = soup.find("div", attrs=self.SOUP_TARGET).text.split("°")[0]
        info = int(temp)
      except:
        info = "#"

      finally:
        with mutex :
          with open(self.OUT_FILE, 'a') as f:
            print(f'{country}:{city}:{info}')
            f.write(f'{country}:{city}:{info}\n')

        with max_threads_counter.get_lock():
          max_threads_counter.value  += 1

  def load_data(self):
    with open(self.IN_FILE, "r") as f:
      self.COUNTRIES_DICT = json.load(f)


  def start(self):
    mutex = Lock()
    max_threads_counter = Value('d', self.MAX_THREADS)
    for country, cities in self.COUNTRIES_DICT.items():
      for city in cities:
        if max_threads_counter.value != 0 : 		
          max_threads_counter.value -= 1
	
          process = Process(target=self.scrape, args=(country, city, max_threads_counter, mutex)) 
          process.start()
        while max_threads_counter.value == 0:
          continue

    while max_threads_counter.value != self.MAX_THREADS:
      continue