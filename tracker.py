import requests
import time

# global variables
api_key = *****************************
bot_token = *****************************
chat_id = **********
bitcoin_threshold = 30000
time_interval = 5 * 300  # API request interval in seconds
xrp_threshold = 0.30
eth_threshold = 1150
xlm_threshold = .30

# def get_price_data():
#     """
#     Retrieves the price JSON data from coinmarketcap api
#     :return: JSON data
#     """
#     url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
#     headers = {'Accepts': 'application/json',
#                'X-CMC_PRO_API_KEY': api_key}
#
#     # make a request to the coinmarketcap api
#     response = requests.get(url, headers=headers)
#     response_json = response.json()
#     return response_json


def get_btc_price(price_data):

    # extract the bitcoin price from the json data
    btc_price = price_data['data'][0]
    return btc_price['quote']['USD']['price']


def get_xlm_price(price_data):


    # extract xlm price
    xlm_price = price_data['data'][10]
    return xlm_price['quote']['USD']['price']


def get_eth_price(price_data):
    """
    Gets the price of ETH
    :return: ETH Price
    """

    eth_price = price_data['data'][1]
    return eth_price['quote']['USD']['price']


def get_xrp_price(price_data):
    """
    Gets the price of XRP
    :return: XRP Price
    """

    xrp_price = price_data['data'][3]
    return xrp_price['quote']['USD']['price']


def send_message(chat_id, msg):
    """
    Sends a message through telegram
    :param chat_id: Chat ID to send message to
    :param msg: message contents
    :return None
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"

    # send the message
    requests.get(url)


def main():
    btc_price_list = []
    xrp_price_list = []
    eth_price_list = []
    xlm_price_list = []

    # infinite loop
    while True:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {'Accepts': 'application/json',
                   'X-CMC_PRO_API_KEY': api_key}

        # make a request to the coinmarketcap api
        response = requests.get(url, headers=headers)
        response_json = response.json()


        # BTC
        price = get_btc_price(response_json)
        btc_price_list.append(price)

        # if the price falls below threshold, send immediate message
        if price < bitcoin_threshold:
            send_message(chat_id=chat_id, msg=f"BTC Price Drop Alert: {price}")

        # XRP
        xrp_price = get_xrp_price(response_json)
        xrp_price_list.append(xrp_price)

        if xrp_price < xrp_threshold:
            send_message(chat_id=chat_id, msg=f"XRP Price Drop Alert {xrp_price}")

        # ETH
        eth_price = get_eth_price(response_json)
        eth_price_list.append(eth_price)

        if eth_price < eth_threshold:
            send_message(chat_id=chat_id, msg=f"ETH Price Drop Alert {eth_price}")

        # Stellar Lumens (XLM)
        xlm_price = get_xlm_price(response_json)
        xlm_price_list.append(xlm_price)

        if xlm_price < xlm_threshold:
            send_message(chat_id=chat_id, msg=f"Stellar Lumen Price Drop Alert {xlm_price}")


        # Sends update for each coin every 30 minutes
        if len(btc_price_list) >= 1:
            send_message(chat_id=chat_id, msg=btc_price_list)
            send_message(chat_id=chat_id, msg=xrp_price_list)
            send_message(chat_id=chat_id, msg=eth_price_list)
            send_message(chat_id=chat_id, msg=xrp_price_list)
            # empty price list
            btc_price_list = []
            xrp_price_list = []
            eth_price_list = []
            xlm_price_list = []

        # fetch the price for every dash minutes

        time.sleep(time_interval)


if __name__ == '__main__':
    main()
