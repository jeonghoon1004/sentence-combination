import json
import pandas
import openpyxl
import os

class extractExcel():
    path_json = "data/extracts.json"
    def __init__(self) -> None:
        self.getText()
        pass
    def read(self, path) -> None:
        self.list = []
        self.getList(path)
        
        data = None
        # F열 리뷰상세 내용 추출
        open(self.path_json, "w").close()
        for file in self.list:
            df = pandas.read_excel(file, usecols=[1,3,5]) # 1 상품명, 3 리뷰점수, 5 리뷰내용
            data = pandas.concat([data, df]) # merge
        self.toJson( data.to_json(orient='records' ,force_ascii=False) )
        # 카테고리별 문장 추출해서 sentence.json 업데이트
        self.getText()
        print("read() END")
    def getList(self, path) -> None:
        # path 하위 xlsx 확장자 검색 
        folders = os.listdir(path)
        folders.remove(".DS_Store")
        folders.remove("상품코드.txt")
        folders.remove("MarketExcelUploadReviewDefault.xlsx")
        # print( folders )
        for folder in folders:
            self.search(os.path.join(path, folder))

    # 재귀 함수로 하위 리스트 훓음, MarketExcelUploadReviewDefault [A~Z0~9 ** ].xlsx 파일 목표
    def search(self, dirname):
        if os.path.isdir(dirname):
            folders = os.listdir(dirname)
            for filename in folders:
                fullPath = os.path.join(dirname, filename)
                self.search(fullPath)
        else:
            if "MarketExcelUploadReviewDefault" in dirname and "~$MarketExcelUploadReviewDefault" not in dirname and dirname.endswith(".xlsx"):
                # print(dirname)
                self.list.append(dirname)
            else:
                pass
    def toJson(self, data):
        with open(self.path_json, "a+", encoding="utf-8") as f:
            f.write(data)
    # 리뷰글만 return self.TextList
    def getText(self, idx=None):
        with open(self.path_json, 'r', encoding="utf-8") as f:
            self.js_array = json.load(f)
            self.TextList = []
            if idx is not None:
                if type(idx) is tuple:
                    for num in idx:
                        self.TextList.append(self.js_array[num]["리뷰상세내용"])
                elif type(idx) is int:
                    self.TextList.append(self.js_array[idx]["리뷰상세내용"])
                else:
                    print("type mismatched : {} => tuple or int".format( type(idx) ))
            else:
                counter = 0
                for js in self.js_array:
                    if js["리뷰상세내용"] is not None:
                        self.TextList.append(js["리뷰상세내용"])
                        counter += 1
                        pass
                    else:
                        print('%s:\t%d' % (js, counter))
                        counter += 1
                        pass
        return self.TextList


if __name__ == "__main__":
    # extractExcel().read(r"C:\Users\com\Desktop\스마트스토어 to 스냅리뷰")
    extract = extractExcel()
    extract.getText(idx=(2, 3))
    print( "jsarray : {}".format( len(extract.js_array) ) )
    print( "content : {}".format( len(extract.TextList) ) )
    print( "content ==== \n{}\n============".format( extract.TextList ) )
    