import os
import time
import json
import shutil 
class DeltaFile():
    def __init__(self,path,textFilePath):
        self.path=path
        os.rename(textFilePath,path+'content.txt')
        os.makedirs(self.path+'versioning')
        shutil.copyfile(self.path+'content.txt',self.path+'versioning/v1.txt')
        modifiedTime=os.path.getmtime(self.path+'content.txt')
        self.__generate_log_file(modifiedTime)
        self.__listener()

        
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


DeltaFile('testfile/', 'content.txt')