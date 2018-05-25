# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import hkexnews.settings as settings
from datetime import datetime,date,timedelta

class HkexnewsPipeline(object):

    def __init__(self):
        self.conn = MySQLdb.connect(settings.HOST, settings.USER, settings.PASSWD, 
                                    settings.DBNAME, charset="utf8",
                                    use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):    
        #try:
        #    self.cursor.execute("""INSERT INTO hkexnews(code, name,mount,percent)  
        #                VALUES (%s, %s,%s,%s)""", 
        #               (item['code'].encode('utf-8'), 
        #                item['name'].encode('utf-8'),
        #                item['mount'].encode('utf-8'),
        #                item['percent'].encode('utf-8')
        #                ))            
        #    self.conn.commit()            
        #except MySQLdb.Error, e:
        #    print "Error %d: %s" % (e.args[0], e.args[1])

        day_items = self.get_top_items_by_day()
        week_items = self.get_top_items_by_week()
        month_items = self.get_top_items_by_month()
        print day_items
        print week_items
        print month_items
        return item


    def get_top_items_by_day(self):
      today = date.today()
      yesterday = date.today() - timedelta(1)
      today_cursor = self.cursor.execute("""select name,code,mount,percent from hkexnews where createtime = '%s'""" % today)
      today_items = self.cursor.fetchall()

      yes_cursor = self.cursor.execute("""select name,code,mount,percent from hkexnews where createtime = '%s'""" % yesterday)
      yes_items = self.cursor.fetchall()
      return self.get_top(today_items,yes_items)



    def get_top_items_by_week(self):
      today = date.today()
      last_week = date.today() - timedelta(7)
      today_cursor = self.cursor.execute("""select name,code,mount,percent from hkexnews where createtime = '%s'""" % today)
      today_items = self.cursor.fetchall()

      yes_cursor = self.cursor.execute("""select name,code,mount,percent from hkexnews where createtime = '%s'""" % last_week)
      yes_items = self.cursor.fetchall()
      return self.get_top(today_items,yes_items)



    def get_top_items_by_month(self):
      today = date.today()
      last_month = date.today() - timedelta(30)
      today_cursor = self.cursor.execute("""select name,code,mount,percent from hkexnews where createtime = '%s'""" % today)
      today_items = self.cursor.fetchall()

      yes_cursor = self.cursor.execute("""select name,code,mount,percent from hkexnews where createtime = '%s'""" % last_month)
      yes_items = self.cursor.fetchall()
      return self.get_top(today_items,yes_items)


    def get_top(self,today_items,yes_items):

      minus_items = []
      for today_item in today_items:
        
        minus_mount = 0
        minus_percent = 0
        for yes_item in yes_items:
          if today_item[1] == yes_item[1]:
            print today_item[1]
            minus_mount = int(today_item[2].replace(',','')) - int(yes_item[2].replace(',',''))
            minus_percent = float(today_item[3].replace('%','')) - float(yes_item[3].replace("%",''))
        
        minus_items.append([today_item[0],today_item[1],today_item[2],today_item[3],minus_mount,minus_percent,date.today()])
      return  minus_items

