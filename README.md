androidstring2dict
==================
收集Android项目中组件中特定语言的字符串数据，到词典中。另外提供
1、根据字典中的词条更新 .po文件。
2、导出词条到Excel表格中
3、从Excel表格中导入词条到词典中
目的：统一收集Android字符串数据到一起，方便翻译后,统一导入


安装要求:
-------
需要安装以下Python模块，当然他们大部分都能自动安装，请参考各自的安装说明
babel >= 1.0dev (only the dev version has support for contexts)
http://babel.edgewall.org/
lxml
http://codespeak.net/lxml/
argparse
http://argparse.googlecode.com/
a2po
https://github.com/huzhennan/android2po
openpyxl
http://pythonhosted.org/openpyxl/

使用
~~~
* 从现有的Android代码中导出所有的字符串到词典中。
  配置所需要导出的组件子路径，在androidstring2dict/config.py。
  $ as2d.py init -dictionary DICTIONARY -language LANGUAGE
  DICTIONARY: 生成词典的文件名
  LANGUAGE： 所需要的国际语言代码，如中文：zh_CN 德文: de 

* 从词典中导出词条到Excel表格中
  $ cd android_root_dir_directory
  $ as2d.py export -dictionary DICTIONARY -excelfile EXCELFILE [--all][--isnone]
  DICTIONARY: 指定词典文件
  EXCELFILE: 指定Excel表格文件
  --all 导出所有的词条
  --isnone 导出没有值的词条

* 从Excel表格导入词条到词典中
  $ as2d.py import -dictionary DICTIONARY -excelfile EXCELFILE
    	    [-keycolumn KEY_COLUMN] [-valuecolumn VALUE_COLUMN]
  DICTIONARY: 指定词典文件
  EXCELFILE： 指定Excel表格文件
  --keycolumn 指定英文字符在第几列，默认为0,第一列
  --valuecolumn 指定对应语言字符串在第几列，默认为1，第二列

* 生成新的词典后，生成新的.po文件.
  由于使用a2po导入后,xml里的字符串没有双引号，不利于对比。因此只生成到.po文件
  $ androidstring2dict init 会调用a2po init生成对应的.po文件在android组件目录下
  的子目录local下，如 package/app/Gallery/local下。
  $ as2d.py generate [-h] -dictionary DICTIONARY -language LANGUAGE
  DICTIONARY: 指定词典文件
  LANGUAGE: 指定语言
  as2d.py generate会生成.po文件在android组件目录下的子目录generate下。

* 对应local目录和generate目录下的.po文件，确认无误后，使用
  $ a2po import --android RES_DIR --gettext PO_DIR
  RES_DIR: Android 资源目录($PROJECT/res)
  PO_DIR: 包含.po文件的目录