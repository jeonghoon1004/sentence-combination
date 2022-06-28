
# from transformers import RobertaConfig, RobertaModel, RobertaTokenizer
# tokenizer = RobertaTokenizer.from_pretrained("roberta-base")


# from konlpy.tag import Mecab
# tokenizer = Mecab()
# print(tokenizer.morphs(kor_text))


# nltk data 설치
# import nltk
# nltk.download()

import urllib.request

from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer

# 한국어 전처리 , 학습기반
# 데이터 로드
# urllib.request.urlretrieve("https://raw.githubusercontent.com/lovit/soynlp/master/tutorials/2016-10-20.txt", filename="2016-10-20.txt")
# corpus = DoublespaceLineCorpus("2016-10-20.txt")
# len(corpus)
# i=0
# for document in corpus:
#     if len(document) > 0:
#         print("corpus : {}".format(document))
#         i=i+1
#     if i==3:
#         break

# 학습
# word_extractor = WordExtractor()
# word_extractor.train(corpus)
# word_score_table = word_extractor.extract()

# L토큰 R토큰 띄우기 구분 - 점수기반 L토큰 추출
# scores = {word:score.cohesion_forward for word, score in word_score_table.items()}
# l_tokenizer = LTokenizer(scores=scores)
# l_tokenizer.tokenize("국제사회와 우리의 노력들로 범죄를 척결하자", flatten=False)
