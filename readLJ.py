import bs4 as bs
import urllib.request

# current temperatue

def getTemp():
    url = "https://meteo.arso.gov.si/uploads/probase/www/observ/surface/text/sl/observationAms_si_latest.html"
    out = ""
    try:
        source = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(source,features="html.parser")
        table = soup.find('table')
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i  in td]
            if len(row) > 0 and row[0] == "Ljubljana":
                #print(row[0], row[2])
                out = row[2]
                break
    except Exception as err:
        print(f"readLJ {err} {type(err)}")
    return(out)

# print(getTemp())
