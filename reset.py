import os,shutil
os.rename('testfile/content.txt','content.txt')
os.remove('testfile/logs.json')
shutil.rmtree('testfile/versioning')