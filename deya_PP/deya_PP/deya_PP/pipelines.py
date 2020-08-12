# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pandas as pd
import os
import pymysql

from deya_PP.settings import PP_AIM_FILE, PE_AIM_FILE
from deya_PP.tools import gen_temp_file, gen_aim_file, gen_excel_and_sheet, send_email


class DeyaPpPipeline(object):

    def __init__(self, host, port, user, password, database, charset):
        self.today = datetime.date.today()
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get("HOST"),
            port=crawler.settings.get("PORT"),
            user=crawler.settings.get("USER"),
            password=crawler.settings.get("PASSWORD"),
            database=crawler.settings.get("DATABASE"),
            charset=crawler.settings.get("CHARSET")
        )

    def open_spider(self, spider):
        self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database, charset=self.charset)
        self.cursor_for_insert = self.conn.cursor()
        self.cursor_for_query = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
        # PP
        if len(item['title']) == 5:
            self.cursor_for_query.execute("select specifications_name, category from specification_comparison where type=0")
            num_type = self.cursor_for_query.fetchall()
            pp_middle_file_name, pp_origin_excel, pp_origin_excel_sheet = gen_excel_and_sheet("PP", self.today)
            df = gen_temp_file(item, pp_middle_file_name)
            additional_content = list(pd.read_excel('爬虫-PP.xlsx', sheet_name='Sheet1', index_col=False)['石化名称备注'])
            gen_aim_file(additional_content, df, pp_origin_excel_sheet.max_column, pp_origin_excel, pp_origin_excel_sheet, PP_AIM_FILE, num_type, self.cursor_for_insert, self.conn, 0)

        # PE
        if len(item['title']) == 7:
            self.cursor_for_query.execute("select specifications_name, category from specification_comparison where type=1")
            num_type = self.cursor_for_query.fetchall()
            pe_middle_file_name, pe_origin_excel, pe_origin_excel_sheet = gen_excel_and_sheet("PE", self.today)
            df = gen_temp_file(item, pe_middle_file_name)
            additional_content = list(pd.read_excel('爬虫备注-PE排产 (1).xlsx', sheet_name="Sheet1", index_col=False)['企业名称备注2'])
            gen_aim_file(additional_content, df, pe_origin_excel_sheet.max_column, pe_origin_excel, pe_origin_excel_sheet, PE_AIM_FILE, num_type, self.cursor_for_insert, self.conn, 1)
        return item

    def close_spider(self, spider):
        self.cursor_for_insert.close()
        self.cursor_for_query.close()
        self.conn.close()
        file_path_list = []
        if os.path.exists(PP_AIM_FILE):
            file_path_list.append(PP_AIM_FILE)
        if os.path.exists(PE_AIM_FILE):
            file_path_list.append(PE_AIM_FILE)
        send_email(file_path_list)
        if len(file_path_list) > 0:
            for f in file_path_list:
                os.remove(f)
