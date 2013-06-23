
from argparse import Namespace
import unittest
from androidstring2dict.commands import InitCommand, GenerateCommand, ImportCommand, ExportCommand

class TestCommand(unittest.TestCase):

    def testInitCommmad(self):
        options = Namespace(dictionary='test_initcommand.dict', language='zh_CN')
        InitCommand(options).execute()


    def testGenerateCommand(self):
        options = Namespace(dictionary='test_initcommand.dict', language='zh_CN')
        GenerateCommand(options).execute()

    def testImportCommand(self):
        options = Namespace(dictionary='test_initcommand.dict',
                            excelfile='/home/hzn/PycharmProjects/androidstring2dict/tests/test_import.xlsx',
                            key_column=0, value_column=1)
        ImportCommand(options).execute()

    def testExportCommandAll(self):
        options = Namespace(dictionary='test_initcommand.dict',
                            excelfile='/home/hzn/PycharmProjects/androidstring2dict/tests/test_export_all.xlsx',
                            all=True, isnone=False)
        ExportCommand(options).execute()

if __name__ == '__main__':
    unittest.main()
