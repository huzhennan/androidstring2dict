#!/usr/bin/env python
# encoding: utf8

import os
from contextlib import closing
from translate_dict import TranslateDict
from config import Android_Component_SubPath
from android2po import program
from re import match
from babel.messages import pofile

RES_DIR = 'res'
VALUES_DIR = 'values'
LOCAL_DIR = 'local'
GENERATE_DIR = 'generate'

def language_po_file_type(language_code):
    return r'(.)*%s.po$' % language_code

def read_catalog(filename, **kwargs):
    """ Helper to read a catalog from a .po file.
    """
    file = open(filename, 'rb')
    try:
        return pofile.read_po(file, **kwargs)
    finally:
        file.close()

def write_catalog(filename, catalog, **kwargs):
    """ Helper to write a catalog to a .po file.
    """
    f = open(filename, 'wb')
    try:
        return pofile.write_po(f, catalog, **kwargs)
    finally:
        f.close()

class Command(object):
    """Abstract base command class.
    """

    @classmethod
    def setup_arg_parser(cls, argparser):
        """A command should register it's sub-arguments here  with the
        given argparser instance
        """

    def execute(self):
        raise NotImplementedError()

class InitCommand(Command):
    """
    The init command;
    """

    def __init__(self, namespace):
        self.language = namespace.language
        self.dictionary = namespace.dictionary

    @classmethod
    def setup_arg_parser(cls, parser):
        parser.add_argument('-dictionary', help="specify a dictionary's file path.", required=True, )
        parser.add_argument('-language', help='specify language code to initialize.', required=True)

    def execute(self):
        cur_path = os.getcwd()
        with closing(TranslateDict(self.dictionary)) as dic:
            for subpath in Android_Component_SubPath:
                model_path = os.path.join(cur_path, subpath)
                res_path = os.path.join(model_path, RES_DIR)
                values_path = os.path.join(model_path, VALUES_DIR)

                local_path = os.path.join(model_path, LOCAL_DIR)
                print local_path
                if not os.path.exists(local_path):
                    os.mkdir(local_path)

                program.main(('just_do_it', 'init', '--android', res_path,
                             '--gettext', local_path, 'language', self.language))

                args = {'language_code':self.language, 'dict':dic}
                os.path.walk(local_path, self._visit_po_file, args)


    def _visit_po_file(self, args, dirname, names):
        language_code = args['language_code']
        filename_pattern = language_po_file_type(language_code)
        dic = args['dict']

        for name in names:
            po_file_path = os.path.join(dirname, name)
            if os.path.isfile(po_file_path) and match(filename_pattern, name):
                self._update_po_content2dict(po_file_path, language_code, dic)

    def _update_po_content2dict(self, filename, local_code, dic):

        catalog = read_catalog(filename, locale=local_code)
        for msg in catalog:
            if not msg.id and not msg.context:
                continue

            if isinstance(msg.id, unicode):
                member_key = (msg.id).encode("utf-8")
            elif isinstance(msg.id, tuple) and len(msg.id) == 2:
                member_key = ("::".join(msg.id)).encode("utf-8")
            else:
                member_key = ""


            if isinstance(msg.string, unicode):
                member_value = msg.string
            elif isinstance(msg.string, tuple):
                member_value = "::".join(msg.string)
            else:
                member_value = u""

            dic[member_key] = member_value

class GenerateCommand(Command):

    def __init__(self, namespace):
        self.language = namespace.language
        self.dictionary = namespace.dictionary

    @classmethod
    def setup_arg_parser(cls, parser):
        parser.add_argument('-dictionary', help="specify a dictionary's file path.", required=True, )
        parser.add_argument('-language', help='specify language code to generate.', required=True)

    def execute(self):
        cur_path = os.getcwd()
        with closing(TranslateDict(self.dictionary)) as dic:
            for subpath in Android_Component_SubPath:
                model_path = os.path.join(cur_path, subpath)
                local_path = os.path.join(model_path, LOCAL_DIR)
                generate_path = os.path.join(model_path, GENERATE_DIR)
                if not os.path.exists(generate_path):
                    os.mkdir(generate_path)

                args = {'language_code':self.language, 'dict':dic, 'new_pofile_path':generate_path}
                os.path.walk(local_path, self._generate_po_file, args)

    def _generate_po_file(self, args, dirname, names):
        language_code = args['language_code']
        filename_pattern = language_po_file_type(language_code)
        dic = args['dict']
        generate_path = args['new_pofile_path']

        for name in names:
            po_file_path = os.path.join(dirname, name)
            if os.path.isfile(po_file_path) and match(filename_pattern, name):
                new_pofile_path = os.path.join(generate_path, name)
                self._update_po_content2new_pofile(po_file_path, new_pofile_path, language_code, dic)

    def _update_po_content2new_pofile(self, pofile_path, new_pofile_path, language_code, dic):
        catalog = read_catalog(pofile_path, locale=language_code)

        for msg in catalog:
            if not msg.id and not msg.context:
                continue

            if isinstance(msg.id, unicode):
                member_key = (msg.id).encode("utf-8")
                member_value = msg.string
                if dic.has_key(member_key):
                    value_from_dic = dic.get(member_key)
                    if not isinstance(value_from_dic, (str, unicode)):
                        value_from_dic = unicode(value_from_dic)

                    if (cmp(value_from_dic, u"") != 0) and (cmp(value_from_dic, member_value) != 0):
                        msg.string = value_from_dic
                    catalog[msg.id] = msg
            elif isinstance(msg.id, tuple):
                member_key = ("::".join(msg.id)).encode("utf-8")
                member_value = msg.string
                if dic.has_key(member_key):
                    value_from_dic = dic.get(member_key)
                    if isinstance(value_from_dic, (str, unicode)):
                        value_from_dic = value_from_dic.split("::")
                    else:
                        value_from_dic = unicode(value_from_dic)

                    if cmp(value_from_dic, u"") != 0 and cmp(value_from_dic, member_value) != 0:
                        msg.string = value_from_dic

                    catalog[msg.id] = msg

        write_catalog(new_pofile_path, catalog)

class ImportCommand(Command):
    def __init__(self, namespace):
        self.dictionary = namespace.dictionary
        self.excelfile = namespace.excelfile
        self.key_column = namespace.key_column
        self.value_column = namespace.value_column

    @classmethod
    def setup_arg_parser(cls, parser):
        parser.add_argument('-dictionary',
                            help="specify a dictionary's file path.", required=True)
        parser.add_argument('-excelfile',
                            help='specify excel file path', required=True)
        parser.add_argument('-keycolumn',
                            help="specify in excel file, the key's column",
                            type=int, default=0, dest='key_column')
        parser.add_argument('-valuecolumn',
                            help="specify in excel file, the value's column",
                            type=int, default=1,
                            dest='value_column')

    def execute(self):
        with closing(TranslateDict(self.dictionary)) as dic:
            dic.import_from_excel(self.excelfile, self.key_column, self.value_column)

            return dic



class ExportCommand(Command):
    def __init__(self, namespace):
        self.dictionary = namespace.dictionary
        self.excelfile = namespace.excelfile
        self.all= namespace.all
        self.isnone = namespace.isnone

    @classmethod
    def setup_arg_parser(cls, parser):
        parser.add_argument('-dictionary',
                            help="specify a dictionary's file path.", required=True)
        parser.add_argument('-excelfile',
                            help='specify excel file path', required=True)

        group = parser.add_mutually_exclusive_group()

        group.add_argument('--all', help='specify whether export all itmes.',
                            action='store_true')
        group.add_argument('--isnone', help='specify whether exort items which is None',
                           action='store_true')

    def execute(self):
        with closing(TranslateDict(self.dictionary)) as dic:
            dic.export_all_items(self.excelfile)