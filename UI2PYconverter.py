from PyQt5 import uic

fin = open('FrequencyFilterUI.ui', 'r', encoding='UTF-8')  # UI文件
fout = open('FrequencyFilterUI.py', 'w', encoding='UTF-8')  # 接收UI的py文件
uic.compileUi(fin, fout, execute=True)  # 文件转换
fin.close()  # 关掉文件
fout.close()
