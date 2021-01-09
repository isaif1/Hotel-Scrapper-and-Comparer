from lxml.html import fromstring, tostring
import urllib
import urllib.request
from lxml.cssselect import CSSSelector
from cssselect import GenericTranslator, SelectorError
from lxml import etree

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


html = download('https://www.oyorooms.com/hotels-in-bangalore/?page=1')
tree = etree.parse(html)
tre = fromstring(tree)
tr=tre.xpath('//div[@class="hotelRating"]')
print(etree.tostring(tr))
#content = tree.find_all(attrs={'class': 'oyo-cell--12-col oyo-cell--8-col-tablet oyo-cell--4-col-phone'})
"""for cont in content:
    distance = cont.find(attrs={'class': 'listingHotelDescription__distanceText'})  # class="listingHotelDescription__distanceText"
    rating=cont.find(attrs={'class': 'hotelRating'})
    price = cont.find(attrs={'class': 'oyo-cell--12-col listingHotelDescription__priceBtn'})  # listingPrice__finalPrice
    address = cont.find(attrs={'class': 'd-body-lg listingHotelDescription__hotelAddress'})  # d-body-lg listingHotelDescription__hotelAddress
    print('{} {} {}'.format())"""
#tr=tree.xpath('//div[@class="hotelRating"]').text_content()
#print(tr.tag)
#print(td)