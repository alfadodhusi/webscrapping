from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

def scrap(url = 'https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019') :
    #This is fuction for scrapping
    url_get = requests.get('https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019')
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    #Find the key to get the information
    table = soup.find('table', attrs={'class':'centerText newsTable2'}) 
    tr = table.find_all('tr') 

    temp = [] #initiating a tuple

    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]
        #use the key to take information here
        #name_of_object = row.find_all(...)[0].text
        
        #get tanggal
        tanggal = row.find_all('td')[0].text
        tanggal = tanggal.strip() #for removing the excess whitespace
    
        #get jual
        jual = row.find_all('td')[1].text
        jual = jual.strip() #for removing the excess whitespace
    
        #get beli
        beli = row.find_all('td')[2].text
        beli = beli.strip() 
    
        temp.append((tanggal,jual,beli)) 
  
    temp = temp[::-1] #remove the header

    df = pd.DataFrame(temp, columns = ('Tanggal','Jual','Beli')) #creating the dataframe
   
   #data wranggling
   
   #change comma into dot
    df.Jual.replace(to_replace = ',',value = '.',regex=True, inplace=True) 
    df.Beli.replace(to_replace = ',',value = '.',regex=True, inplace=True) 
   
   #change language of month
    df.Tanggal.replace(to_replace = 'Oktober',value = 'October',regex=True, inplace=True) 
    df.Tanggal.replace(to_replace = 'Agustus',value = 'August',regex=True, inplace=True) 
    df.Tanggal.replace(to_replace = 'Desember',value = 'December',regex=True, inplace=True) 
    df.Tanggal.replace(to_replace = 'Juli',value = 'July',regex=True, inplace=True) 
    df.Tanggal.replace(to_replace = 'Juni',value = 'June',regex=True, inplace=True) 
    df.Tanggal.replace(to_replace = 'Januari',value = 'January',regex=True, inplace=True) 
    df.Tanggal.replace(to_replace = 'Februari',value = 'February',regex=True, inplace=True) 
    df.Tanggal.replace(to_replace = 'Maret',value = 'March',regex=True, inplace=True) 
    df.Tanggal.replace(to_replace = 'Mei',value = 'May',regex=True, inplace=True) 
   
    #change data type
    df[['Jual','Beli']] = df[['Jual','Beli']].astype('float64')
    
    #create column month
    df['Bulan']=pd.to_datetime(df['Tanggal']).dt.strftime('%b').astype('category')

    #end of data wranggling

    return df

@app.route("/")
def index():
    df = scrap('https://monexnews.com/kurs-valuta-asing.htm?kurs=JPY&searchdatefrom=01-01-2019&searchdateto=31-12-2019') #insert url here

    #This part for rendering matplotlib
    fig = plt.figure(figsize=(5,2),dpi=300)
    df.plot(kind = 'line', x = 'Bulan', y=['Jual','Beli'], title ='Kurs Yen Januari-Desember 2019')
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df, result=result)


if __name__ == "__main__": 
    app.run()
