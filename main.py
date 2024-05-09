import pprint
import json
from pydantic import BaseModel, HttpUrl, parse_raw_as
from typing import List, Optional
from jisho_api.word import Word
from jisho_api.kanji import Kanji
from jisho_api import scrape

def printAsJson(obj: BaseModel):
	print(json.dumps(obj.dict(), indent=4))

# res = Word.request('water')
# printAsJson(res)
# resDict = res.dict()

res = scrape(Kanji, ['水'], './out')