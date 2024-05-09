import sys
import argparse
from typing import List
from jisho_api.word import Word
from rich.console import Console

class Vocab:
	def __init__(self, word: str, definitions: List[List[str]]) -> None:
		self.word = word
		self.definitions = definitions

	def __str__(self) -> str:
		return_string = self.word + ":\n"
		for sense in self.definitions:
			return_string += "  ----DEF----\n"
			for definition in sense:
				return_string += f"    > {definition}\n"
		return_string += "\n\n"
		return return_string


def parse_res_to_Vocab(res, n) -> List[Vocab]:
	Vocabs = []
	for index, elem in enumerate(res):
		if index >= n:
			break
		definitions = [sense.get('english_definitions', []) for sense in elem.get("senses", [])]
		Vocabs.append(Vocab(elem['slug'], definitions))
	return Vocabs

if __name__ == '__main__':
	# parsing cli arguments
	argv_parser = argparse.ArgumentParser(
		prog='wanikani jisho parser',
		description='It does something',
		epilog='thats epilog'
	)
	argv_parser.add_argument('searchWord', type=str)
	argv_parser.add_argument('-n', '--number', type=int)
	args = argv_parser.parse_args()

	# scraping data from jisho
	res = Word.request(args.searchWord)
	res = res.dict()
	res = res['data']

	# data cleanup
	keys_to_remove = ['is_common',
					'tags',
					'jlpt',
					'japanese',
					'parts_of_speech',
					'links',
					'restrictions',
					'see_also',
					'antonyms',
					'source',
					'info']

	for word in res:
		for key in keys_to_remove:
			if key in word:
				del word[key]
		for sense in word['senses']:
			for key in keys_to_remove:
				if key in sense:
					del sense[key]

	# parsing cleanedup data to Vocab objects
	dictionary = parse_res_to_Vocab(res, args.number)

	console = Console()
	console.print(f"[red bold]=================Jisho==================")
	for elem in dictionary:
		print(elem)