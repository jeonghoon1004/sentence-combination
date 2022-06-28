![logo](./data/logo.png)
# 사양 : 
python
window
json

# 화면  :
1. 등록(문장, 카테고리박스 선택으로 등록)
  json파일로 카테고리별 문장 축적
     ※ 클립보드 자동 붙여넣기, 카테고리 관련 단어시 해당 문장 자동 축적
2. 조합(텍스트 편집기 느낌으로)
  텍스트 편집기에 카테고리 태그를 넣고 각 카테고리에 랜덤 출력
      ※ 드래그 드랍형식(front), 클립보드에 등록, 단축키 조합, preview 투명창

※ 미확정 추가 별도 기능

<!-- py to exe -->
py -m PyInstaller -F -w --i="data/logo.png" --add-data="data/logo.png;." main.py
<!-- .exe module error -->
for d in a.datas:
    if '_C.cp310-win_amd64.pyd' in d[0]:
        a.datas.remove(d)
        break

py -m PyInstaller main.spec