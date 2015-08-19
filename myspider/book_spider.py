#!/usr/bin/evn python
#-*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import time
import requests
from bs4 import BeautifulSoup

import MySQLdb

file_name = 'book.txt'
file_content=''
file_content += '生成时间：'+time.asctime()


class spiderdb:

	""" MySqL """

	conn = ''
	cursor = ''

	def __init__(self, dbhost='127.0.0.1', dbport='3306', dbuser='root',
				dbpasswd='123456', db='spiderdb', charset='utf8'):

		""" MySQL Database initialization """

		try:
			self.conn = MySQLdb.connect(dbhost, dbuser, dbpasswd, db)
		except Exception, e:
			print e
			sys.exit()


		self.cursor = self.conn.cursor()
			
		self.conn.set_character_set('utf8')
		"""
		self.cursor.execute('set names utf8;')
		self.cursor.execute('set character set utf8;')
		self.cursor.execute('set character_set_connection=utf8;')
		"""
	def selectcount(self, table, wherename, wherevalue):
		
		""" select count query """
	
		sql = "select count(0) from %s where %s = '%s' " % (table, wherename, wherevalue)
		
		try:
			self.cursor.execute(sql)
		except Exception, e:
			print e
			sys.exit()
		results = self.cursor.fetchone();
		print "%d" %results
		return "%d" %results
	
	def query(self, sql):
	
		""" Execute SQL statement """
		
		return self.cursor.execute(sql)


	def insertData(self, table, title, rating, authorinfo, pubinfo):

		""" INSERT DATA to MySQL """

		sql = "insert into %s (bookname, authorinfo, pubinfo, rating) \
			values('%s', '%s', '%s', '%s')" %(table, title, authorinfo,
			pubinfo, rating)
		try:
			self.cursor.execute(sql)
			self.conn.commit()
		except Exception, e:
			sys.exit()
	

	def __del__(self):

		""" Terminate the connection """
	
		if self.conn != '':
			self.conn.close()

		if self.cursor != '':
			self.cursor.close()


def book_spider(book_tag):
	global file_content
	
	spid = spiderdb('127.0.0.1', '3306', 'root', '123456', 'spiderdb', 'utf8')

	url = "http://www.douban.com/tag/%s/book" % book_tag
	print url;
	source_code = requests.get(url, timeout=10)
	print "url get is ok"
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text)
	
	title_divide = '\n' + '--' * 30 + '\n' + '--' * 30 + '\n'
	file_content += title_divide + '\t' * 4 + book_tag + ':' + title_divide

	count = 1

	list_soup = soup.find('div', {'class':'mod book-list'})

	for book_info in list_soup.findAll('dd'):
		title = book_info.find('a', {'class':'title'}).string.strip()

		desc=book_info.find('div', {'class':'desc'}).string.strip()
		desc_list = desc.split('/')

		author_info = '作者/译者:' + '/'.join(desc_list[0:-3])
		pub_info = '出版信息:' + '/'.join(desc_list[-3:])

		rating = book_info.find('span', {'class':'rating_nums'}).string.strip()
		
		if spid.selectcount('spi_bookinfo', 'bookname', title) <= 0 :
			spid.insertData('spi_bookinfo', title, rating, author_info, pub_info)

		file_content +="*%d\t《%s》\t评分：%s\n\t%s\n\t%s\n\n" % (count, title, rating, author_info, pub_info)
		count += 1

book_lists = ['人物传记']

def do_spider(book_lists):
	for book_tag in book_lists:
		book_spider(book_tag)


if __name__ == '__main__':
	do_spider(book_lists)

	f = open(file_name, 'w')
	if f is None: 
		sys.exit()
	f.write(file_content)
	f.close()
