from bs4 import BeautifulSoup as bs
import time
import requests
import os
import json

for filename in os.listdir('./Aiping/'):
    if not os.path.exists('./Aipingjson/' + filename.split(".")[0] + '.json'):
        with open('./Aiping/' + filename, encoding='utf-8') as data:
            x = data.read()
            urls = x.split(",")
            count = 0
            biglist = []
            for url in urls:
                url = url.split("-")[0]
                res = requests.get(url)
                if res.status_code == 200:
                    count += 1
                    print(count)
                    if count % 40 == 0:
                        time.sleep(3)
                    if count % 50 == 0:
                        if not os.path.exists('Aipingjson'):
                            os.makedirs('Aipingjson')
                        with open('./Aipingjson/' + filename.split(".")[0] + '.json', 'w') as f:
                            json.dump(biglist, f)
                    soup = bs(res.text, 'lxml')
                    res.close

                    #     print(soup.select("#shop-header > div.info > h1 > span")[0].text.strip())
                    #     print(soup.select("#shop-header > div.info > div.brief > p.cate.i > a")[0].text)
                    #     print(soup.select("#shop-header > div.info > div.brief > p.tel.i > a")[0].text.replace("-",""))
                    #     print(soup.select("#shop-header > div.info > div.brief > p.addr.i > a")[0].text.strip())
                    #     print(soup.select("#shop-header > div.info > div.brief > p.cost.i")[0].text.strip().split("  ")[1].split(" ")[0])
                    #     print(soup.select("#shop-summary > div.summary")[0].text.strip().replace(" ",""))
                    #     print(soup.select("#shop-header > div.info > div.hours")[0].text)
                    #     print(soup.select("#shop-header > div.info > div.hours > div > span"))

                    peenlist = []
                    dien = {}
                    try:
                        for i in range(1, 5):
                            url2 = url + '/comments?p=' + str(i)
                            res2 = requests.get(url2)
                            if res2.status_code == 200:
                                soup2 = bs(res2.text, 'lxml')
                                pagepeenlist = ['http://www.ipeen.com.tw' + i['href'] for i in
                                                soup2.select("p.summary > a")]
                                peenlist += pagepeenlist
                    except:
                        pass
                    try:
                        dien['name'] = soup.select("#shop-header > div.info > h1 > span")[0].text.strip()
                        dien['address'] = (
                        soup.select("#shop-header > div.info > div.brief > p.addr.i > a")[0].text.strip())
                        dien['coordinate'] = None
                        dien['tel'] = soup.select("#shop-header > div.info > div.brief > p.tel.i > a")[0].text.replace("-",
                                                                                                                       "")
                        dien['business_hours'] = None
                        dien['average_consumption'] = \
                        soup.select("#shop-header > div.info > div.brief > p.cost.i")[0].text.strip().split("  ")[1].split(
                            " ")[0]
                        dien['style'] = soup.select("#shop-header > div.info > div.brief > p.cate.i > a")[0].text
                        dien['introduction'] = soup.select("#shop-summary > div.summary")[0].text.strip().replace(" ",
                                                                                                                  "").replace(
                            "\r", "").replace("\n", "")
                        dien['tag'] = None
                        dien['comment'] = peenlist
                        dien['coupon'] = None
                        dien['image'] = None
                        print(dien)
                        biglist.append(dien)
                    except:
                        pass
            # print(peenlist)
            if not os.path.exists('Aipingjson'):
                os.makedirs('Aipingjson')
            with open('./Aipingjson/' + filename.split(".")[0] + '.json', 'w') as f:
                json.dump(biglist, f)