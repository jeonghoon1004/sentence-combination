# from ckonlpy.tag import Twitter # 아래 Okt로 전환됨
import json
import re

from konlpy.tag import Okt
from konlpy.utils import pprint
from konlpy.tag import Komoran

# from krwordrank.word import KRWordRank, summarize_with_keywords
# from krwordrank.sentence import summarize_with_sentences

# from extract import extractExcel

# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# from hanspell import spell_checker

import torch
# from fastai.text.all import *
# import fastai
# from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

# from torch.utils.data import DataLoader, Dataset
# from transformers.optimization import AdamW, get_cosine_schedule_with_warmup

class koreanTokenizer:
    def __init__ (self):
        self.okt = Okt()
    def addNoun(self):
        self.okt.nouns('단어') # 단어사전에 추가
    def morph(self, text):
        return self.okt.morphs(text)
        # Twitter.add_dictionary('단어', 'Noun') # 단어사전에 추가 *구버전
    def pos(self, text):
        return self.okt.pos(text)
    def noun(self, text):
        return self.okt.nouns(text)
    def prase(self, text):
        return self.okt.phrases(text)
    def getTags(self, text, filter = None ):
        self.okt.normalize
        prep = self.okt.pos(text)
        matched = []
        for dict in prep:
            name = dict[0] # 원문
            if name in filter:
                matched.append(name)
        return "matched tag {}".format(matched) if len(matched) > 0 else None
class kmran:
    def __init__(self) -> None:
        self.kmr = Komoran(userdic="data/dict.txt")
        
        pass
    def morph(self, text):
        try:
            return self.kmr.morphs(text)
        except:
            print("error text : {}".format(text))
    def pos(self, text):
        try:
            return self.kmr.pos(text, flatten=True)
        except:
            print("error text : {}".format(text))
    def nouns(self, text):
        try:
            # spelled_sent = spell_checker.check(text)
            # hanspell_sent = spelled_sent.checked
            # return self.kmr.nouns(hanspell_sent)
            return self.kmr.nouns(text)
        except:
            print("error text : {}".format(text))
            # return self.kmr.nouns(text)
    def getTags(self, text, filter = None ):
        try:
            prep = self.kmr.pos(text, flatten=False)
            matched = []
            for dict in prep:
                name = dict[0]
                if name in filter:
                    matched.append(name)
            return "matched tag {}".format(matched) if len(matched) > 0 else None
        except:
            print("error text : {}".format(text))
    def unkownChecker(self):
        path_temp_json = 'data/test_sentence_json.json'
        with open(path_temp_json, "r", encoding="utf-8") as f:
                js_obj = json.load(f)
                OptionList = []
                for key in js_obj:
                    OptionList.append(key)
        for text in js_obj["모호함"]:
            pprint( kmran().pos(text) )
# class rank:
#     def __init__(self) -> None:
#         pass
#     def extractBest(self, stopwords=None ):
#         if stopwords is None:
#             stopwords = {'림프', '마사지', '세탁기', '곰팡이', '후드'}
#         penalty = lambda x:0 if (25 <= len(x) <= 80) else 1
#         keywords, sents = summarize_with_sentences( texts, penalty=penalty, stopwords=stopwords, diversity=0.5, num_keywords=100, num_keysents=10, verbose=False )
#         print('sentence : %s' % (sents))
        
#     def drawKewords(self):
#         passwords = {
#             word:score for word, score in sorted(keywords.items(), key=lambda x:-x[1])[:300] if not (word in stopwords)
#         }
#         krwordrank_cloud = WordCloud(
#             font_path = font_path,
#             width = 800,
#             height = 800,
#             background_color="white"
#         )
#         krwordrank_cloud = krwordrank_cloud.generate_from_frequencies(passwords)
#         fig = plt.figure(figsize=(10, 10))
#         plt.imshow(krwordrank_cloud, interpolation="bilinear")
#         plt.show()
        # fig.savefig('./wordcloud.png')
    
# TODO keras 기반 seq2seq LSTM 모델, KoGPT-2 모델 딥러닝 
# LSTM 25~100자 긴문장 과적합발생이슈  
# - epoch 50 batch size 64 50번 반복; 12만 리뷰 검증시 70% 목표치  데이터 양 부족하면 일반적 데이터 패턴을 학습 문제
# bahdanau attention 적용 seq2seq모델
# - epoch 100 batch size 2 검증정확도는 오름 - 훈련 정확도가 낮아서 그런지 다른 리뷰생성이슈
# [ ] KoGPT 한글 사전학습  Transformer decoder 12층, BPE 기반 SentencePiece 토큰화 방식
# - 상기 2 모델보다는 정확하지만 어색한 문장이 연결됨 훈련90%이하 검증 93% 데이터 12만개 리뷰
# class ReviewGenerator:
#     def __init__(self) -> None:
#         path_temp_json = 'data/test_sentence_json.json'
        
#         torch.manual_seed(42)
#         # 기본 베이스는 신문기사, 청와대 연설문 등으로 리뷰관련된 추가학습이 필요
#         self.tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2", 
#                                                                  bos_token='</s>', 
#                                                                  eos_token='</s>', 
#                                                                  unk_token='<unk>',
#                                                                  pad_token='<pad>', 
#                                                                  mask_token='<mask>')
#         self.model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
        
#         with open(path_temp_json, "r", encoding="utf-8") as f:
#             data_json = json.load(f)
#         keys = data_json.keys()
#         data = []
#         for k in keys:
#             data.append( data_json[k] )
#         tls = TfmdLists(data, TransformersTokenizer(self.tokenizer))
#         batch,seq_len = 8,256
#         # dls = tls.dataloaders(bs=batch, seq_len=seq_len)
#         # dls.show_batch(max_n=2)
        
#         pass
#     def generator(self, text) -> None:
#         input_ids = self.tokenizer.encode(text, return_tensors='pt')
#         gen_ids = self.model.generate(input_ids, max_length=128, 
#                                       repetition_penalty=2.0, 
#                                       pad_token_id=self.tokenizer.pad_token_id,
#                                       eos_token_id=self.tokenizer.eos_token_id,
#                                       bos_token_id=self.tokenizer.bos_token_id,
#                                       use_cache=True)
#         generated = self.tokenizer.decode(gen_ids[0])
#         print(generated)
#         pass

# class TransformersTokenizer(Transform):
#     def __init__(self, tokenizer) -> None:
#         self.tokenizer = tokenizer
#     def encode(self, x):
#         toks = self.tokenizer.tokenize(x)
#         return torch.tensor(self.tokenizer.convert_tokens_to_ids(toks))
#     def decodes(self, x):
#         return TitledStr(self.tokenizer.decode(x.cpu().numpy()))

if __name__ == "__main__": # 직접 실행된 모듈일 경우
    print(torch.__version__)
    korText = "빠른 배송 좋은 품질 굿입니다." # test
    test_str = '좋아지는 것 같아요🥰🥰'
    filter = ["배송", "품질", "서비스", "만족"]
    stopwords = {'림프', '마사지', '세탁기', '곰팡이', '후드'}
    font_path = 'font/NanumGothic.ttf' # wordcloud hangul font
    
    only_BMP_pattern = re.compile("["
        u"\U00010000-\U0010FFFF"  #BMP characters 이외
                "]+", flags=re.UNICODE)
    test_str = only_BMP_pattern.sub(r'', test_str)    

    print(test_str)
    # pprint( koreanTokenizer().getTags(korText, filter=filter) )
    # pprint( kmran().getTags(korText, filter=filter) )
    
    pprint( kmran().getTags(test_str, filter=stopwords))
    pprint( kmran().nouns(test_str) )
    pprint( kmran().pos(test_str) )
    
    # path_temp_json = 'data/test_sentence_json.json'
    # with open(path_temp_json, "r", encoding="utf-8") as f:
    #         js_obj = json.load(f)
    #         OptionList = []
    #         for key in js_obj:
    #             OptionList.append(key)
    # for text in js_obj["모호함"]:
    #     text = only_BMP_pattern.sub(r'', text)
    #     # pprint( kmran().pos(text) )
    #     pprint( kmran().nouns(text) )
    
    # gen = ReviewGenerator()
    # gen.generator("배송 감사")
    
    # quit()
        
#     # test TextJson
#     extracts = extractExcel()
#     extracts.getText()
#     texts = extracts.TextList
#     print("json {} sentence loaded".format(len(texts)))
    
    
#     min_count = 5
#     max_length = 10
#     wordrank_extractor = KRWordRank(min_count=min_count, max_length=max_length) #전처리
    
#     beta = 0.85
#     max_iter = 10
#     keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter) #추출
#     for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
#         print('%8s:\t%.4f' % (word, r))
    
    
#     # passwords = {
#     #     word:score for word, score in sorted(keywords.items(), key=lambda x:-x[1])[:300] if not (word in stopwords)
#     # }
#     # keywords = summarize_with_keywords(texts) # with default arguments
#     # keywords = summarize_with_keywords(texts, min_count=5, max_length=10,
#     #     beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)    
#     # for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
#     #     print('%8s:\t%.4f' % (word, r))
    
#     # default sentence
#     # keywords, sents = summarize_with_sentences(texts, num_keywords=100, num_keysents=10)
#     # print('sentence : %s' % (sents)) # num_keysents 개 최대조합 리뷰글
    
#     # 길이제한, 금지어 포함
#     penalty = lambda x:0 if (25 <= len(x) <= 80) else 1
#     keywords, sents = summarize_with_sentences( texts, penalty=penalty, stopwords=stopwords, diversity=0.5, num_keywords=10, num_keysents=10, verbose=False)
#     print('dict : %s' % (keywords))
#     print('sentence 2 : %s' % (sents))
    


# # ========================================================================
# def practice():
#     korText = "빠른 배송 좋은 품질 굿입니다." # test
#     filter = ["배송", "품질", "서비스", "만족"]
    
#     font_path = 'font/NanumGothic.ttf' # wordcloud hangul font
    
#     # pprint( koreanTokenizer().getTags(korText, filter=filter) )
#     # pprint( kmran().getTags(korText, filter=filter) )
    
#     extracts = extractExcel()
#     extracts.getText()
#     texts = extracts.TextList
#     print(len(texts))
    
#     min_count = 5
#     max_length = 10
#     wordrank_extractor = KRWordRank(min_count=min_count, max_length=max_length)
    
#     beta = 0.85
#     max_iter = 10
#     keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter)
#     for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
#         print('%8s:\t%.4f' % (word, r))
    
#     stopwords = {'림프', '마사지', '세탁기', '곰팡이'}
#     passwords = {
#         word:score for word, score in sorted(keywords.items(), key=lambda x:-x[1])[:300] if not (word in stopwords)
#     }
#     # keywords = summarize_with_keywords(texts) # with default arguments
#     keywords = summarize_with_keywords(texts, min_count=5, max_length=10,
#         beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)    
#     for word, r in sorted(keywords.items(), key=lambda x:x[1], reverse=True)[:30]:
#         print('%8s:\t%.4f' % (word, r))
    
#     # Set your font path
    
#     # krwordrank_cloud = WordCloud(
#     #     font_path = font_path,
#     #     width = 800,
#     #     height = 800,
#     #     background_color="white"
#     # )
#     # krwordrank_cloud = krwordrank_cloud.generate_from_frequencies(passwords)
    
#     # fig = plt.figure(figsize=(10, 10))
#     # plt.imshow(krwordrank_cloud, interpolation="bilinear")
#     # plt.show()
#     # fig.savefig('./wordcloud.png')
    
#     # default sentence
#     keywords, sents = summarize_with_sentences(texts, num_keywords=100, num_keysents=10)
#     print('sentence : %s' % (sents)) # num_keysents 개 최대조합 리뷰글
    
#     # 길이제한, 금지어 포함
#     penalty = lambda x:0 if (25 <= len(x) <= 80) else 1
#     keywords, sents = summarize_with_sentences( texts, penalty=penalty, stopwords=stopwords, diversity=0.5, num_keywords=100, num_keysents=10, verbose=False)
#     print('sentence 2 : %s' % (sents))