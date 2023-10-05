# 
#
#
#
#
#
import requests
from bs4 import BeautifulSoup as bs
import urllib3
import pandas as pd

urllib3.disable_warnings()

global base_url
global filtre_list
base_url = "https://www.escor.ru"
sub_url = 'https://www.escor.ru/catalog/elektronnye_komponenty_i_oborudovanie/'
filtre_list = ['/catalog/optoelektronika/','/catalog/rezistory/','/catalog/kondensatory/',
                '/catalog/rele_1/','/catalog/gazovoe_oborudovanie/','/catalog/razemy/',
                '/catalog/kabelnaya_produktsiya/', '/catalog/istochniki_pitaniya_2/','/catalog/izmeritelnye_pribory/',
                '/catalog/instrument/','/catalog/payalnoe_oborudovanie/','/catalog/raskhodnye_materialy_2/','/catalog/mikroskhemy/']
FILE_NAME = 'test.csv'
def catalogy_url(base_url,sub_url,filtre):
    result_url = []
    sub_result_url = []
    sub_result = []
    final_url = requests.get(sub_url, verify=False)
    soup = bs(final_url.text, 'lxml')
    names = soup.find('ul', class_='list_section')
    for index, name in enumerate(names):
        if index % 2:
            link = name.find("a")
            catalogyURL = link['href']
            result_url.append(catalogyURL)


    for i in range(1,len(result_url)):
        #print(result_url[i])
        #print(base_url+result_url[i])
        sub_url_2 = requests.get(base_url+result_url[i], verify=False)
        sub_soup = bs(sub_url_2.text, 'lxml')




        if sub_soup.find('ul', class_='list_section') != None:
            
            for index,name in enumerate(sub_soup.find('ul', class_='list_section')):
                if index % 2:
                    links = name.find("a")
                    catalogyURL_2 = links['href']
                    sub_result_url.append(catalogyURL_2)

    
    for i in range(0, len(result_url)):
        catalogy_url = result_url[i]
        filtred = filtre_list.count(catalogy_url)
        if filtred > 0:    
            sub_result.append(catalogy_url)
        
            
            sub_url = requests.get(base_url +(catalogy_url+'?PAGEN_1=1&setpagesize=500') , verify = False)
            soup = bs(sub_url.text, 'lxml')
            sub_href = soup.find('ul', class_='list_section')
            



            if sub_href != None:
                for urls_filtre in sub_href.find_all('a'):
                    sub_result.append(urls_filtre['href'])

            else:
                sub_href = soup.find('ul', class_='panel-category-list')
                for urls_filtre in sub_href.find_all('a'):
                    sub_result.append(urls_filtre['href'])



    
    result_ur = sub_result + result_url
    unique_list = list(set(result_ur))
    unique_list = list(set(unique_list) - set(filtre))
    return(unique_list)







def parse(main_url,catalogy_url): 

    
    result_list = {'Title': [], 'price': []}
    final_url = requests.get(main_url +(catalogy_url+'?PAGEN_1=1&setpagesize=4500') , verify = False)
    soup = bs(final_url.text, 'lxml')

    
    if catalogy_url == '/importnye_1/' or catalogy_url == '/catalog/otechestvennye_1/' :

        final_url = requests.get(main_url +(catalogy_url+'?PAGEN_1=1&setpagesize=100') , verify = False)
        soup = bs(final_url.text, 'lxml')

       
        list_page = soup.find('div', class_='list-pager')                       
        list_pages = list_page.find_all('span')                                 
        page = list_pages[-1]                                                                                                               
        s1 = "".join(c for c in str(page) if  c.isdecimal())                    
        pages = int(s1)
        print(pages)


        for i in range(1,pages):

            mest_url = requests.get(main_url +(catalogy_url+'?PAGEN_1='+str(i)+'&setpagesize=100') , verify = False)
            soup = bs(mest_url.text, 'lxml')



            for name in soup.find_all('td', class_='left'):
                result_list['Title'].append(name.a['title']+ '  ')


            for price in soup.find_all('span', itemprop='price'):
                sheme = price.get_text()
                sheme = ' '.join(sheme.split())
                result_list['price'].append(sheme+'  ')
    else:
        mest_url = requests.get(main_url +(catalogy_url+'?PAGEN_1='+'&setpagesize=4500') , verify = False)
        soup = bs(mest_url.text, 'lxml')  

        for name in soup.find_all('td', class_='left'):
            result_list['Title'].append(name.a['title']+ '  ')

        for price in soup.find_all('span', itemprop='price'):
            sheme = price.get_text()
            sheme = ' '.join(sheme.split())
            result_list['price'].append(sheme+'  ')


    df = pd.DataFrame(result_list)
    df.to_csv('test_2.csv', mode = 'a', index= False)  

    return(result_list)
       





if __name__ == "__main__":

    result_url = catalogy_url(base_url,sub_url,filtre_list)
    for i in range(0,len(result_url)):
        parce = parse(base_url, result_url[i])
    print('Программа завершила работу!')

