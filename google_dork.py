# from urllib.parse import urlparse

# url = "https://accl.cmu.ac.th"
# parsed_url = urlparse(url)
# path = parsed_url.path

# print(path)  # Output: /2017
from googlesearch import search
import csv
from bs4 import BeautifulSoup, builder
import requests

def google_search(array_query):
    f= open("./google_dork_site.txt","w", encoding='utf-8')
    for query in array_query:
        print(query)
        try:
            # Perform the search using the googlesearch package
            search_results = search(query, pause=0.5)
            
            # Print the link of each result
            for result in search_results:
                print(result)
                f.write(result+'\n')
        except Exception as e:
            print(f"An error occurred: {e}")

# Define your search query

def write_text(site_check):
    with open('keyword.txt','r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for keyword in csv_reader:
            if len(keyword)==0 : continue
            site_check.append(keyword[0].strip())
    return site_check

def query_adding(query,site_check):
    array_query = []
    for key in site_check:
        array_query.append(query + ' '+ key)
    return array_query

def fetch_website_content(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        if response.status_code == 404:
            print(f"Failed to fetch website content. Status code: {response.status_code}, on the website {url}")
            return None
        elif response.status_code == 200:
            return response.text
        else: #! cannot access to website
            print(f"Failed to fetch website content. Status code: {response.status_code}, on the website {url}")
            

            return None
    except Exception as e:
        print(f"Error fetching website content: on the website {url}\n", e)
        return None
    

def write_result(url_found,founding,url_notfound,url_cannot_fetch):
    f = open(f"google_dork_site_result.txt", "w", encoding='utf-8')
    f.write(f"summary: {len(url_found)+ len(url_notfound)+len(url_cannot_fetch) }\n")
    f.write(f"\n[Defacement detected {len(url_found)}]\n")
    if(not url_found): f.write("-\n")
    for i in range(len(url_found)):
        f.write(f"{url_found[i]}\n")
        f.write(f"found: {founding[i]}\n")
    f.write(f"[No defacement detected {len(url_notfound)}]\n")
    if(not url_notfound): f.write("-\n")
    for i in url_notfound:
        f.write(f"{i}\n")
    f.write(f"[Cannot fetch URL {len(url_cannot_fetch)}]\n")
    if(not url_cannot_fetch): f.write("-\n")
    for i in url_cannot_fetch:
        f.write(f"{i}\n")
    f.write("------------------------------------------------------------------")
    print("Finish")

def find_defacement():
    #* Check HTML content variable
    urls_array =[]
    found =[]
    url_found =[]
    founding=[]
    url_notfound =[]
    url_cannot_fetch = []
    #* Passive scan variable
    fetched =set()
    
    try:
        #*if keyword.txt not exits create one
        open('keyword.txt', "x")
        print('keyword.txt does not exits.\nNow it was created please write keyword in file')
        return
    except FileExistsError:
        with open('google_dork_site.txt','r', encoding='utf-8') as urls:
            url_reader = csv.reader(urls)
            
            for url in url_reader:
                if len(url)==0 : continue
                if url in urls_array : continue
                urls_array.append(url[0])
            for url in urls_array:
                found =[]
                website_content = fetch_website_content(url)
                if(website_content == None ): 
                    url_cannot_fetch.append(url)
                    continue
                try:
                    soup = BeautifulSoup(website_content, 'html.parser')
                except builder.ParserRejectedMarkup:
                    continue
                fetched.add(url)
                
                with open('keyword.txt','r', encoding='utf-8') as file:
                    csv_reader = csv.reader(file)
                    for keyword in csv_reader:
                        if len(keyword)==0 : continue
                        if soup.find(string=lambda text: text and keyword[0].strip() in text):
                            found.append(keyword[0].strip())
                    if(found) :
                        print(f"Defacement detected on the website: {url}")
                        print(f'summary keyword that were found : {found}')
                        url_found.append(url)
                        founding.append(found)
                    else : 
                        print(f"No defacement detected on the website: {url}")
                        url_notfound.append(url)
            print(f"Finish")
            write_result(url_found,founding,url_notfound,url_cannot_fetch)

query = "site:*.cmu.ac.th"
array_query = []
site_check =[]
site_check =write_text(site_check)
print (site_check)
array_query=query_adding(query,site_check)
# google_search(array_query)
find_defacement()