import urllib
import re, itertools,csv
import urllib.request
from urllib.error import URLError, HTTPError, ContentTooShortError
from bs4 import BeautifulSoup
import math
import pandas as pd
#first we need to download the web pages there may be some error occure then we need to retry as many times we want
from xml.etree.ElementTree import fromstring
output_rows = []
def download(url, user_agent='wswp', num_retries=2, charset='utf-8'):  #adding agent wswp defualt was Python-urllib/3.x
	print('Downloading:', url)
	request = urllib.request.Request(url)
	request.add_header('User-agent', user_agent)
	try:
		resp = urllib.request.urlopen(request)     #e will use a simpleregular expression to extract URLs within the <loc> tags.
		cs = resp.headers.get_content_charset()
		if not cs:
			cs = charset
		html = resp.read().decode(cs)
	except (URLError, HTTPError, ContentTooShortError) as e:
		print('Download error:', e.reason)
		html=None
		if(num_retries>0):
			if hasattr(e, 'code') and 500 <= e.code < 600:
				download(url,num_retries-1)     # recursively retry 5xx HTTP errors

	return html

def scrapdata(html):
	soup = BeautifulSoup(html, features="html.parser")
	# locate the area row
	# tr = soup.find(attrs={'class':'oyo-row oyo-row--no-spacing ListingHotelCardWrapper'})  #class="oyo-row oyo-row--no-spacing ListingHotelCardWrapper"
	content = soup.find_all(attrs={'class': 'oyo-cell--12-col oyo-cell--8-col-tablet oyo-cell--4-col-phone'})  # class="oyo-cell--12-col oyo-cell--8-col-tablet oyo-cell--4-col-phone"
	# getting information from a single page now and printing that.
	for cont in content:
		output_row = []
		distance = cont.find(attrs={'class': 'listingHotelDescription__distanceText'})  # class="listingHotelDescription__distanceText"
		output_row.append(distance.text.encode('utf-8'))
		rating=cont.find(attrs={'class': 'hotelRating'})
		output_row.append(rating.text.encode('utf-8'))
		price = cont.find(attrs={'class': 'oyo-cell--12-col listingHotelDescription__priceBtn'})  # listingPrice__finalPrice
		output_row.append(price.text[:5].encode('utf-8'))
		address = cont.find(attrs={'class': 'd-body-lg listingHotelDescription__hotelAddress'})  # d-body-lg listingHotelDescription__hotelAddress
		output_row.append(address.text.encode('utf-8'))
		output_rows.append(output_row)


def crawl_sitemap(url, max_errors=1):
	#this crawler needs 5 consecutive errors to failed downloading
	max_url='{}{}'.format(url, 500)
	new_html=download(max_url)
	soup = BeautifulSoup(new_html, features="html.parser")
	content = soup.find(attrs={'class': 'ListingContentHeader__h1'})
	maximum_pages=int(''.join(filter(str.isdigit, content.text)))/20
	#if(math.ceil(maximum_pages)!=math.floor(maximum_pages)):
		#maximum_pages += 1
	maximum_pages=math.floor(maximum_pages)
	for page in range(1,maximum_pages+1):
		pg_url = '{}{}'.format(url, page)
		html = download(pg_url)
		#print(pg_url)
		if html is None:
			num_errors += 1
			if num_errors == max_errors:  # max errors reached, exit loop
				break
		else :
			scrapdata(html)
			num_errors=0
	f = open('scrape.csv', 'w')
	csv_writer = csv.writer(f)
	for i in output_rows:
		csv_writer.writerow(i)
	f.close()
		# success - can scrape the resul
crawl_sitemap("https://www.oyorooms.com/hotels-in-bangalore/?page=")

