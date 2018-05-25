# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import hkexnews.settings as settings


class HkexnewsPipeline(object):

    def __init__(self):
        print '~~~~~'
        self.conn = MySQLdb.connect(settings.HOST, settings.USER, settings.PASSWD, 
                                    settings.DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):    
        try:
            self.cursor.execute("""INSERT INTO hkexnews(code, name,mount,percent)  
                        VALUES (%s, %s,%s,%s)""", 
                       (item['code'].encode('utf-8'), 
                        item['name'].encode('utf-8'),
                        item['mount'].encode('utf-8'),
                        item['percent'].encode('utf-8')
                        ))            
            self.conn.commit()            
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
        return item


