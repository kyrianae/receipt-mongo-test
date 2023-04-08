from flask import Flask, json, request, Response
import random
import datetime
import requests
import json
from marmiton import Marmiton, RecipeNotFound
from pymongo import MongoClient
import os


mongo_user="kyrianae"
mongo_password="4bqcNAF9Ew0oFXTb"
mongo_instance="mongrosbebe"
# if "mongo_password" not in os.environ:
#     exit(0)

# mongo_password=os.environ["mongo_password"]

# from bs4 import BeautifulSoup

name="receipt_search"
app = Flask(name)
# https://www.marmiton.org/recettes/recherche.aspx?aqt=poulet
# https://www.marmiton.org/recettes/recherche.aspx?aqt=poulet-bas


# https://www.cuisineaz.com/recettes/recherche_terme.aspx?recherche=poulet
sources=[
    # {
    # "name": "marmiton" ,
    # "server": "https://www.marmiton.org",
    # "path": "/recettes/recherche.aspx?aqt=",
    # "substitutions": [
    #     [" ","-"]
    # ]
    # }
    
   {
    "name": "cuisineaz" ,
    "server": "https://www.cuisineaz.com",
    "path": "www.cuisineaz.com/recettes/recherche_terme.aspx?recherche=",
    "substitutions": [
        [" ","+"]
    ]
    }
]

def str_now():
    return str(datetime.datetime.now())

def get_sub_service(server, service):
    url=server+"/"+service
    print (str_now()+"\t"+name +" calls: "+url)
    # carrier = {}
    # TraceContextTextMapPropagator().inject(carrier)
    # header = {"traceparent": carrier["traceparent"]}
    # x = requests.get(url,headers=header)
    x = requests.get(url)
  
    # print (x.text)
    return x.text

# def get_header_from_flask_request(request, key):
#    return request.headers.get_all(key)

class recipe:
    def __init__(self,source,url,title):
        self.url=url
        self.title=title
        self.source=source
    
    def json():
        return json.dump(self)



# bs4
# <a href="/recettes/recette_saute-de-poulet-basquaise-au-wok_40478.aspx" class="MRTN__sc-1gofnyi-2 gACiYG"><div class="MRTN__sc-1cct3mj-1 dSTcmp"><div class="MRTN__sc-1cct3mj-2 kaJbaF"><img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=" data-src="https://assets.afcdn.com/recipe/20130712/734_w190h190c1cx1182cy1456.webp" class="SHRD__sc-dy77ha-0 fotHqj MRTN__sc-1cct3mj-3 hiKnrc lazyload" alt="" width="190" height="190" data-srcset="https://assets.afcdn.com/recipe/20130712/734_w190h190c1cx1182cy1456.webp 1x, https://assets.afcdn.com/recipe/20130712/734_w380h380c1cx1182cy1456.webp 2x" sizes="190px"></div><h4 class="MRTN__sc-30rwkm-0 dJvfhM">Sauté de Poulet Basquaise au wok</h4><div class="MRTN__sc-30rwkm-2 jgaQNE"><div class="SHRD__sc-1q3upxa-1 jxQcRj"><div class="SHRD__sc-1q3upxa-2 egbhkM"><svg class="SHRD__sc-sr6s0j-1 cuxuXS" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M25.155 31.333h-.006c-.456 0-.884-.121-1.253-.333l.012.006-7.827-4.42-7.844 4.42a2.533 2.533 0 0 1-3.664-2.929l-.005.018 2.3-7.629a.2.2 0 0 0-.052-.203l-5.404-5.41a2.482 2.482 0 0 1-.754-1.786c0-.327.063-.64.178-.927l-.006.017a2.511 2.511 0 0 1 2.225-1.625h.006l7.157-.373a.199.199 0 0 0 .168-.121V10.002l3.943-8.205A1.972 1.972 0 0 1 16.11.667h.014-.001a1.968 1.968 0 0 1 1.789 1.152l.005.012 3.832 8.153c.028.081.099.14.185.151h.001l7.157.373a2.535 2.535 0 0 1 1.66 4.321l-5.41 5.404a.2.2 0 0 0-.046.205v-.001l2.283 7.611a2.533 2.533 0 0 1-2.422 3.261z"></path></svg><svg class="SHRD__sc-sr6s0j-1 cuxuXS" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M25.155 31.333h-.006c-.456 0-.884-.121-1.253-.333l.012.006-7.827-4.42-7.844 4.42a2.533 2.533 0 0 1-3.664-2.929l-.005.018 2.3-7.629a.2.2 0 0 0-.052-.203l-5.404-5.41a2.482 2.482 0 0 1-.754-1.786c0-.327.063-.64.178-.927l-.006.017a2.511 2.511 0 0 1 2.225-1.625h.006l7.157-.373a.199.199 0 0 0 .168-.121V10.002l3.943-8.205A1.972 1.972 0 0 1 16.11.667h.014-.001a1.968 1.968 0 0 1 1.789 1.152l.005.012 3.832 8.153c.028.081.099.14.185.151h.001l7.157.373a2.535 2.535 0 0 1 1.66 4.321l-5.41 5.404a.2.2 0 0 0-.046.205v-.001l2.283 7.611a2.533 2.533 0 0 1-2.422 3.261z"></path></svg><svg class="SHRD__sc-sr6s0j-1 cuxuXS" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M25.155 31.333h-.006c-.456 0-.884-.121-1.253-.333l.012.006-7.827-4.42-7.844 4.42a2.533 2.533 0 0 1-3.664-2.929l-.005.018 2.3-7.629a.2.2 0 0 0-.052-.203l-5.404-5.41a2.482 2.482 0 0 1-.754-1.786c0-.327.063-.64.178-.927l-.006.017a2.511 2.511 0 0 1 2.225-1.625h.006l7.157-.373a.199.199 0 0 0 .168-.121V10.002l3.943-8.205A1.972 1.972 0 0 1 16.11.667h.014-.001a1.968 1.968 0 0 1 1.789 1.152l.005.012 3.832 8.153c.028.081.099.14.185.151h.001l7.157.373a2.535 2.535 0 0 1 1.66 4.321l-5.41 5.404a.2.2 0 0 0-.046.205v-.001l2.283 7.611a2.533 2.533 0 0 1-2.422 3.261z"></path></svg><svg class="SHRD__sc-sr6s0j-1 cuxuXS" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M25.155 31.333h-.006c-.456 0-.884-.121-1.253-.333l.012.006-7.827-4.42-7.844 4.42a2.533 2.533 0 0 1-3.664-2.929l-.005.018 2.3-7.629a.2.2 0 0 0-.052-.203l-5.404-5.41a2.482 2.482 0 0 1-.754-1.786c0-.327.063-.64.178-.927l-.006.017a2.511 2.511 0 0 1 2.225-1.625h.006l7.157-.373a.199.199 0 0 0 .168-.121V10.002l3.943-8.205A1.972 1.972 0 0 1 16.11.667h.014-.001a1.968 1.968 0 0 1 1.789 1.152l.005.012 3.832 8.153c.028.081.099.14.185.151h.001l7.157.373a2.535 2.535 0 0 1 1.66 4.321l-5.41 5.404a.2.2 0 0 0-.046.205v-.001l2.283 7.611a2.533 2.533 0 0 1-2.422 3.261z"></path></svg><svg class="SHRD__sc-sr6s0j-2 eHPLKd" xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><path d="M5.43 30.78a2.52 2.52 0 0 1-.839-2.726l-.005.018 2.283-7.606a.2.2 0 0 0-.052-.203l-5.404-5.41a2.482 2.482 0 0 1-.754-1.786c0-.327.063-.64.178-.927l-.006.017a2.512 2.512 0 0 1 2.219-1.625h.006l7.163-.373a.227.227 0 0 0 .186-.15v-.002l3.838-8.176A1.974 1.974 0 0 1 16.036.666h.013a1.97 1.97 0 0 1 1.776 1.118l.005.012 3.919 8.188.002.017-.002.018v-.001a.214.214 0 0 0 .174.122h.001l7.157.373a2.535 2.535 0 0 1 1.66 4.321l-5.41 5.404a.2.2 0 0 0-.046.205v-.001l2.283 7.611a2.533 2.533 0 0 1-3.682 2.905l.013.007-7.815-4.379-7.844 4.42a2.508 2.508 0 0 1-1.244.326c-.6 0-1.151-.209-1.585-.557l.005.004zm10.791-6.819l8.834 5.014a.176.176 0 0 0 .228 0 .18.18 0 0 0 .063-.217v.001l-2.283-7.635a2.517 2.517 0 0 1 .634-2.516l5.404-5.404a.184.184 0 0 0 .046-.216v.001a.18.18 0 0 0-.173-.128h-.008l-7.157-.379a2.514 2.514 0 0 1-2.172-1.481l-.006-.016-3.587-7.53z"></path></svg></div><div class="SHRD__sc-1q3upxa-0 dkNMAE"><span class="SHRD__sc-10plygc-0 jHwZwD">4.8<!-- -->/<!-- -->5</span></div></div><div class="MRTN__sc-30rwkm-3 fyhZvB">(<!-- -->53<!-- --> avis<!-- -->)</div></div></div></a>
@app.route('/search', methods=['GET'])
def search():
    search_param=request.args.get('q')
    # for source in sources:
    #     print (str(source))
    #     search_param=request.args.get('q')
    #     for subst in source['substitutions']:
    #         search_param=search_param.replace(subst[0],subst[1])
        
    #     result = get_sub_service(source['server'], source['path']+search_param)
    #     soup=BeautifulSoup(result, 'html.parser')
    #     l=soup.find_all('article',id='result')
    #     for e in l:
    #         # print (e)
    #         if e.get('href') and e.get('href').startswith("/recettes/"):
    #             print (e)
    #         #    for c in e.children:
    #         #        print (c)
    #     # get_sub_service(hoover, "cook")
        
        
    # Search :
    query_options = {
    "aqt": search_param
    # ,  # Query keywords - separated by a white space
    # "dt": "platprincipal",       # Plate type : "entree", "platprincipal", "accompagnement", "amusegueule", "sauce" (optional)
    # "exp": 2,                    # Plate price : 1 -> Cheap, 2 -> Medium, 3 -> Kind of expensive (optional)
    # "dif": 2,                    # Recipe difficulty : 1 -> Very easy, 2 -> Easy, 3 -> Medium, 4 -> Advanced (optional)
    # "veg": 0,                    # Vegetarien only : 0 -> False, 1 -> True (optional)
    }
    query_result = Marmiton.search(query_options)

    # Get :
    client = MongoClient("mongodb+srv://"+mongo_user+":"+mongo_password+"@"+mongo_instance+".bgg4gde.mongodb.net/?retryWrites=true&w=majority")
    # db = client.test
    db = client.gettingStarted
    if "marmiton" not in db.list_collection_names():
        db.create_collection("marmiton")
    recipes = db.get_collection("marmiton")
    recipes.insert_many(query_result)    
    # for recipe in query_result:
    # # recipe = query_result[0]
    #     # main_recipe_url = recipe['url']

    #     print (recipe)
        
    # try:
    #     detailed_recipe = Marmiton.get(main_recipe_url)  # Get the details of the first returned recipe (most relevant in our case)
    # except RecipeNotFound as e:
    #     print(f"No recipe found for '{query_options['aqt']}'")
    #     import sys
    #     sys.exit(0)  
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
