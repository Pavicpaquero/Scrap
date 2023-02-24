import requests
from bs4 import BeautifulSoup
import csv
import re

url = "https://barreau-caen.com"
uri = "/annuaire-des-avocats/lettre/"
lettres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "V", "W", "X",
           "Y", "Z"]
nbPg = 20


def getlink(url,nbPg):
    urls = []
    for page in range(nbPg):
        urls.append(url + lettres[int(page)])
    return urls


def swoup(url):
    response = requests.get(url)
    if response.ok:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    else:
        print("ERROR: Failed Connect on :" + str(url))
        return False


def getinfo(div):
    try:
        title = div.find("span", class_="fn n notranslate")
        rue = div.find("span", class_="address-block")
        numPro = div.find("span", class_="tel cn-phone-number cn-phone-number-type-workphone")
        numFax = div.find("span", class_="tel cn-phone-number cn-phone-number-type-workfax")
        mail = div.find("span", class_="email-address")
        list =[title,rue,numPro,numFax,mail]

        if title is None:
            title = ""

        if rue is None:
            rue = ""

        if numPro is None:
            numPro = ""

        if numFax is None:
            numFax = ""

        if mail is None:
            mail = ""
        return list
    except AttributeError:
        return None


def main():
    links = getlink(url + uri, nbPg+1)
    informa = []
    for link in links:
        soup = swoup(link)
        divs = soup.findAll("div", class_="cn-list-row cn-list-item vcard individual avocats-generalistes")
        for div in divs:
            row = getinfo(div)
            print(row)
            if row is not None:
                informa.append(row)

    with open('informa.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nom', 'Adresse', 'Numéro de téléphone professionnel', 'Numéro de fax', 'Adresse e-mail'])
        writer.writerows(informa)


main()
