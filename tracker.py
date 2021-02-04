import requests
import time
import json

# global variables
api_key = '************************************'
bot_token = '**********************************'
chat_id = '*******'
BITCOIN_THRESHOLD = 3000
time_interval = 10 * 175  # API request every 15 minutes
XRP_THRESHOLD = 0.30
ETH_THRESHOLD = 1150
XLM_THRESHOLD = .30


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

# def get_btc_price(price_data):
#     """
#     Gets the price of bitcoin from the JSON
#     :param price_data: JSON data
#     :return: BTC price
#     """
#     # extract the bitcoin price from the json data
#     btc_price = price_data['data'][0]
#     return btc_price['quote']['USD']['price'], btc_price['quote']['USD']['percent_change_1h']


class Coin:
    """
    Class for a new coin
    """

    def __init__(self, price_data, coin_name: str):
        """
        Creates a new coin object
        :param coin_name: Name of coin `str`
        """
        self._coin_name = coin_name
        self._value = 0
        self._change_percentage = 0
        self._price_data = price_data
        self._dict_key = 0


    def get_dict_key(self, coin_name):
        """
        Value is the dictionary key for the coin
        :param coin_name: `str` coin name
        :return: Dictionary key
        """
        val = 0
        try:
            for coin in self._price_data['data']:
                if coin['name'] == coin_name:
                    self._dict_key = val
                    return val
                val += 1

        except KeyError:
            print("Coin not found")

        return None


    def get_coin_name(self):
        return self._coin_name


    def get_coin_value(self):
        coin_value = self._price_data['data'][self._dict_key]
        self._value = coin_value['quote']['USD']['price']
        return self._value


    def get_change_percentage(self):
        coin_value = self._price_data['data'][self._dict_key]
        self._change_percentage = coin_value['quote']['USD']['percent_change_1h']
        return self._change_percentage


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
    return "{:.3f}".format(coin_amount)


def main():
    btc_price_list = []
    xrp_price_list = []
    eth_price_list = []
    xlm_price_list = []
    doge_price_list = []

    # infinite loop
    while True:
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        headers = {'Accepts': 'application/json',
                   'X-CMC_PRO_API_KEY': api_key}

        # make a request to the coinmarketcap api
        response = requests.get(url, headers=headers)
        response_json = response.json()

        # BitCoin
        btc = Coin(response_json, "Bitcoin")
        btc.get_dict_key("Bitcoin")
        btc_price_list.append(btc.get_coin_value())

        # Ethereum
        eth = Coin(response_json, "Ethereum")
        eth.get_dict_key("Ethereum")
        eth_price_list.append(eth.get_coin_value())


        # Stellar Lumen
        xlm = Coin(response_json, "Stellar")
        xlm.get_dict_key("Stellar")
        xlm_price_list.append(xlm.get_coin_value())
        # doge
        doge = Coin(response_json, "Dogecoin")
        doge.get_dict_key("Dogecoin")
        doge_price_list.append(doge.get_coin_value())

        # Sends update for each coin every 30 minutes
        if len(btc_price_list) >= 1:
            send_message(chat_id=chat_id,
                         msg=f"Bitcoin price: {format_decimal(btc.get_coin_value())} --- BTC changed {format_decimal(btc.get_change_percentage())}% in the last hour"
                             f"\n\nETH price: {format_decimal(eth.get_coin_value())} --- ETH changed {format_decimal(eth.get_change_percentage())}% in the last hour"
                             f"\n\nXLM price: {format_decimal(xlm.get_coin_value())} --- XLM changed {format_decimal(xlm.get_change_percentage())}% in the last hour"
                             f"\n\nDoge price: {format_decimal(doge.get_coin_value())} --- Doge changed {format_decimal(doge.get_change_percentage())}% in the last hour")


        # # write data to JSON
        data_dictionary = {'coins': [{'btc': btc_price_list},
                                     {'eth': xrp_price_list},
                                     {'xlm': eth_price_list},
                                     {'xrp': xlm_price_list},
                                     {'doge': doge_price_list}]}

        with open("test_file.json", 'w') as file:
            json.dump(data_dictionary, file)

        # fetch the price for every dash minutes

        time.sleep(time_interval)


if __name__ == '__main__':
    main()
