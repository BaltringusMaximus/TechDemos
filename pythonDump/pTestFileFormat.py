with open("datatest.txt", "r") as txt_file:
	list_lines = txt_file.readlines()
#	print(list_lines)
	list_str = []
	str_line_value = str()
	int_index_line = int()
	for j in list_lines:
#		print(j[:3])
		if j[:3] == "300":
#			print(j)
			int_index_line = list_lines.index(j)
#	print(int_index_line)
	for i in list_lines[int_index_line]:
		if i.isnumeric() or i == ".":
			str_line_value = str_line_value+i
#			print(str_line_value)
		else:
			if str_line_value != "":
				list_str.append(str_line_value)
			str_line_value = str()
#	print(list_str)
list_str_values = list_str[2:10]
#print(list_str_values)
str_format = str()
for i in list_str_values:
	str_format = str_format+i+"~"
str_format = str_format[:-1]
print(str_format)