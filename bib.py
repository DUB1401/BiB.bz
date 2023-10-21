from dublib.Methods import CheckPythonMinimalVersion, MakeRootDirectories, WriteJSON
from dublib.Terminalyzer import *
from Source.BiB import BiB

import sys
import os

#==========================================================================================#
# >>>>> ИНИЦИАЛИЗАЦИЯ СКРИПТА <<<<< #
#==========================================================================================#

# Проверка поддержки используемой версии Python.
CheckPythonMinimalVersion(3, 10)
# Создание папок в корневой директории.
MakeRootDirectories(["Output"])

#==========================================================================================#
# >>>>> НАСТРОЙКА ОБРАБОТЧИКА КОМАНД <<<<< #
#==========================================================================================#

# Список описаний обрабатываемых команд.
CommandsList = list()

# Создание команды: get.
COM_get = Command("get")
COM_get.addKeyPosition(["author", "book", "chapter"], ArgumentType.URL, Important = True)
CommandsList.append(COM_get)

# Инициализация обработчика консольных аргументов.
CAC = Terminalyzer()
# Получение информации о проверке команд.
CommandDataStruct = CAC.checkCommands(CommandsList)

# Если не удалось определить команду.
if CommandDataStruct == None:
	# Завершение работы скрипта с кодом ошибки.
	exit(1)

#==========================================================================================#
# >>>>> ОБРАБОТКА КОММАНД <<<<< #
#==========================================================================================#

# Инициализация парсера BiB.bz.
BiB_Object = BiB()

# Загрзука главы.
if "chapter" in CommandDataStruct.Keys:
	# Получение описания главы.
	Chapter = BiB_Object.getChapter(CommandDataStruct.Values["chapter"])
	# Сохранение файла с описанием.
	WriteJSON("Output/" + Chapter["title"] + ".json", Chapter)

# Загрзука книги.
if "book" in CommandDataStruct.Keys:
	# Получение описания книги.
	Book = BiB_Object.getBook(CommandDataStruct.Values["book"])
	# Сохранение файла с описанием.
	WriteJSON("Output/" + Book["name"] + ".json", Book)

# Загрзука всех книг автора.
if "author" in CommandDataStruct.Keys:
	# Получение списка книг автора.
	Books = BiB_Object.getAuthorsBooks(CommandDataStruct.Values["author"])

	# Сохранение каждой книги.
	for Book in Books:
		WriteJSON("Output/" + Book["name"] + ".json", Book)