import os

current_file = os.path.realpath(__file__)
current_directory = os.path.dirname(current_file)


regFile = open("./reg.reg", "w")
regFile.write('Windows Registry Editor Version 5.00\n')
regFile.write('[HKEY_CLASSES_ROOT\*\shell\Markdown Helper]\n')
regFile.write('@="markdown image uploader"\n')
regFile.write('[HKEY_CLASSES_ROOT\*\shell\Markdown Helper\command]\n')
regFile.write('@="\\"{}\\\\drag.cmd\\" \\"%1\\""'.format(os.path.normpath(current_directory).replace(os.path.sep, '\\\\')))
regFile.close()