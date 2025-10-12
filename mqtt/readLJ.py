import bs4 as bs
import urllib.request

# current temperature and humidity
# 1.11.2025

def getTemp():
    url = "https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.html"
    outT = ""
    outH = ""
    count = 0
    while count < 2 and not outT:
        try:
            count += 1
            source = urllib.request.urlopen(url).read()
            soup = bs.BeautifulSoup(source,features="html.parser")
            table = soup.find('table')
            table_rows = table.find_all('tr')
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i  in td]
                if len(row) > 0 and row[0] == "Ljubljana - Vič":
                    #print(row[0], row[2])
                    outT = row[2]
                    outH = row[3]
                    break
        except Exception as err:
            print(f"readLJ {err} {type(err)}")

    url = "http://hmljn.arso.gov.si/zrak/kakovost%20zraka/podatki/dnevne_koncentracije.html"
    outP10 = ""
    outP25 = ""
    count = 0
    while count < 2 and not outP10:
        try:
            count += 1
            source = urllib.request.urlopen(url).read()
            soup = bs.BeautifulSoup(source,features="html.parser")
            tables = soup.find_all('table', class_="online")
            for table in tables:
                table_rows = table.find_all('tr')
                for tr in table_rows:
                    td = tr.find_all('td')
                    row = [i.text for i  in td]
                    if len(row) > 0 and row[0] == "LJ Vič":
                        print(row[0], row[1], row[2])
                        outP10 = row[1]
                        outP25 = row[2]
                        break
        except Exception as err:
            print(f"readLJ {err} {type(err)}")

    return(outT, outH, outP10, outP25)

#print(getTemp())
