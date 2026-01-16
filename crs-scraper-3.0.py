# This scrapes an acad year and sem. Then turns it into a .csv file. Then, starts comparing past and present continuously.
from requests import get
import os
import shutil
import datetime
from pandas import read_html
from time import time
from time import sleep
from subprocess import run
from filecmp import cmp
from io import StringIO

start_time = time()
now = datetime.datetime.now()
generationdate=now.strftime("%Y-%m-%d--%H-%M-%S")
letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
letters=list(letters)

os.mkdir('Scraper-3.0-Results '+generationdate)
os.chdir(os.getcwd()+"\\"+('Scraper-3.0-Results '+generationdate))

def ScrapeIt(year,sem,generationdate,iteration):
    letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    letters=list(letters)
    
    for x in range(0,26):
        currLetterWebpage=get("https://crs.upd.edu.ph/schedule/1"+year+sem+"/"+letters[x])       
        currentHTML=read_html(StringIO(currLetterWebpage.text))
        currentTable=currentHTML[0]
        if(x!=0):
            currentTable.to_csv(('AllSince'+str(iteration)+'.csv'), mode='a', index=False, header=False)
        else:
            currentTable.to_csv(('AllSince'+str(iteration)+'.csv'), mode='a', index=False, header=True)
    filename=('AllSince'+str(iteration)+'.csv')
    return filename

i=0

initialFile=ScrapeIt("2025","2",generationdate,i) # change year and sem here. The ones in quotes
differencesSinceGenerationDate=[]
differencesSinceLastIteration=[] 
print("Done scraping CRS regular classes as of opening the file!")
while True:
    if(i!=0):
        prevIter=ScrapeIt("2025","2",generationdate,i)
    else:
        prevIter=initialFile
        
    sleep(500)
    
    i+=1   
    
    currIter=ScrapeIt("2025","2",generationdate,i)
    nowWithinLoop = datetime.datetime.now()
    NowWithinLoop =nowWithinLoop.strftime("%Y-%m-%d--%H-%M-%S")

    # Shows differences since the generation date
    differencesSinceGenerationDate.append(f"{i}differencesAsOf--{NowWithinLoop}.html")
    command=[
        "daff",
        "--act",
        "update",
        "--output", 
        f"{i}differencesAsOf--{NowWithinLoop}.html", 
        initialFile, 
        currIter
    ]
    run(command,shell=True)

    # Shows differences since last iteration
    
    differencesSinceLastIteration.append(f"{i}differencesSinceLastIteration.html")
    command=[
        "daff",
        "--act",
        "update",
        "--output", 
        f"{i}differencesSinceLastIteration.html", 
        prevIter, 
        currIter
    ]
    run(command,shell=True)
    
    if (i!=1):
        pathtoOneGen=os.getcwd()+"\\"+differencesSinceGenerationDate[i-1]
        pathtoTwoGen=os.getcwd()+"\\"+differencesSinceGenerationDate[i-2]
        fileComparisonGen=cmp(pathtoOneGen,pathtoTwoGen,shallow=False)

        pathtoOneIter=os.getcwd()+"\\"+differencesSinceLastIteration[i-1]
        pathtoTwoIter=os.getcwd()+"\\"+differencesSinceLastIteration[i-2]
        fileComparisonIter=cmp(pathtoOneIter,pathtoTwoIter,shallow=False)
        
        if fileComparisonGen==False:
            #print("Since the generation date, something new has been added! Check the file:", differencesSinceGenerationDate[i-1])
            if fileComparisonIter==False:
                print("Something changed. What has been changed since last *iteration* is in:",differencesSinceLastIteration[i-1])
                print("Check LatestChange.html for the latest change")
                shutil.copy2(differencesSinceLastIteration[i-1],"LatestChange.html")
            else:
                print("Nothing has changed since last iteration")
                print("Check LatestChange.html for the latest change")
        else:
            print("Nothing changed.")
    else:
        print("At first iteration, there be nothing to compare difference to...")

