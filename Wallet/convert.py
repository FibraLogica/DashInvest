from .binance_cliente import BinanceClient

def take_coin():
    binance_client = BinanceClient()
    coins = binance_client.get_all_coins_info()
    filtered_coins = [{'name': coin['name'], 'coin': coin['coin'], 'free': coin['free']} for coin in coins if float(coin['free']) > 0]
    return filtered_coins

def convert_coins_to_eur():
    binance_client = BinanceClient()
    usdt_to_eur_rate = binance_client.get_usdt_to_eur_rate()
    coins = take_coin()

    for coin in coins:
        if coin['coin'] == "USDT":
            eur_value = float(coin['free']) * usdt_to_eur_rate
            print(f"{coin['name']}: {coin['free']} USDT = {eur_value} EUR")
        else:
            price_in_usdt = binance_client.get_price(coin['coin'])
            if price_in_usdt:
                eur_value = price_in_usdt * float(coin['free']) * usdt_to_eur_rate
                print(f"{coin['name']} ({coin['coin']}): {coin['free']} x {price_in_usdt} USDT = {eur_value} EUR")
            else:
                print(f"Preço para {coin['coin']} em USDT não encontrado.")
    return eur_value

if __name__ == "__main__":
    convert_coins_to_eur()
