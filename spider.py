from urllib import request
from bs4 import BeautifulSoup

def get_paragraph(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
	}
	page = request.Request(url, headers=headers)
	page_info = request.urlopen(page).read().decode('utf-8')
	soup = BeautifulSoup(page_info, 'html.parser')
	titles = soup.find_all('h1', '')
	paragraphs = soup.find_all('p', '')
	result = '********\n'
	for title in titles:
		result += title.string + '\n'
	result += '\n'
	for para in paragraphs:
		if para.string:
			result += para.string + '\n'
	result += '********\n'
	print(len(titles), len(paragraphs))
	return result


def get_book():
	url_template = "http://www.mossiella.com/html/"
	for index in range(88978, 98978, 2):
		result = ''
		cur_url = url_template + str(index) + '.html'
		result += get_paragraph(cur_url)
		print(index)
		with open(r'gt.txt', 'a') as file:
			file.write(result)

if __name__ == '__main__':
	get_book()


