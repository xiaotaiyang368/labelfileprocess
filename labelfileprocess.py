#This is a class to process labelme files.
#Version: V1.1
#1. You need to acticate your virtual environment of Labelme
#2. You need to set these parameters:
#   1)the directory of your json files(not availabel to set in version V1.0) :  json_file_dir
#   2)the directory of your origin pictures  :   origin_picture_dir
#   3)the destination directory to store your mask pictures:   des_mask_dir
#3. You need to put this file in the directory of your label json file with the 
#   origin picture in Version 1.0, and by default the folder stored the "label.png" would be deleted.

import os
import shutil
import json

    
class labelfileprocess():
    """A class to process the labelme files."""

    def __init__(self, json_file_dir=os.getcwd(), origin_picture_dir=os.getcwd(),
                 des_mask_dir=os.getcwd()):
        """Initial the parameter directories."""
        if (os.path.isdir(json_file_dir) and os.path.isdir(origin_picture_dir)
           and os.path.isdir(des_mask_dir)):
            self.json_file_dir = json_file_dir
            self.origin_picture_dir = origin_picture_dir
            self.des_mask_dir = des_mask_dir
        else:
            print("Please check your directories.")
            exit()

    def printdirectory(self):
        """Print the directories."""
        print("json directory: ", self.json_file_dir)
        print("origin picture directory: ", self.origin_picture_dir)
        print("destination mask directory: ", self.des_mask_dir)
        
    
    def jsonimgpath(self, json_file_dic):
        """Modify the imgpath in the labelme json file."""
        for jsonfile, file_id in json_file_dic.items():
            with open (jsonfile, 'r') as f_json:
                dic_json = json.load(f_json)
                #print(dic_json)
                dic_json["imagePath"] = self.origin_picture_dir + "\\" + dic_json["imagePath"]        

            with open (jsonfile, 'w') as w_json:
                json.dump(dic_json, w_json)

        
    
    
    
        
    def jsonfiledic(self):
        """Return json file list."""
        json_file_list = []
        json_file_dic = {}
        for jsonfile in os.listdir(self.json_file_dir):
            if 'json' in jsonfile:
                json_file_list.append(jsonfile)
            
        for json_dic_key in json_file_list:
            if '_' in json_dic_key:
                json_file_dic[json_dic_key] = json_dic_key.split('_')[0]          
            else:
                json_file_dic[json_dic_key] = json_dic_key[:-5]
        print(json_file_list)
        print(json_file_dic)
        return json_file_dic
        
    
    def labelfile(self, filename_dic):
        """Run the labelme commands."""
        labelme_command_pre = "labelme_json_to_dataset "
        for key, value in filename_dic.items():
            ###Run command labelme_jason_to_dataset to create the label.png
            os.system(labelme_command_pre + key + ' -o ' + key[0:-5] + "_json")
            ###Rename the label.png as picture_id.png
            mask_file_src = self.json_file_dir + "\\" + key[0:-5] + "_json\\" + "label.png"
            mask_file_rename = self.json_file_dir + "\\" + key[0:-5] + "_json\\" + value + "_m.png"
            os.rename(mask_file_src, mask_file_rename)
            ###Copy the picture_id.png to the destination directory.
            mask_file_des = self.des_mask_dir + "\\" + value + "_m.png"
            shutil.copyfile(mask_file_rename, mask_file_des)
            ###Delete the tmp folders, if you don't need to delete the folders, please comment this line.
            shutil.rmtree(key[0:-5] + "_json")
            

        
                

#test script
l = labelfileprocess(origin_picture_dir="C:\Kaggle\origin_fei", des_mask_dir = "C:\Kaggle\json\mask")
l.printdirectory()
m = l.jsonfiledic()
l.jsonimgpath(m)
l.labelfile(m)



