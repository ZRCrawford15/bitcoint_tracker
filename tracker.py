import requests
import time

# global variables
api_key = '**********************************'
bot_token = '*******************************'
chat_id = '********'
bitcoin_threshold = 3000
time_interval = 10 * 175  # API request every 15 minutes
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
    """
    Gets the price of bitcoin from the JSON
    :param price_data: JSON data
    :return: BTC price
    """
    # extract the bitcoin price from the json data
    btc_price = price_data['data'][0]
    return btc_price['quote']['USD']['price']


def get_xlm_price(price_data):
    """
    Gets the price of Stellar Lumen
    :param price_data: JSON Data
    :return: XLM price
    """

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


def price_change(coin_price: list):
    """
    Take a list of 2 prices and calculates how much it has changed
    :param coin_price: Price list
    :return: Price change
    """


    if len(coin_price) > 1:
        return coin_price[1] - coin_price[0]

    else:
        return 0

def format_decimal(coin_amount: int):
    return "{:.2f}".format(coin_amount)

def main():
    btc_price_list = []
    xrp_price_list = []
    eth_price_list = []
    xlm_price_list = []
    btc_change, xrp_change, eth_change, xlm_change = 0, 0, 0, 0

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
        btc_change = price_change(btc_price_list)

        # if the price falls below threshold, send immediate message
        if price < bitcoin_threshold:
            send_message(chat_id=chat_id, msg=f"BTC Price Drop Alert: {price}")

        # XRP
        xrp_price = get_xrp_price(response_json)
        xrp_price_list.append(xrp_price)
        xrp_change = price_change(xrp_price_list)

        if xrp_price < xrp_threshold:
            send_message(chat_id=chat_id, msg=f"XRP Price Drop Alert {xrp_price}")

        # ETH
        eth_price = get_eth_price(response_json)
        eth_price_list.append(eth_price)
        eth_change = price_change(eth_price_list)

        if eth_price < eth_threshold:
            send_message(chat_id=chat_id, msg=f"ETH Price Drop Alert {eth_price}")

        # Stellar Lumens (XLM)
        xlm_price = get_xlm_price(response_json)
        xlm_price_list.append(xlm_price)
        xlm_change = price_change(xlm_price_list)

        if xlm_price < xlm_threshold:
            send_message(chat_id=chat_id, msg=f"Stellar Lumen Price Drop Alert {xlm_price}")


        # Sends update for each coin every 30 minutes
        if len(btc_price_list) >= 2:
            formatted_btc = format_decimal(btc_price_list[1])
            formatted_btc_change = format_decimal(btc_change)

            send_message(chat_id=chat_id, msg=f"Bitcoin price: {formatted_btc} **** Change amount: {formatted_btc_change}"
                                              f"\nETH price: {format_decimal(eth_price_list[1])} **** Change amount: {format_decimal(eth_change)}"
                                              f"\nXLM price: {format_decimal(xlm_price_list[1])} **** Change amount: {format_decimal(xlm_change)}"
                                              f"\nXRP price: {format_decimal(xrp_price_list[1])} **** Change amount: {format_decimal(xrp_change)}")

            # empty price list
            btc_price_list = []
            xrp_price_list = []
            eth_price_list = []
            xlm_price_list = []

        # fetch the price for every dash minutes

        time.sleep(time_interval)


if __name__ == '__main__':
    main()
