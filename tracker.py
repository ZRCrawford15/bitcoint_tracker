import requests
import time

# global variables
api_key = '1cb0aa8e-b434-48da-8cef-598681ddab8f'
bot_token = '1517396279:AAFddinu0lIo1Ejzl-GQE1WFg0Q4J-b-5FQ'
chat_id = '1621053059'
bitcoin_threshold = 31000
time_interval = 10 * 60  # API request interval in seconds


def get_btc_price():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': api_key}

    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers)
    response_json = response.json()

    # extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    return btc_price['quote']['USD']['price']


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
    price_list = []

    # infinite loop
    while True:
        price = get_btc_price()
        price_list.append(price)

    # if the price falls below threshold, send immediate message
        if price < bitcoin_threshold:
            send_message(chat_id=chat_id, msg=f"BTC Price Drop Alert: {price}")

        if len(price_list) >= 6:
            send_message(chat_id=chat_id, msg=price_list)
            #empty price list
            price_list = []

       # fetch the price for every dash minutes

        time.sleep(time_interval)


if __name__ == '__main__':
    main()
