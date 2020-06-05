import requests, os, wget
from bs4 import BeautifulSoup as bs
from os import path

headers = {"User Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97'}
urlMain = 'https://zerochan.net/'

def download(): # Function to download everything
    imgs = 0 # Amount of images downloaded
    print('Done.')
    access = open('links.txt', 'r+')
    accessLinks = access.readlines()

    print('Downloading...this will definitely take a while.')
    for link in accessLinks:
        if 'https://static.zerochan.net/' in link:
            fileDownload = link.rstrip('\n') # Remove the endline to download images
            wget.download(fileDownload, downloadPath)
            imgs = imgs + 1
    
    access.truncate(0)
    access.close()
    print('\nImages Downloaded: ' + str(imgs))
    print('\nThank you!')
    exit()

def fileCheck(): # Check and take all download links
    print('Done.')
    print('Checking for links...')
    tempCheck = open('temp.txt', 'r+') # Read temporary file
    links = open('links.txt', 'w+') # Storage for download links

    tempRead = tempCheck.readlines()
    for x in tempRead:
        if 'https://static.zerochan.net/' in x: # https://static.zerochan.net/ is the main header for downloadables
            links.write(x)

    tempCheck.truncate(0) # Erase the file contents
    tempCheck.close()
    links.close()
    download()

def runner(): # Find more for other pages until max pages reached
    f = open('temp.txt', 'w+')
    x = 1

    while True:
        x = x + 1
        urlAdd = '?p=' # Extra extension for pages
        urlUse = url + urlAdd + str(x)

        #print(urlUse) # Comment after testing

        page = requests.get(urlUse, headers = headers)
        soup = bs(page.content, 'html.parser')
        link = soup.find_all('a', href=True)

        if x == maxPageCount: # Check if max pages is reached
            f.close()
            fileCheck()
        else: 
            for i in link:
                text = i['href']
                #print(text) # Comment after use
                f.write(text + '\n')

def taker(): # Search the page for downloadable images
    print("Searching " + str(maxPageCount) + " pages.")
    print('Fetching links...this may take a while.')

    f = open('temp.txt', 'w+') # Temporary storage for links
    link_take = soup2.find_all('a', href=True) # Find all download links

    for i in link_take: # For all found a tag links
        text = i['href'] # Separate the ones needed
        #print(text) # Comment after use
        f.write(text + '\n') # And store into file 

    f.close()

    runner()

def page_finder(): # Get the maximum amount of available pages
    extension = search_name.replace(' ', '+') # Replace whitespace with plus sign (+) for search query

    urlUse = urlMain + extension
    global url
    url = urlUse

    #print(urlUse) # Comment after testing

    page = requests.get(urlUse, headers = headers)

    soup = bs(page.content, 'html.parser')
    global soup2 
    soup2 = soup # Basically just reducing the workload for the full program

    linkPage = soup.find('p', class_='pagination').getText()

    # Remove the strings that are not needed
    s1 = linkPage.replace('\n\tpage 1 of ', '')
    s2 = s1.replace('\tNext »\n','')
    count = s2

    print("Max pages found: " + str(count) + " pages")
    max = input("How many do you want to search? ")

    global maxPageCount
    maxPageCount = int(max)

    taker()

def dir(): # Make a new directory where to download
    set_address = path.expanduser('~\\Desktop\\') + search_name # Makes a new directory in Desktop

    global downloadPath
    downloadPath = set_address

    if not path.isdir(set_address): # Check if folder exists, else make a new one
        os.mkdir(set_address)

    #print(set_address) # Comment after testing
    
    page_finder()

def main():
    print("Welcome to the Zerochan Prototype Downloader V3 Rework")
    dirName = input('Who do you want to search? ')

    global search_name
    search_name = dirName

    dir()

main()

# Note to self:
# 1. Check if downloadable pages are available, else throw exception - taker()
# 2.a Check if user input single word and accidentally added space by end of word to throw exception - page_finder()
# 2.b Check if user input single word and accidentally added space by end of word to change url for download - page_finder()
# 2.c Try to find a way to verify url with selenium - page_finder()
# 3. Check if user is connected to internet() - main()
# 4. User must be able to download just one page so add feature - taker() to runner()