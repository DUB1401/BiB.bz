from dublib.Methods import SaveJSON
from dublib.Terminalyzer import *
from Source.BiB import BiB

import sys
import os

#==========================================================================================#
# >>>>> ПРОВЕРКА ВЕРСИИ PYTHON <<<<< #
#==========================================================================================#

# Минимальная требуемая версия Python.
PythonMinimalVersion = (3, 10)
# Проверка соответствия.
if sys.version_info < PythonMinimalVersion:
	sys.exit("Python %s.%s or later is required.\n" % PythonMinimalVersion)

#==========================================================================================#
# >>>>> СОЗДАНИЕ ВЫХОДНОЙ ДИРЕКТОРИИ <<<<< #
#==========================================================================================#

# Если выходная директория не существует, то создать.
if os.path.isdir("Output") == False:
	os.makedirs("Output")

#==========================================================================================#
# >>>>> НАСТРОЙКА ОБРАБОТЧИКА КОМАНД <<<<< #
#==========================================================================================#

# Создание команды: get.
COM_get = Command("get")
COM_get.addKeyPosition(["author", "book", "chapter"], ArgumentType.URL, Important = True)

# Инициализация обработчика консольных аргументов.
CAC = Terminalyzer()

#==========================================================================================#
# >>>>> ОБРАБОТКА КОММАНД <<<<< #
#==========================================================================================#

# Инициализация парсера BiB.bz.
BiB_Object = BiB()

# Загрзука главы.
if CAC.checkCommand(COM_get) and "chapter" in CAC.checkCommand(COM_get).Keys:
	# Получение описания главы.
	Chapter = BiB_Object.getChapter(CAC.checkCommand(COM_get).Values["chapter"])
	# Сохранение файла с описанием.
	SaveJSON(Chapter, "Output/" + Chapter["title"] + ".json")

# Загрзука книги.
if CAC.checkCommand(COM_get) and "book" in CAC.checkCommand(COM_get).Keys:
	# Получение описания книги.
	Book = BiB_Object.getBook(CAC.checkCommand(COM_get).Values["book"])
	# Сохранение файла с описанием.
	SaveJSON(Book, "Output/" + Book["name"] + ".json")

# Загрзука всех книг автора.
if CAC.checkCommand(COM_get) and "author" in CAC.checkCommand(COM_get).Keys:
	# Получение списка книг автора.
	Books = BiB_Object.getAuthorsBooks(CAC.checkCommand(COM_get).Values["author"])

	# Сохранение каждой книги.
	for Book in Books:
		SaveJSON(Book, "Output/" + Book["name"] + ".json")