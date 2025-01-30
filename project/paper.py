import pandas as pd
from lxml import etree
import requests



def get_params(num, keywords):
    data = {
        'searchType': 'publisherSearch',
        'sort': 'Relevance',
        'query': keywords,
        'page': num
    }
    return data


def get_data(data):
    search_url = "https://www.springeropen.com/search?"
    try:
        
        resp = requests.get(search_url, headers=headers, params=data)

        resp.raise_for_status()

        resp.encoding = resp.apparent_encoding
        tree = etree.HTML(resp.text)  

        list_data = tree.xpath('//*[@id="main-content"]/div/main/div/ol/li')
        return list_data
    except Exception as e:
        print("Failed", e)



def get_info(li_list):
    cnt = 1

    for li in li_list:

        title = li.xpath('./article/h3/a/text()')[0]

        title_link = li.xpath('./article/h3/a/@href')[0]
        full_text_link = 'https:' + str(title_link)

        journal_title = li.xpath('./article/div[2]/em/text()')[0]

        article_type = li.xpath('./article/div[3]/span[1]/text()[1]')[0]

        published_on = li.xpath('normalize-space(./article/div[3]/span[2]/text())') + \
                       li.xpath('normalize-space(./article/div[3]/span[2]/span/text())')

        pdf_link = li.xpath('./article/ul/li[2]/a/@href')[0]
        download_pdf_link = 'https:' + str(pdf_link)
        print(cnt, title, 'done!!!')
        cnt += 1
        all_info.append([title, published_on, journal_title, article_type, full_text_link, download_pdf_link])


def save_data(all_info):
   
    df = pd.DataFrame(all_info, columns=['title', 'published_on', 'journal_title',
                                             'article_type', 'full_text_link', 'download_pdf_link'])

    df.to_csv(f'{keywords}.csv', encoding='utf-8')



if __name__ == '__main__':

    search_url = "https://www.springeropen.com/search?"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    }

    print('please enter the keywords you want to query')
    keywords = input('keywords:')
    print('please enter the pages range you want to query')
    start_page = int(input('start_page:'))
    end_page = int(input('end_page:')) + 1


    all_info = []
    for i in range(start_page, end_page):
        print(f'Begin{i} Page')
        params_data = get_params(i, keywords)
        li_list = get_data(params_data)
        info_list = get_info(li_list)
        print(f'End{i} Page。')

    save_data(all_info)
    print('Completed')

import requests
from lxml import html
for entry in all_info:
    article_url = entry[4] 
    try:

        response = requests.get(article_url)
        if response.status_code == 200:
            page_content = html.fromstring(response.content)
            print(page_content)
            

            keywords = page_content.xpath('//*[@id="article-info-content"]/div/div[2]/ul[2]/li/span/a/text()')
            print(keywords)

            if keywords:
                entry.extend(keywords)
        else:
            print(f"Failed to fetch the page: {article_url}, status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching keywords for {article_url}: {e}")

for entry in all_info:
    print(entry)

from collections import defaultdict, Counter


year_keywords = defaultdict(list)

for info in all_info:

    year = info[1].split()[-1]  

    keywords = info[6:]

    year_keywords[year].extend(keywords)


year_keyword_counts = {}

for year, keywords in year_keywords.items():

    keyword_count = Counter(keywords)
    year_keyword_counts[year] = keyword_count


for year, counts in year_keyword_counts.items():
    print(f"Year: {year}")
    for keyword, count in counts.items():
        if count > 1:  
            print(f"  Keyword: '{keyword}' appears {count} times")
    print("---")
