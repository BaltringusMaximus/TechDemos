def f_str_res(file):
	with open(file, "r") as txt_file:
		list_lines = txt_file.readlines()
		list_str = []
		str_line_value = str()
		int_index_line = int()
		for j in list_lines:
			if j[:1] == "3" and len(j)>2:
				int_index_line = list_lines.index(j)
		for i in list_lines[int_index_line]:
			if i.isnumeric() or i == ".":
				str_line_value = str_line_value+i
			else:
				if str_line_value != "":
					list_str.append(str_line_value)
				str_line_value = str()
	list_str_values = []
	if file[0:2] == "47":
		list_str_values = list_str[1:12]
	if file[0:2] in ["09","01"]:
		list_str_values = list_str[1:10]
	str_format = str()
	for i in list_str_values:
		str_format = str_format+i+"~"
	str_format = str_format[:-1]
	return str_format

def f_get_barcode(file):
	str_barcode = str()
	with open(file,"r") as txt_file:
		list_lines = txt_file.readlines()
	for line in list_lines:
		if line[:3] in ["112","122"]:
			str_barcode = line[3:]
	return str_barcode

def f_get_order(file):
	str_order = str()
	with open(file,"r") as txt_file:
		list_lines = txt_file.readlines()
	for line in list_lines:
		if line[:3] in ["112","122"]:
			str_order = line[5:]
	return str_order