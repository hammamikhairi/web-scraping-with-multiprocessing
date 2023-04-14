
import requests
import json
from multiprocessing import Process, Value, Lock
from dataclasses import dataclass


class Scraper:
  BASE_URL : str 
  OUT_FILE : str
  IN_FILE : str
  MAX_THREADS : int = 1
  COUNTRIES_DICT : dict

  def __init__(self, outfile :  str, infile : str, maxthreads : int):
    self.OUT_FILE    = outfile
    self.IN_FILE     = infile
    self.MAX_THREADS = maxthreads

  def scrape(self,country, max_threads_counter, mutex) -> None:
      res = requests.post("https://countriesnow.space/api/v0.1/countries/capital", data={"country" : country})
      try:
        info = json.loads(res.content)["data"]["capital"]
      except:
        info = "#"

      finally:
        with mutex :
          with open(self.OUT_FILE, 'a') as f:
            print(f'{country}:{info}')
            f.write(f'{country}:{info}\n')

        with max_threads_counter.get_lock():
          max_threads_counter.value  += 1

  def load_data(self):
    with open(self.IN_FILE, "r") as f:
      self.COUNTRIES_DICT = json.load(f)


  def start(self):
    mutex = Lock()
    max_threads_counter = Value('d', self.MAX_THREADS)
    for country, _ in self.COUNTRIES_DICT.items():
        if max_threads_counter.value != 0 : 		
          max_threads_counter.value -= 1
	
          process = Process(target=self.scrape, args=(country, max_threads_counter, mutex)) 
          process.start()
        while max_threads_counter.value == 0:
          continue

    while max_threads_counter.value != self.MAX_THREADS:
      continue