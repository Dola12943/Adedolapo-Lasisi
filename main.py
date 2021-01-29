from queue import Queue
from commoncrawl.Panther import Panther
from commoncrawl.opencrawl import *

PROJECT_NAME ='commoncrawl'
HOMEPAGE = 'https://commoncrawl.org/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()
Panther(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)
