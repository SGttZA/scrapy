「いらすとや」で画像を取得

irasutoya #ここに移動して scrapy crawl spider名 で実行(例: scrapy craw irasuto_category)
    │  chromedriver.exe #https://chromedriver.chromium.org/downloads (使ってるchromeのバージョンに合わせてDL)
    │  scrapy.cfg
    │
    └─irasutoya
        │  items.py
        │  middlewares.py
        │  pipelines.py
        │  settings.py #IMAGES_STORE = r'ここに保存先のパスを指定' (一番下の行にあります)
        │  __init__.py
        │
        └─spiders
		irasuto_category.py #9行目のstart_urlsにカテゴリーごとのURLを指定(複数指定可)
                irasuto_search.py #22行目の search_word に検索したい文字列を入れる
                __init__.py

※irasuto_searchを使う場合scrapy-seleniumが必要 
pip install scrapy-selenium