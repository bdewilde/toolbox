import bs4
import csv
import re
import requests


USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11'
BASE_URL = 'http://www.boxofficemojo.com/movies'

def get_film_weekly_box_office(film_id) :

	url = BASE_URL + '/?page=weekly&id=' + film_id + '.htm'
	response = requests.get(url, headers={'User-agent':USER_AGENT})
	print 'URL:', response.url

	soup = bs4.BeautifulSoup(response.text)
	body = soup.find('body')
	tables = body.find_all('table', class_='chart-wide')
	for table in tables :
		trs = table.find_all('tr')
		for tr in trs :
			tds = tr.find_all('td')
			row = []
			for td in tds :
				text = ' '.join(td.find_all(text=True))
				text = re.sub(' \(click to view chart\)', '', text)
				text = re.sub('\x96', '_', text)
				text = re.sub('\$|%|,', '', text)
				if re.search(' / ', text) is not None :
					text = re.split(' / ', text)
					row.extend(text)
					continue
				row.append(text)
			f_csv.writerow(row)

docs = [
	'Forks Over Knives',
	'The Waiting Room',
	'Unknown White Male',
	'Under Our Skin',
	'Escape Fire',
	'The Business of Being Born',
	'Living in Emergency: Stories of Doctors without Borders',
	'So Much So Fast',
	'A Walk to Beautiful',
	'Sicko'
	]

doc_ids = [
	'forksoverknives',
	'waitingroom',
	'unknownwhitemale',
	'underourskin',
	'escapefire',
	'businessofbeingborn',
	'livinginemergency',
	'somuchsofast',
	'walktobeautiful',
	'sicko'
	]

for doc_id in doc_ids :
	f_out = open('box_office_mojo_' + doc_id + '.txt', 'w')
	f_csv = csv.writer(f_out, delimiter="\t")
	get_film_weekly_box_office(doc_id)
	f_out.close()