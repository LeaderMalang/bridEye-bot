# BridEye-bot

## Requirement Statement 
#### Buy: Read token adresses from .txt or .csv file in the same folder and check if the token is found first time or it second if the first time then buy x amount of SOL or lamports. If the token adress was already found or bought before then skip, search for other new token addreses in that .txt or .csv.
#### if the number of watchers increase by +10%, so if watcher were 10 1 minute ago and now its 11, we buy the coin with small size orders and spam 1$ buys. If after 600s there is no new wallets that bought, then dump all the previously bought tokens

#### Sell: if the price increased 100% sell out 50% of wallet total token holdings if the price increased 300% sell out 100% ot token, if the price from entry price went down to -90% take out 100%

#### birdseye  public api for token current price

## Pre req
#### Phantom wallet Extension for chrome .crx type file
#### Phantom recovery pass of length 12 

## How  to Setup 

### Installation
#### create virtual environment
``python -m venv env``
#### Activate virtual environment in Linux
``source env/bin/activate``
#### Activate virtual environment in Windows
``.\env\Scripts\activate``

#### install Requirements
``pip install -r requirements.txt``

#### start bot
``python main.py``


## features
### Developed and tested Features
#### Read and write CSV of token address and update their price and date information
#### Get updated token price and date information
#### Import existing phantom wallet 

### Upoming Features

#### Get increase/decrease percentage of  token price
#### Buy Token on match condition using phantom wallet via jupiter 
#### Sell Token on match condition using phantom wallet via jupiter



