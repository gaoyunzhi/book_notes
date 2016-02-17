import urllib2, time, random

DOUBAN_HEADER = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
  'Origin':'http://book.douban.com',
};

class DoubanFetcher():
	def __init__(self, book_name):
		self.book_name = book_name

	def get_notes(self):
		self.book_id = self.get_book_id()
		self.note_link = 'http://book.douban.com/subject/' + \
		 	self.book_id + '/annotation?sort=rank&start='
		for i in xrange(0, 10):
			start = str(10 * i)
			notes = self.get_note_from_page(self.note_link + start)
			num = 0
			for note in notes:
				num += 1
				yield note
			if num < 10:
				break

	def get_book_id(self):
		url = 'http://www.douban.com/search?cat=1001&q=' + self.book_name
		req = urllib2.Request(url, None, DOUBAN_HEADER)	
		response = urllib2.urlopen(req).read()
		start_index = response.find('book.douban.com%2Fsubject')
		content = response[start_index + 28:]
		end_index = content.find('%2F')
		return content[:end_index]

	def get_note_from_page(self, link):
		time.sleep(random.randint(1, 5))
		req = urllib2.Request(link, None, DOUBAN_HEADER)
		response = urllib2.urlopen(req).read()
		anchor = 'div class="reading-note"'
		anchor_index = response.find(anchor)
		while anchor_index != -1:
			text_anchor = '<div class="all hidden" style="display:none" >'
			start_index = response.find(text_anchor, anchor_index) + len(text_anchor)
			text_end_anchor = '<div class="col-rec-con clearfix">'
			end_index = response.find(text_end_anchor, start_index)
			yield response[start_index: end_index]
			anchor_index = response.find(anchor, end_index)

def get_notes(book_name):
	douban_fetcher = DoubanFetcher(book_name)
	notes = douban_fetcher.get_notes()
	return notes