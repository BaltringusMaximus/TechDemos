from pTestGraph_v2 import f_graph_from_text
import os
import os.path
import sys
import time
import shutil
import msvcrt
from datetime import datetime
from pResFromTxtFile_v2 import f_str_res, f_get_barcode, f_get_order, f_get_alarm
str_date_today = datetime.today().strftime('%d%m%Y')
fol_txt_archive = 'C:\\pierre\\apps\\python apps\\graphgen\\fol_txt_archive\\'
fol_png_archive = 'C:\\pierre\\apps\\python apps\\graphgen\\fol_png_archive\\'
fol_hca_data = 'C:\\pierre\\apps\\python apps\\graphgen\\fol_hca_data\\'
fol_server = 'C:\\pierre\\apps\\python apps\\server\\'
sys.path.append(fol_txt_archive)
sys.path.append(fol_png_archive)
sys.path.append(fol_hca_data)
str_continue = "y"
while str_continue in ["y","Y","yes","Yes","YES","yES","yy","YY"]:
	dir = os.listdir()
	fol_G8_images = 'E:\\G8\\'+str_date_today+'\\'
	os.makedirs(fol_G8_images, exist_ok = True)
	for file in dir:
		if file[-4:] == ".txt":
			print(file)
			str_file_name = file
			with open(str_file_name,"r") as current_txt_file:
				txt_file = current_txt_file.read()
			path_to_save_hca = os.path.join(fol_hca_data,str_file_name[:-4]+'_hca_data.txt')
			path_to_server = os.path.join(fol_server,str_file_name[:-4]+'_hca_msg.txt')
			try:
				print("generating graph",str_file_name)
				f_graph_from_text(str_file_name)
				shutil.copy2(file,fol_txt_archive)
				shutil.copy2(file[:-4]+'_x1.png',fol_G8_images)
				shutil.copy2(file[:-4]+'_x10.png',fol_G8_images)
				shutil.copy2(file[:-4]+'_x100.png',fol_G8_images)
				shutil.copy2(file[:-4]+'_x1.png',fol_png_archive)
				shutil.copy2(file[:-4]+'_x10.png',fol_png_archive)
				shutil.copy2(file[:-4]+'_x100.png',fol_png_archive)
				with open(path_to_save_hca,"w") as saved_hca_file:
					saved_hca_file.write(f_get_order(file)+"\n"+f_get_barcode(file)+"\n"+f_str_res(file)+"\n"+f_get_alarm(file))
				with open(path_to_server,"w") as hca_msg_file:
					hca_msg_file.write(f_get_order(file)+"\n"+f_get_barcode(file)+"\n"+f_str_res(file)+"\n"+f_get_alarm(file))
				os.remove(file)
				os.remove(file[:-4]+'_x1.png')
				os.remove(file[:-4]+'_x10.png')
				os.remove(file[:-4]+'_x100.png')
			except:
				print("file", str_file_name,"not suited")
		if msvcrt.kbhit():
			str_continue = "n"
			break
		time.sleep(1)

