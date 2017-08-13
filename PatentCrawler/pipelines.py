# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from config.BaseConfig import BaseConfig
from util.excel.ExcelUtil import ExcelUtil


class PatentcrawlerPipeline(object):

    LINE_INDEX = 1

    def process_item(self, item, spider):
        if self.checkForInventor(item):
            if self.checkForProposer(item):
                print(item.items())
                self.writeToExcel(item)
        return item

    def writeWithNotNone(self, sh, i, strData):
        if strData == None or strData == "None":
            sh.write(self.LINE_INDEX, i, "")
        else:
            sh.write(self.LINE_INDEX, i, strData)

    def writeToExcel(self, item):
        try:
            editor = ExcelUtil(BaseConfig.FILE_NAME).edit()
            sh = editor.getSheet(0)
            self.writeWithNotNone(sh, 0, item.get('patentType'))
            self.writeWithNotNone(sh, 1, item.get('name'))
            self.writeWithNotNone(sh, 2, item.get('lawState'))
            self.writeWithNotNone(sh, 3, item.get('lawStateDate'))
            self.writeWithNotNone(sh, 4, item.get('publishNumber'))
            self.writeWithNotNone(sh, 5, item.get('publishDate'))
            self.writeWithNotNone(sh, 6, item.get('requestNumber'))
            self.writeWithNotNone(sh, 7, item.get('requestDate'))
            self.writeWithNotNone(sh, 8, item.get('proposerName'))
            self.writeWithNotNone(sh, 9, item.get('inventorName'))
            self.writeWithNotNone(sh, 10, item.get('ipcNumber'))
            self.writeWithNotNone(sh, 11, item.get('agent'))
            self.writeWithNotNone(sh, 12, item.get('agency'))
            self.writeWithNotNone(sh, 13, item.get('locarnoNumber'))
            editor.commit()
            PatentcrawlerPipeline.LINE_INDEX += 1
        except Exception as e:
            print("写excel报错")

    def checkForInventor(self, item):
        if BaseConfig.CHECK_INVENTOR is False:
            return True
        targetInventor = item.get('targetInventor')
        inventorList = item.get('inventorName').split(";")
        for i in inventorList:
            if targetInventor == i.strip():
                return True
        return False

    def checkForProposer(self, item):
        if BaseConfig.CHECK_PROPOSER is False:
            return True
        targetProposer = item.get('targetProposer')
        proposerList = item.get('proposerName').split(";")
        for p in proposerList:
            if targetProposer == p.strip():
                return True
        return False
