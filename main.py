import helpers as help 
import bitcoinlib as btc
import requests as re
import os, os.path as p
from flask import Flask,request
from random import randint
import os.path
from yahoo_fin import stock_info as si

app = Flask(__name__)


#path to current directory
path = os.path.curdir
bypassKeys = False #When enabled you don't need to provide a license key. If configured to True a license key must be provided in the parameters.
keyLength = 64 #The length of the license key.
keyTokens = 1000 #The default uses of a license key.

#Token Costs. This area highlights how much a request will cost
tokenCosts = {'4', '1000'}
def runAuth(key, option):
    if bypassKeys == False:
        with open(f"{path}/keys/{key}/tokens", "r") as f: #gets user's tokens
            tokens = int(f.read())
            token2 = tokens - list(tokenCosts)[int(option)]

        if token2 <= 0: #checks if the user has enough tokens
            return False
        else:
            return True
    
@app.route('/create', methods=['GET'])
def createKey():
    #generate random 64 number license key
    apiKey = ''.join([str(randint(0, 9)) for _ in range(64)])
    masterKey = ''.join([str(randint(0, 9)) for _ in range(128)])
    os.mkdir(f"{path}/keys/{apiKey}")
    with open(f"{path}/keys/{apiKey}/masterkey", "w") as f: #writes master key file.
        f.write(masterKey)
    with open(f"{path}/keys/{apiKey}/tokens", "w") as f: #write tokens file
        f.write(str(keyTokens))
    return f"<p>Succesfully Created Key: {apiKey}</p><p>Master Key: {masterKey}</p>Credits: 1000"

@app.route("/")
def index():
    toReturn = """
        #
    """
@app.route("/price", methods=['GET'])
def price():

    coin = request.args['coin']
    coin = coin.upper()

    currency = request.args['currency']
    currency = currency.upper()
    
    key = request.args['key']
    boolt = runAuth(key, list(tokenCosts)[1]) #RUNS AUTHENTICATION
    if boolt == False:
        return "Error: Insufficient Tokens"
        

    #^^^Gets Arguments
    if currency == "ALL":
        
        count = 0
        allCurr = {'USD', 'GBP', 'EUR'}
        after1 = {}
        for curr in allCurr:
            latest_price = si.get_live_price(f'{coin}-{curr}')
            
            after1[curr] = f"{latest_price:.2f}"
        return after1    
    else:
        ticker = f"{coin}-{currency}"

        latest_price = si.get_live_price(ticker)

        return f"{latest_price:.2f}"

if __name__ == "__main__":
    app.run(port=6070, debug=True)
#get current price of bitcoin
