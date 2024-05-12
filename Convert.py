import subprocess
import os
from tkinter.filedialog import askopenfilename
from tkinter import Tk, messagebox, filedialog



# Функция для добавления поддержки русского языка
def add_russian_support(tex_file):


    with open(tex_file, 'r', encoding='utf-8') as file:
        start_of_file = file.readline()
        file.seek(32)
        rest_of_file = file.read()
        file.close()
    with open(tex_file, 'w', encoding='utf-8') as file:
        file.write(start_of_file)
        file.write("\\usepackage[utf8]{inputenc}\n")
        file.write("\\usepackage[russian]{babel}\n")
        file.write("\\usepackage{cmap}\n")
        file.write(rest_of_file)
        file.close()

def file_location(place):
    while place[-1]!="/":
        place = place[:-1]
    return place


# Функция для конвертации ipynb в pdf
def convert_ipynb_to_pdf(ipynb_path):
    # Расположение файла
    file_loc = file_location(ipynb_path)

    os.chdir(file_loc)

    # Конвертация в .tex
    subprocess.run(["jupyter", "nbconvert", "--to", "latex", ipynb_path], check=True)
    
    # Получение имени .tex файла
    tex_file = ipynb_path.replace(".ipynb", ".tex")
    
    # Добавление поддержки русского языка
    add_russian_support(tex_file)
    
    # Конвертация в .pdf
    subprocess.run(["pdflatex", tex_file], check=True)
    
    #Удаление вспомогательных файлов
    try:
        os.remove(ipynb_path.replace(".ipynb", ".tex"))
        os.remove(ipynb_path.replace(".ipynb", ".log"))
        os.remove(ipynb_path.replace(".ipynb", ".out"))
        os.remove(ipynb_path.replace(".ipynb", ".aux"))
    except:
        pass
        
# Создание UI для выбора файла
Tk().withdraw()
ipynb_path = askopenfilename(filetypes=[("IPython Notebook", "*.ipynb")])

# Подтверждение от пользователя
if messagebox.askyesno("Подтверждение", f"Вы хотите конвертировать {ipynb_path} в PDF?"):
    convert_ipynb_to_pdf(ipynb_path)