
import unittest
from unittest import TestCase
from androidstring2dict.translate_dict import TranslateDict
from contextlib import closing

class TestTranslateDict(TestCase):
    def setUp(self):
        pass

    def testTranslateDictAutoClose(self):
        with closing(TranslateDict('temp.dat')) as dic:
            #dic['test'] = 'test'
            pass

    def testExportHasNotValueToExFile(self):

        with closing(TranslateDict('temp.dat')) as dic:
            dic['key1'] = 'key1 value'
            dic['key2'] = 'key2 value'
            dic['key3'] = None
            dic.export_has_not_value('test.xlsx')

    def testExportAllItemsToExFile(self):
        with closing(TranslateDict('temp.dat')) as dic:
            dic['key1'] = 'key1 value'
            dic['key2'] = 'key2 value'
            dic['key3'] = None
            dic['key4'] = 5
            dic.export_all_items('test2.xlsx')

    def testImportItemsFromExFile(self):
        with closing(TranslateDict('temp.dat')) as dic:
            dic.import_from_excel('test_import.xlsx', 0, 1)

            self.assertTrue(dic.has_key('test_import'))

    def testExportAllItem(self):
        with closing(TranslateDict("/home/hzn/test.dict")) as dic:
            dic.export_all_items("/home/hzn/export_dict.xlsx")

    def tearDown(self):
        pass




if __name__ == '__main__':
    unittest.main()
