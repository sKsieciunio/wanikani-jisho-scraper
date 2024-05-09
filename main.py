import json
from typing import List
from jisho_api import scrape
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


def parse_res_to_Vocab(res) -> List[Vocab]:
	Vocabs = []
	for elem in res:
		definitions = [sense.get('english_definitions', []) for sense in elem.get("senses", [])]
		Vocabs.append(Vocab(elem['slug'], definitions))
	return Vocabs



res = Word.request('water')
res = res.dict()
res = res['data']

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

print(json.dumps(res, indent=4))

vocabs = parse_res_to_Vocab(res)

console = Console()
console.print(f"[red bold]=================LOGS==================")
for elem in vocabs:
	print(elem)