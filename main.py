import requests
from bs4 import BeautifulSoup
import telegram
import linecache

api_key = '5541825850:AAGldFcgZBndMJ4_g3uasLVWoEloBpQ9mZo'
user_id = '1011416325'

bot = telegram.Bot(token=api_key)

productID = '81' #should may change everyday, but not a problem at all as their backend automatically redirect to the correct URL

class Article:
    def __init__(self, title, price, pricebefore, details, leftpieces):
        self.title = title
        self.price = price
        self.pricebefore = pricebefore
        self.details = details
        self.leftpieces = leftpieces

def getProductDetailFromURL(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    html = list(soup.children)[1]
    body = list(html.children)[1]
    productDetail = body.find('article', class_='liveshoppingbigProduct')
    
    return productDetail

def getPrice(productDetail):
    price = productDetail.find('span', class_='knEJvu')
    pprice = price.find('strong').getText()
    return pprice.strip()

def getTitle(productDetail):
    title = productDetail.find('div', class_='bwiRGz').getText()
    return title

def getLeftPieces(productDetail):
    leftpieces = productDetail.find('div', class_='CLA-dF').getText()
    return leftpieces.strip()

def getArticle(url):
    productDetail = getProductDetailFromURL(url)
    title = getTitle(productDetail)
    price = getPrice(productDetail)
    leftpieces = getLeftPieces(productDetail)
    return Article(title, price, leftpieces)

def getPriceBefore(productDetail):
    pricebefore = productDetail.find('span', class_='knEJvu')
    ppricebefore = pricebefore.find('span', class_='lpcYSf').getText()
    return ppricebefore

def getDetails(productDetail):
    details = productDetail.find('span', class_='fYwkNp').getText()
    return details

def buildURL(url):
    url = 'https://www.digitec.ch/fr/liveshopping/'+productID+'/'
    return url

def lineReturn():
    print("\n")

def hashTags():
    print("############################################################")
    
def buildArticle(url):
    productDetail = getProductDetailFromURL(url)
    title = getTitle(productDetail)
    price = getPrice(productDetail)
    pricebefore = getPriceBefore(productDetail)
    details = getDetails(productDetail)
    leftpieces = getLeftPieces(productDetail)
    
    return Article(title, price, pricebefore, details, leftpieces)

article = buildArticle(buildURL(productID))

# print(products) in a local file named out.txt -> The file is opened in "a+" mode (append and read/write) and the file is created if it does not exist. If the file exists, it is opened in append mode. The file pointer is positioned at the end of the file. This is the default mode.
with open('out.txt', 'a+') as f:
    print(article.title, file=f)
    print(article.price, file=f)
    print(article.pricebefore, file=f)
    print(article.details, file=f)
    print(article.leftpieces, file=f)
    print('####################', file=f)
    
#print in the console the content of the file
print("Title: " + article.title + "\n" + "Price: " + article.price + "\n" + "Price before: " + article.pricebefore + "\n" + "Details: " + article.details + "\n" + "Left pieces: " + article.leftpieces + "\n" + "URL: " + buildURL(productID))

#send the message to the user with the bot API and the user ID (the user ID is the same as the Telegram ID) and the message (the message is the content of the file out.txt) and the parse_mode is set to HTML to allow the bot to send the message in HTML format (the message is in HTML format) and the disable_web_page_preview is set to True to disable the preview of the web page (the preview is disabled) and the disable_notification is set to True to disable the notification of the message (the notification is disabled) 
bot.send_message(chat_id=user_id, text="📣\t Digitec daily offer \t📣" + "\n\n" + "Article: " + article.title + "\n" + "Price: " + article.price + "\n" + "Price before: " + article.pricebefore + "\n" + "Details: " + article.details + "\n" + "Left pieces: " + article.leftpieces + "\n" + "URL: " + buildURL(productID))
    