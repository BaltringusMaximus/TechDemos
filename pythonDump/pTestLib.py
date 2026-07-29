from LibTxt import f_str_results,f_get_barcode,f_get_tubeid_from_hca,f_get_order_from_hca,f_get_res_from_hca
#str_to_send = f_str_results("092409160171_hca_data")
#print(str_to_send)
#print(f_get_barcode("092409160171_hca_data"))
print(f_get_res_from_hca("092409160171_hca_data.txt"))
print(f_get_tubeid_from_hca("092409160171_hca_data.txt"))
print(f_get_order_from_hca("092409160171_hca_data.txt"))
print("press enter to fuck off")
input()