import time
import ccxt

exchangesData = {
    "fantom": {
        "apiKey": "",
        "secret": "",
        "transactionFee": 0.001
    },
}

min_spread = 1
min_profit = 0


def main():
    exchanges = [
        "binance",
    ]

    symbols = [
        "WFTM/USDT",
    ]

    min_ask_exchange_id = ""
    min_ask_price = 99999999

    max_bid_exchange_id = ""
    max_bid_price = 0

    exchange_symbol = ""
    max_increase_percentage = 0.0

    for symbol in symbols:
        print("-----------------------------")
        print("Searching for the best opportunity for {0} on {1}".format(
            symbol, exchanges))

        ask_exchange_id, ask_price, bid_exchange_id, bid_price = get_biggest_spread_by_symbol(
            exchanges, symbol)
        increase_percentage = (bid_price - ask_price) / ask_price * 100

        print("[{0} - {1}] - [{2}] - Price Spread: {3:.2}%".format(ask_exchange_id,
                                                                   bid_exchange_id, symbol, increase_percentage))

        if increase_percentage > max_increase_percentage:
            exchange_symbol = symbol
            max_increase_percentage = increase_percentage
            min_ask_exchange_id = ask_exchange_id
            min_ask_price = ask_price
            max_bid_exchange_id = bid_exchange_id
            max_bid_price = bid_price

        if increase_percentage >= min_spread:
            break
    print("-----------------------------")

    if max_increase_percentage > 0:
        print("\n----------Settings-----------")
        ask_amount = get_min_amount(min_ask_exchange_id, exchange_symbol)
        print("Min Ask amount: {0}".format(ask_amount))
        bid_amount = get_min_amount(max_bid_exchange_id, exchange_symbol)
        print("Min Bid amount: {0}".format(bid_amount))
        amount = max(ask_amount, bid_amount)
        print("Actual amount: {0}".format(amount))
        print("Min spread percentage: {0}%".format(min_spread))
        print("Min profit: {0}%".format(min_profit))


        print("[{0} - {1}] - [{2}]: Spread percentage: {3:.2}%".format(min_ask_exchange_id,
                                                                       max_bid_exchange_id, exchange_symbol, max_increase_percentage))

    return ask_exchange_id, min_ask_price, bid_exchange_id, max_bid_price


def get_exchanges_by_symbol(exchanges, symbol_to_find):
    for exchange_id in exchanges:
        exchange = eval("ccxt.{0}()".format(exchange_id))

        exchange.load_markets(True)

        for symbol in exchange.symbols:
            if symbol == symbol_to_find:
                print("{0} - {1} [OK]".format(exchange_id, symbol))


if __name__ == "__main__":
    main()