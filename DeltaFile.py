import os
import time
import json
import shutil 
class DeltaFile():
    def __init__(self,path,textFilePath,mode):
        if mode not in ['generator', 'reader']:
            raise ValueError('mod trebuie sa fie generator sau reader')
        self.path=path
        if mode=='generator':
            os.rename(textFilePath,path+'content.txt')
            os.makedirs(self.path+'versioning')
            shutil.copyfile(self.path+'content.txt',self.path+'versioning/v1.txt')
            modifiedTime=os.path.getmtime(self.path+'content.txt')
            self.__generate_log_file(modifiedTime)
            self.__listener()
        else:
            self.textFilePath=textFilePath

        
    def __generate_log_file(self,modifiedTime):        
        content={
            modifiedTime:"v1.txt"
        }
        self.__save_logs(content)
    
    def __get_logs(self):
        with open(self.path+'logs.json','r') as file: 
            content=json.load(file)
            return content
        
    def __save_logs(self,content):
        with open(self.path+'logs.json','w') as file:
            json.dump(content,file)

    def __generate_new_version(self,modifiedTime):
        versions=os.listdir(self.path+'versioning')
        maxVersion=max(versions).split('.')[0][1:]
        maxVersion=str(int(maxVersion)+1)
        shutil.copyfile('testfile/content.txt',f'testfile/versioning/v{maxVersion}.txt')
        content=self.__get_logs()
        content[modifiedTime]=f"v{maxVersion}.txt"
        self.__save_logs(content)

    def __listener(self):
       while True:
            print('In while')
            files=os.listdir(self.path)
            for file in files:
                if file.endswith('.txt'):
                        modifiedTime=os.path.getmtime(self.path+file)
                        if str(modifiedTime) not in self.__get_logs().keys():
                            self.__generate_new_version(modifiedTime)
                        else:
                            print('No changes!')
            time.sleep(3)
    
    
    def get_content(self, version=None, timestamp=None):
        '''functia va returna fisierul de la o anumita data ora specificata la apelarea functiei'''
        if version is not None:
            filepath=f'{self.path}versioning/v{version}.txt'
        else:
            if timestamp is not None:
                logs=self.__get_logs()
                keys=[key for key in logs.keys()]
                if timestamp<float(keys[0]):
                    print("timestamp este dinainte ca fisierul sa fi fost creat")
                if timestamp>float(keys[-1]):
                    filepath=self.path+logs[keys[-1]]
                for i in range(len(logs.keys()))-1:
                    if timestamp>float(keys[i]) and timestamp<float(keys[i+1]):
                        leftTimeStamp=keys[i]
                filepath=f"{self.path}versioning/{logs[leftTimeStamp]}"
            else:
                filepath=self.path+self.textFilePath
        try:
            with open(filepath, 'r') as file:
                content=file.read()
                return content
        except FileNotFoundError:
            return 'introduceti o versiune care sa existe'

myfile=DeltaFile('testfile/', 'content.txt', 'reader')
print(myfile.get_content(version=2))
