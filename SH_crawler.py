# -*- coding: utf-8 -*-
"""
Created on Mon Sep 24 15:12:05 2018

@author: zouco
"""

from bc2 import BasicCrawler
import pandas as pd

import time

def refine_wiki_link(link):
    if link.startswith('https://de.wikipedia.org') or link.startswith('https://en.wikipedia.org'):
        return link
    else:
        pieces = link.split('=')
        link = ''
        for piece in pieces[1:]:
            link += piece
        pieces = link.split('&')
        link = pieces[0]
        if link.startswith('https://de.wikipedia.org') or link.startswith('https://en.wikipedia.org'):
            return link
        else:
            print('\n{}\n!!! wrong link !!!\n'.format(link))
            return 'https://www.google.com'
        

def get_revenue_supplier(supplier_name):
        supplier = supplier_name.replace(' ','+') + '+wiki'
        print(supplier)
        
        bc = BasicCrawler(headers='auto')
        search_link = 'https://www.google.com/search?q={}'.format(supplier)
    
        print(search_link)
        
        soup = bc.get_soup(search_link)
        time.sleep(3)
        a = soup.find_all('h3', class_='r')[0]
        link = a.find('a')['href']
        	
        link = refine_wiki_link(link)
        print(link)
      
        
        soup = bc.get_soup(link)
        time.sleep(3)
        
        revenue = None
        if link.startswith('https://de.wikipedia.org'):
            revenue = get_revenue_in_soup_de(soup)
        elif link.startswith('https://en.wikipedia.org'):
            revenue = get_revenue_in_soup_en(soup)
        else:
            print(link)
        
        return revenue
        
        
        
    

def get_revenue_in_soup_de(soup):
    table = soup.select('#Vorlage_Infobox_Unternehmen')
    revenue = None
    if table:
        for row in table[0].find_all('tr'):
            try:
                if str.strip(row.find('td').text) == 'Umsatz':
                        revenue = row.find_all('td')[1].text
                        print(revenue)
            except AttributeError:
                pass
        
    return revenue 



def get_revenue_in_soup_en(soup):
    table = soup.select('#mw-content-text > div > table.infobox.vcard')[0]
    revenue = None
    if table:
        for row in table.find_all('tr'):
            try:
                if str.strip(row.find('th').text) == 'Revenue':
                    revenue = row.find('td').text
                    print(revenue)
            except AttributeError:
                    pass
    return revenue 
    

    
    
    


if __name__ == '__main__':
    
    pd.set_option('max_colwidth',200)
    pd.set_option('max_columns',None) 
    
    suppliers = ["Jabil", "Sanmina", "Thermo Fisher Diagnostics", "IVEK", "Randox Laboratories", "Inpeco", "Nypro", "Carclo", "Bio-Rad Laboratories"]
    
    revenues = []
    for supplier in suppliers:
        revenues.append(get_revenue_supplier(supplier))
    
    result = pd.DataFrame()
    result['supplier']=suppliers
    result['revenue'] = revenues
    
    print(result)
    result.to_csv('SPIDER.csv')
        
        
        
        
        

    