import json
import sys
import os
import re

# Проверяет, имеются ли кирилические символы в строке.
def CheckForCyrillicPresence(Text: str) -> bool:
	# Русский алфавит в нижнем регистре.
	Alphabet = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
	# Состояние: содержит ли строка кирилические символы.
	TextContainsCyrillicCharacters = not Alphabet.isdisjoint(Text.lower())

	return TextContainsCyrillicCharacters

# Очищает консоль.
def Cls():
	os.system("cls" if os.name == "nt" else "clear")

# Объединяет словари без перезаписи.
def MergeDictionaries(DictionaryOne: dict, DictionaryTwo: dict) -> dict:

	# Скопировать значения отсутствующих в оригинале ключей.
	for Key in DictionaryTwo.keys():
		if Key not in DictionaryOne.keys():
			DictionaryOne[Key] = DictionaryTwo[Key]

	return DictionaryOne

# Удаляет теги HTML из строки.
def RemoveHTML(TextHTML: str) -> str:
	# Регулярное выражение фильтрации тегов HTML.
	TagsHTML = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
	# Удаление найденных по регулярному выражению тегов.
	CleanText = re.sub(TagsHTML, '', str(TextHTML))

	return str(CleanText)

# Удаляет из строки подряд идущие повторяющиеся символы.
def RemoveRecurringCharacters(String: str, Character: str) -> str:

	# Пока в строке находятся повторы указанного символа, удалять их.
	while Character + Character in String:
		String = String.replace(Character + Character, Character)

	return String

# Удаляет из строки все вхождения подстрок, совпадающие с регулярным выражением.
def RemoveRegexSubstring(Regex: str, String: str) -> str:
	# Поиск всех совпадений.
	RegexSubstrings = re.findall(Regex, String)

	# Удаление каждой подстроки.
	for RegexSubstring in RegexSubstrings:
		String = String.replace(RegexSubstring, "")

	return String

# Переименовывает ключ в словаре, сохраняя исходный порядок.
def RenameDictKey(Dictionary: dict, OldKey: str, NewKey: str) -> dict:
	# Результат выполнения.
	Result = dict()

	# Перебор элементов словаря по списку ключей.
	for Key in Dictionary.keys():

		# Если нашли нужный ключ, то переместить значение по новому ключу в результат, иначе просто копировать.
		if Key == OldKey:
			Result[NewKey] = Dictionary[OldKey]
		else:
			Result[Key] = Dictionary[Key]

	return Result

# Выключает ПК: работает на Windows и Linux.
def Shutdown():
	if sys.platform == "linux" or sys.platform == "linux2":
		os.system("sudo shutdown now")
	elif sys.platform == "win32":
		os.system("shutdown /s")

# Сохраняет стилизованный JSON файл.
def SaveJSON(Dictionary: dict, Path: str):
	with open(Path, "w", encoding = "utf-8") as FileWrite:
		json.dump(Dictionary, FileWrite, ensure_ascii = False, indent = '\t', separators = (",", ": "))