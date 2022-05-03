# Web Crawling

Jupyter notebook version for web crawling among givven url's

A Web crawler starts with a list of URLs to visit. Those first URLs are called the seeds. As the crawler visits these URLs, by communicating with web servers that respond to those URLs, it identifies all the hyperlinks in the retrieved web pages and adds them to the list of URLs to visit, called the crawl frontier. URLs from the frontier are recursively visited according to a set of policies. If the crawler is performing archiving of websites (or web archiving), it copies and saves the information as it goes. The archives are usually stored in such a way they can be viewed, read and navigated as if they were on the live web, but are preserved as 'snapshots'


## URL's
Given in the code as list or url's, it is optional to read from .txt file (with space or '\n' as seperators) at the same directory.

## Constraints
We assume a maximum url's visits per main url (max_urls variable) and limited the number of entrances per link (max_link variable)


## Files

### HypeParameters.py
Constant parameters of all the scrifts (such as the constraing of visualization of the results)

### Crawler.py
Create CrawlingObject whice contain main_url and apply crawling by **CrawlingObject.crawl()** method

### utils.py
Helper function for print results and implement crawling with threding.

### Plot_vision.py
Create interactive plot usig **mol3d** module.

### main.py 
The main which need to run to for crawling.

### figure1
the result of crawling among all url's



## Dependencies
Python 3.8 <br> <br>

BeautifulSoup <br>
collections <br>
matplotlib <br>
threading <br>
requests <br>
networkx <br>
random <br>
pandas <br>
urllib <br>
pprint <br>
mpld3 <br>
numpy <br>
time <br>
re <br>


## Results Example
shown in figure1.html (download and open the file in **Chrome**)
