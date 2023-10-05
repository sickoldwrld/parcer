import requests
from bs4 import BeautifulSoup as bs
import urllib3

urllib3.disable_warnings()

final_url = requests.get('https://www.escor.ru/catalog/elektroinstrument/?PAGEN_1=1&setpagesize=10' , verify = False)
soup = bs(final_url.text, 'lxml')
price = soup.find_all("span", itemprop="price")
price = price.get_text()
print(price)





    """
        for local in soup.find_all('td', class_='left'):
            href = (local.a['href'])
            href_list.append(href)
            b += 1            
            #print(local.a['href'])
            len_list=len(href_list)
            #print(len_list)

            local_url = requests.get(main_url+str(href_list[j]) , verify = False)           
                avaibitly = bs(local_url.text, 'lxml')
                error_404 = avaibitly.find('p', class_='button404block')
                print(error_404)
                if error_404 != None:
                    result_list['presence'].append('error')
                    result_list['availability'].append('error')
                else:
                    none_avaibitly = avaibitly.find('div', class_='product_delivery')
                    none_avaibitly = none_avaibitly.get_text()
                    print(j)



                    if none_avaibitly != 'Нет в наличии.':
                        result_list['presence'].append(none_avaibitly+ '  ')
                        none_avaibitly = None
                            
                    else:
                        result_list['presence'].append('Нет в наличии.  ')
                        result_list['availability'].append('  ')
                        print('нет в наличии')


                    if none_avaibitly == None:
                        for adress in avaibitly.find_all('div', class_='presence-market'):
                            
                            adress_avai = (adress.ul).get_text()
                            adress_avai = adress_avai.replace('\n', ' ')
                            adress_avai = adress_avai.replace('"Эскор Хайтек-маркет"', ' ')
                            adress_avai = ' '.join(adress_avai.split())
                            print(adress_avai)
                            result_list['availability'].append(adress_avai+'  ')
    """