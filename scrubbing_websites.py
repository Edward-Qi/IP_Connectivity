import requests
import bs4

res = requests.get('https://tools.tracemyip.org/search--city/toronto-%21-ontario')

f = open(r"C:\Users\micha\Documents\GitHub\IP_Connectivity\ip_page.txt", "a+")
f.write(res.text)
f.close()