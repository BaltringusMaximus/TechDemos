from pTestGraph_v2 import f_graph_from_text
from pResFromTxtFile_v2 import f_get_alarm
file = "012412230042.txt"
f_graph_from_text(file)
alarm = f_get_alarm(file)
print(alarm)