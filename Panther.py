
from urllib.request import urlopen
from commoncrawl.link_finder import LinkFinder
from commoncrawl.web import *




class Panther:

  # Class variables (shared among all instances)
  project_name = ''
  base_url = ''
  domain_name = ''
  queue_file = ''
  crawled_file = ''
  queue = set()
  crawled = set()

  def __init__(self, project_name, base_url, domain_name):
      Panther.project_name = project_name
      Panther.base_url = base_url
      Panther.domain_name = domain_name
      Panther.queue_file = self.project_name + '/queue.txt'
      Panther.crawled_file = self.project_name + '/crawled.txt'
      self.boot()
      self.crawl_page('First panther', Panther.base_url)

  @staticmethod
  def boot():
        create_project_dir(Panther.project_name)
        create_data_files(Panther.project_name, Panther.base_url)
        Panther.queue = file_to_set(Panther.queue_file)
        Panther.crawled = file_to_set(Panther.crawled_file)

  @staticmethod
  def crawl_page(thread_name, page_url):
        if page_url not in Panther.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print(' Queue ' + str(len(Panther.queue)) + ' | Crawled ' + str(len(Panther.crawled)))
            Panther.add_links_to_queue(Panther.gather_links(page_url))
            Panther.queue.remove(page_url)
            Panther.crawled.add(page_url)
            Panther.update_files()

  @staticmethod
  def gather_links(page_url):
        html_string = ''
        try:
            response = urlopen(page_url)
            if response.getheader('Content-Type') == 'text/html':
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
                finder = LinkFinder(Panther.base_url, page_url)
                finder.feed(html_string)
        except:
            print('Error: can not crawl page')
            return set()
        return finder.page_links()

  @staticmethod
  def add_links_to_queue(links):
      for url in links:
          if url in Panther.queue:
              continue
          if url in Panther.crawled:
              continue
          if Panther.domain_name not in url:
              continue
          Panther.queue.add(url)

  @staticmethod
  def update_files():
      set_to_file(Panther.queue, Panther.queue_file)
      set_to_file(Panther.crawled, Panther.crawled_file)
