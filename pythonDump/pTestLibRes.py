from pResFromTxtFile import f_str_res,f_get_barcode,f_get_order
from datetime import datetime
import os
import shutil
str_date_today = datetime.today().strftime('%d%m%Y')
fol_today = 'C:\\pierre\\apps\\python apps\\graphgen\\'+str_date_today+'\\'
fol_today_E = 'E:\\G8\\'+str_date_today+'\\'
shutil.copy2("test.txt",fol_today_E)
print("input")
input()
os.makedirs(fol_today_E, exist_ok=True)
print(str_date_today,type(str_date_today))
file_test = "472409190250.txt"
print(f_get_order(file_test))
print(f_get_barcode(file_test))
print(f_str_res(file_test))
print("to fuck off press enter")
input()