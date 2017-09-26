# -*- coding: utf-8 -*-
import sys
from antlr4 import *
from AntlrLexer import AntlrLexer
from AntlrParser import AntlrParser
from AntlrListener import AntlrListener
import zipfile
import os
import codecs
import time
# from numba import jit
from timeit import timeit

def unzip_scratch(filename):
    """
    unzip scratch project and extract project.json file   
    :param filename: filename fo scratch project 
    :return: null or project.json content
    """
    zfile = zipfile.ZipFile(filename, 'r')
    if "project.json" in zfile.namelist():
        data = zfile.read("project.json")
        return data
    else:
        return None

def gen(argv):
    raw_json = unzip_scratch(argv)
    encoded_json = codecs.decode(raw_json, 'utf-8', 'strict')
    input = InputStream(encoded_json)
    if not input:
        return
    lexer = AntlrLexer(input)
    stream = CommonTokenStream(lexer)
    parser = AntlrParser(stream)
    tree = parser.json()
    walker = ParseTreeWalker()
    listener = AntlrListener()
    walker.walk(listener, tree)
    return listener.score, listener.hint
 
if __name__ == '__main__':
    during = timeit(stmt="gen(sys.argv[1])", setup="from Gen import gen;", number=1)
    print(during)