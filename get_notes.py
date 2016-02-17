import httplib2

DOUBAN_HEADER = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
  'Origin':'http://book.douban.com',
};

class DoubanFetcher():
	def __init__(self, book_name):
		self.book_name = book_name

	def get_notes(self):
		self.book_id = self.get_book_id()

	def get_book_id(self):
		url = 'http://www.douban.com/search?cat=1001&q=' + self.book_name
		req = httplib2.Request(url, None, DOUBAN_HEADER)	
		response = urllib2.urlopen(req).read()
		start_index = response.find('book.douban.com%2Fsubject')
		content = response[start_index:]
		end_index = content.find('%2F')
		print content[:end_index]
		return content[:end_index]

def get_notes(book_name):
	douban_fetcher = new DoubanFetcher(book_name)
	douban_fetcher.get_notes()
	return []