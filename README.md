# pythonProj

数据库表结构：
create table spi_bookinfo(
	`id`	int(11)  AUTO_INCREMENT,
	`bookname` varchar(64) NOT NULL,
	`authorinfo` varchar(64) NOT NULL,
	`pubinfo` varchar(128) NOT NULL,
	`rating`  varchar(12) DEFAULT '0',
	PRIMARY KEY (`id`)
)ENGINE=innodb default charset=utf8 auto_increment=1;
