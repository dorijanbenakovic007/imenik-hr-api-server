import json
import time
import requests
import re

from flask import Flask, jsonify, request
from urllib.parse import quote
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent

app = Flask(__name__)

def detect_operator(phone_number):
    phone_number = re.sub(r'[^\d+]', '', phone_number)
  
    if re.match(r'^3851|^01', phone_number):
        return "Kucni - Zagreb"
    elif re.match(r'^38501|^020', phone_number):
        return "Kucni - Dubrovačko-neretvanska županija"
    elif re.match(r'^38502|^021', phone_number):
        return "Kucni - Splitsko-dalmatinska županija"
    elif re.match(r'^38503|^022', phone_number):
        return "Kucni - Šibensko-kninska županija"
    elif re.match(r'^38504|^023', phone_number):
        return "Kucni - Zadarska županija"
    elif re.match(r'^385031|^031', phone_number):
        return "Kucni - Osječko-baranjska županija"
    elif re.match(r'^385032|^032', phone_number):
        return "Kucni - Vukovarsko-srijemska županija"
    elif re.match(r'^385033|^033', phone_number):
        return "Kucni - Virovitičko-podravska županija"
    elif re.match(r'^385034|^034', phone_number):
        return "Kucni - Požeško-slavonska županija"
    elif re.match(r'^385035|^035', phone_number):
        return "Kucni - Brodsko-posavska županija"
    elif re.match(r'^385040|^040', phone_number):
        return "Kucni - Međimurska županija"
    elif re.match(r'^385042|^042', phone_number):
        return "Kucni - Varaždinska županija"
    elif re.match(r'^385043|^043', phone_number):
        return "Kucni - Bjelovarsko-bilogorska županija"
    elif re.match(r'^385044|^044', phone_number):
        return "Kucni - Sisačko-moslavačka županija"
    elif re.match(r'^385047|^047', phone_number):
        return "Kucni - Karlovačka županija"
    elif re.match(r'^385048|^048', phone_number):
        return "Kucni - Koprivničko-križevačka županija"
    elif re.match(r'^385049|^049', phone_number):
        return "Kucni - Krapinsko-zagorska županija"
    elif re.match(r'^385051|^051', phone_number):
        return "Kucni - Primorsko-goranska županija"
    elif re.match(r'^385052|^052', phone_number):
        return "Kucni - Istarska županija"
    elif re.match(r'^385053|^053', phone_number):
        return "Kucni - Ličko-senjska županija"
    elif re.match(r'^385091|^091', phone_number):
        return "Mobilni - A1 Hrvatska"
    elif re.match(r'^385092|^092', phone_number):
        return "Mobilni - Tomato"
    elif re.match(r'^385095|^095', phone_number):
        return "Mobilni - Telemach"
    elif re.match(r'^385097|^097', phone_number):
        return "Mobilni - bonbon"
    elif re.match(r'^385098|^098|^099', phone_number):
        return "Mobilni - Hrvatski Telekom"
    elif re.match(r'^3850800', phone_number):
        return "Besplatni pozivni brojevi"
    elif re.match(r'^385060', phone_number):
        return "Komercijalni telefonski pozivni brojevi"
    elif re.match(r'^385061', phone_number):
        return "Usluga glasovanja telefonom"
    elif re.match(r'^385064', phone_number):
        return "Usluge sa sadržajem neprimjerenim za djecu"
    elif re.match(r'^385065', phone_number):
        return "Usluge nagradnih igara"
    elif re.match(r'^385069', phone_number):
        return "Usluge namijenjene djeci"
    elif re.match(r'^385072', phone_number):
        return "Jedinstveni pristupni broj za cijelu državu za posebne usluge"
    else:
        return "Unknown Operator"

def scrap_url(input,page_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--proxy-server=socks5://127.0.0.1:9150") Tor proxy

    user_agent = UserAgent()
    chrome_options.add_argument(f"--user-agent={user_agent.random}")
    driver = webdriver.Chrome(executable_path='/chromedriver', options=chrome_options)

    encoded_name = quote(input)
    search_url = f"https://www.imenik.hr/imenik/trazi/{page_id}/Osobe/sve/sve/vaznost/{encoded_name}.html"

    driver.get(search_url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    not_found_element = soup.select_one('p:contains("Nije pronađen niti jedan rezultat za upit")')
    if not_found_element:
        return []           


    items = soup.select('div.rez_item')
    entries = []
    for item in items:
        profile_link = item.select_one('div.telefon a[href^="/imenik/"]')['href']
        profile_id = profile_link.split('/')[2]
        encoded_profile_id = quote(profile_link.split('/').pop().replace('.html', ''))
        profile_url = f"https://www.imenik.hr/imenik/{profile_id}/detalji/{encoded_profile_id}.html"

        driver.get(profile_url)

        profile_html = driver.page_source
        profile_soup = BeautifulSoup(profile_html, 'html.parser')
        try:
            phone_number = profile_soup.select_one('td.data_tel').get_text(strip=True)
            address = profile_soup.select_one('div.adresa_detalj').get_text(strip=True)
            name = profile_soup.select_one('div.tab_naslova').get_text(strip=True)
            operater = detect_operator(phone_number)
            entry = {'full_name': name, 'phone_number': phone_number, 'address': address, 'operater': operater, 'profile_url': profile_url}
            print(f"Added {entry}")
            entries.append(entry)    
        except Exception as e:
            print(f"Skipping because of corrupted data")
            continue
            
    return entries

@app.route('/contacts', methods=['POST'])
def contacts():
    input_data = request.json['input']
    page_id_data = request.json['page_id'] or 1
    entries = scrap_url(input_data, page_id_data)
    return jsonify(entries)


if __name__ == '__main__':
    app.run() 