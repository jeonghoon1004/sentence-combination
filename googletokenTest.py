#
# @brief text 모델  자연어 처리 by google sentencepiece
#
# Created googletokenTest.py on Thu Jun 02 2022
#
# @author kim jeonghoon <kyg1084@gmail.com>
#
# @copyright (c) 2022 DPJ
#

import sentencepiece as spm
# import pandas as pd # 통계
# import urllib.request #url
# import csv

# ENG
# sp = spm.SentencePieceProcessor(model_file='test/test_model.model')
# sp = spm.SentencePieceProcessor(model_file='test/botchan.txt')
sp = spm.SentencePieceProcessor(model_file='m_bpe.model')
sp.encode('This is a test')

# KOR
# spm.SentencePieceTrainer.train('--input=test/great_legacy.txt --model_prefix=m_bpe --vocab_size=2000 --model_type=bpe')
# sp = spm.SentencePieceProcessor()
# sp.load('m_bpe.model')
# print(sp.encode_as_pieces('테스트 문장 구조. 잘 좀 잘라봐라'))