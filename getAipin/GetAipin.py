from bs4 import BeautifulSoup as bs
import requests
import time
# '台北  &adkw=%E5%8F%B0%E5%8C%97',
locations = ['台南  &adkw=%E5%8F%B0%E5%8D%97',
             '高雄  &adkw=%E9%AB%98%E9%9B%84',
             '台中  &adkw=%E5%8F%B0%E4%B8%AD%E5%B8%82',
             '桃園  &adkw=%E6%A1%83%E5%9C%92%E5%B8%82',
             '新北  &adkw=%E6%96%B0%E5%8C%97%E5%B8%82']

def getAipinghref(location):
    url = 'http://www.ipeen.com.tw/search/all/000/1-0-0-0/?p=2' + location.split("  ")[1]
    cookie = 'ipeen_anonymous=f72698a3e6ea673ae76bf334b4256cbe; _atrk_sync_cookie=true; __gads=ID=164ff2371833fd9a:T=1501578738:S=ALNI_MZ5wMTrEVsmN6ZCSa1LVLlGVHNEDA; shop-score-tour=showed; ONEAD_config=%7B%7D; ipeen_update=ipeen_update; fbm_156261592614=base_domain=.ipeen.com.tw; crtg_rta=; _ipeen_search_category=0; appier_uid_1=1b1980d6-391d-40bb-fca6-60f258a3765d; _ga=GA1.3.296840282.1501578737; _gid=GA1.3.1033813361.1502532216; _gat=1; PHPSESSID=ca1692eb43aa206cd7aef9941d90aabe; lbss=1; lbsa=taiwan; _ias_lastreferrer=http://www.ipeen.com.tw/; __asc=cfe2424215dd5e621244ac39fbb; __auc=fb56e39015d9d11381b0e7722f2; appier_utmz=%7B%22csr%22%3A%22google%22%2C%22timestamp%22%3A1502532215%7D; _atrk_ssid=SxZelsQQn-YwAKM9S9I05P; _atrk_sessidx=40; _atrk_siteuid=W6CEyMZ5cn37-ROa; fbsr_156261592614=AyM0_M_83Aup0Mf5L8nnIlOo0dUsTxHZUFZi600GjI4.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUR4MHdHRnNYVnNUNzNMSGstTHpEWkZGVVZHU0VIYXlVUjVuMHdzbk83ek9USnBBM0Q1cUd5U1p6UXVOWTk4cG80REZjdzZRaDU5UjZ3a3dEWlhoQ3d6aDU2T2tuMnE5V0pnYTQ1eWVJTkxqZmk4empRTXg4TnYtOWUtY3pKYXUtSzlpNG1qQkRvb0x2azhsVi1oZXE2TXUtMTNaM1I5MXF6T2VsUDBiU0NYdlQzNjdhdUJTUHl6TzZkakpQendPUURTcl9fcWppQ3VoZjZRb01rWUUzbTVYaWtqUXo0dFdsTXVReGxIa3lydG5kcWYzMjJFcjRYZVJjRENrS3ljU1dQd2tYQkl0ejV6WXBDamZNZ2FlcjNVdTA0dVJDSjUwTVFRa0kzdzVMMnUzNTdpYjA1REp6U1RVUTQ2YjAwRk13SEZFZ1dEZi1faFFseEN0MWZ2TUV2QSIsImlzc3VlZF9hdCI6MTUwMjUzMjc3NSwidXNlcl9pZCI6IjE4NDQzNjE2NDIyNDcwMzQifQ'
    cookies = {}
    for i in cookie.split(";"):
        cookies[i.split("=")[0]] = i.split("=")[1]
    res = requests.get(url, cookies=cookies)
    pages = int(int(res.text.split('符合條件共 <b>')[1].split('</b> 筆結果</h2>')[0]) / 15)
    res.close()
    foodlist = []
    for page in range(1, int(2 * pages / 3)):
        url2 = 'http://www.ipeen.com.tw/search/all/000/1-0-0-0/?p=' + str(page) + location.split("  ")[1]
        res2 = requests.get(url2)
        print(res2.status_code)
        if res2.status_code == 200:
            if page%50==0:
                time.sleep(5)
            print(str(page) + location.split("  ")[0])
            soup2 = bs(res2.text, 'lxml')
            res2.close()
            lists = ['http://www.ipeen.com.tw' + i['href'] for i in
                     soup2.select("article > div > section > article > div > h3 > a ")]
            foodlist += lists
    liststring = ",".join(foodlist)
    with open('./Aiping/AipinwanFood' + location.split("  ")[0] + '.txt', "w", encoding='utf-8') as f:
        f.write(liststring)

import os

if not os.path.exists('Aiping'):
    os.makedirs('Aiping')

for location in locations:
    getAipinghref(location)
