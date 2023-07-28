from dublib.Methods import RemoveRecurringCharacters
from dublib.Methods import RemoveHTML
from bs4 import BeautifulSoup

import requests
import re

# Загрузчик книг с сайта BiB.bz.
class BiB:

	#==========================================================================================#
	# >>>>> МЕТОДЫ <<<<< #
	#==========================================================================================#

	# Возвращает список структур с описанием книг автора.
	def getAuthorsBooks(self, URL: str) -> list:
		# Список ссылок на книги автора.
		BooksLinks = list() 
		# Список структур с описанием книг автора.
		Books = list()
		# Загрузка страницы книги.
		Response = requests.get(URL)

		# Если запрос успешен.
		if Response.status_code == 200:
			# Парсинг книги.
			Soup = BeautifulSoup(Response.text, "html.parser")
			# Поиск заголовков книг.
			Headers = Soup.find_all("h2", {"class": "title"})
			
			# Для каждого заголовка получить URL ссылки.
			for Header in Headers:
				# Парсинг заголовка и помещение ссылки на книгу в список.
				BooksLinks.append(BeautifulSoup(str(Header), "html.parser").find("a")["href"])
			
			# Загрузить книгу по каждой ссылке.
			for Link in BooksLinks:
				Books.append(self.getBook(Link))

		return Books

	# Возвращшает структуру с описанием книги.
	def getBook(self, URL: str) -> dict | None:
		# Вывод в консоль: парсинг книги.
		print(f"Parsing book \"{URL}\"... ")
		# Структура с описанием книги.
		Book = {
			"site": URL,
			"name": None,
			"author": None,
			"description": None,
			"chapters": list()
		}
		# Загрузка страницы книги.
		Response = requests.get(URL)

		# Если запрос успешен.
		if Response.status_code == 200:
			# Парсинг книги.
			Soup = BeautifulSoup(Response.text, "html.parser")
			# Поиск списка глав.
			NavList = Soup.find("nav", {"id": "list"})
			# Поиск названия книги.
			Book["name"] = Soup.find("h1", {"id": "title"}).get_text().strip("«»")
			# Поиск названия книги.
			Book["author"] = Soup.find("h3", {"id": "author"}).get_text()
			# Парсинг главной секции.
			SmallSoup = BeautifulSoup(str(Soup.find("section", {"id": "main"})), "html.parser")
			# Удаление вложенных тегов.
			SmallSoup.find("nav").decompose()
			SmallSoup.find("h4").decompose()
			# Поиск описания книги и удаление повторяющихся пробелов (в том числе неразрывных).
			Book["description"] = RemoveRecurringCharacters(SmallSoup.get_text().replace(" ", " "), ' ')
			# Поиск тегов с ссылками на главы.
			ChaptersNavList = BeautifulSoup(str(NavList), "html.parser").find_all("a")
			# Список ссылок на главы.
			ChaptersLinks = list()

			# Для каждого тега ссылки получить источник.
			for Link in ChaptersNavList:
				ChaptersLinks.append(Link["href"])

			# Получить описание каждой главы.
			for Link in ChaptersLinks:
				Book["chapters"].append(self.getChapter(Link))

		else:
			# Обнуление структуры главы.
			Book = None

		return Book

	# Возвращает структуру с описанием главы.
	def getChapter(self, URL: str) -> dict | None:
		# Вывод в консоль: парсинг главы.
		print(f"Parsing chapter \"{URL}\"... ", end = "")
		# Структура с описанием главы.
		Chapter = {
			"number": None,
			"title": None,
			"paragraphs": list()
		}
		# Загрузка главы.
		Response = requests.get(URL)

		# Если запрос успешен.
		if Response.status_code == 200:
			# Парсинг главы.
			Soup = BeautifulSoup(Response.text, "html.parser")
			# Поиск содержимого главы.
			Article = Soup.find("article")
			# Поиск заголовка главы.
			ChapterTitle = BeautifulSoup(str(Article), "html.parser").find("h1").get_text(strip = True)

			# Если у главы есть номер.
			if re.search(r"глава \d+", ChapterTitle):
				# Поиск номера главы.
				Chapter["number"] = int(ChapterTitle.split('.')[0].strip("Глава "))
				# Поиск названия главы.
				Chapter["title"] = ChapterTitle.split('.')[-1].strip()

			else:
				# Поиск названия главы.
				Chapter["title"] = ChapterTitle

			# Поиск всех абзацев.
			Chapter["paragraphs"] = BeautifulSoup(str(Article), "html.parser").find_all("p")

			# Очистить каждый абзац от тегов.
			for Index in range(0, len(Chapter["paragraphs"])):
				Chapter["paragraphs"][Index] = RemoveHTML(Chapter["paragraphs"][Index])

		else:
			# Обнуление структуры главы.
			Chapter = None

		# Вывод в консоль: парсинг главы завершён.
		print("Done!")

		return Chapter