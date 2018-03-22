import requests
import re
import pymysql
from multiprocessing import Pool

def get_one_page(url):#判断是否get到网页信息
	res = requests.get(url)
	if res.status_code == 200:
		return res.text
	return None


def parse_one_page(html):#用正则表达式抓取
	pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
						 +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
						 +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
	items = re.findall(pattern,html)
	for item in items:
		yield {
			'index':item[0],
			'url':item[1],
			'name':item[2],
			'actors':item[3].strip()[3:],
			'time':item[4].strip()[5:],
			'score':item[5]+item[6]
		}


def save_detail(num,name,actors,time,score):#调用pymysql储存信息
	db = pymysql.connect('localhost','root','123456','maoyan_movies',charset='utf8')
	cursor = db.cursor()
	sql = 'insert into top100 values (%s,%s,%s,%s,%s)'
	cursor.execute(sql,(num,name,actors,time,score))
	db.commit()
	db.close()


def main(offset):
	url = 'http://maoyan.com/board/4?offset={0}'.format(offset)
	html = get_one_page(url)
	for i in parse_one_page(html):
		save_detail(i['index'],i['name'],i['actors'],i['time'],i['score'])


if __name__ == '__main__':
	offset = [i*10 for i in range(10)]#启用多线程
	pool = Pool()
	pool.map(main,offset)
