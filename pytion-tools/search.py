import os
import argparse
import multiprocessing
from multiprocessing import Pool

def thread_arg_type(string):
    value = int(string)
    if value < 0:
        msg = "無効なスレッド数(%d)" % string
        raise argparse.ArgumentTypeError(msg)
    return value

parser = argparse.ArgumentParser(description='マルチスレッドなファイル検索')
parser.add_argument('search', required=True, help='検索する名前') # 必須
parser.add_argument('-t', '--thread', type=thread_arg_type,default=0, help='スレッド数(0=自動,1=シングルモード,デフォルト=0)')
args = parser.parse_args() # コマンドラインの引数を解釈します

def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)
def in_list(string,list):
    for d in list:
        if string.endswith(d):
            return True
    return False
def show_list(path):
	path = path.replace(os.path.sep, '/')
	path = path.decode("utf-8")
	isInList = in_list(path, args.search)
	if os.path.isdir(path):
		return
	if isInList:
		print('found = ' + path)
	else:
		print('not found = ' + path)
if __name__ == "__main__":
    if args.thread == 1:
        print ('start single-thread mode')
        for file in fild_all_files( args.srcDir ):
            show_list(file)
    else :
        thread = 0
        cpu_count = multiprocessing.cpu_count()
        if args.thread == 0:
            thread = cpu_count
        else:
            thread = args.thread
        print ('start match-thread mode (%d thread / %d CPU)' % (thread,cpu_count))
        p = Pool(thread)
        p.map(show_list,  fild_all_files( args.srcDir ))
