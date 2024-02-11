import requests
import hashlib
import hmac
import time
import certifi
import environ

env = environ.Env()
environ.Env.read_env()

class BinanceClient:
    BASE_URL = 'https://api.binance.com'

    def __init__(self):
        self.api_key = env('BINANCE_API_KEY')
        self.api_secret = env('BINANCE_API_SECRET')
        self.headers = {'X-MBX-APIKEY': self.api_key}
    
    def _get(self, path, params=None, auth_required=False):
        if auth_required:
            if params is None:
                params = {}
            params['timestamp'] = int(time.time() * 1000)
            params['recvWindow'] = 5000
            query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
            signature = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
            full_url = f"{self.BASE_URL}{path}?{query_string}&signature={signature}"
        else:
            if params:
                query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
                full_url = f"{self.BASE_URL}{path}?{query_string}"
            else:
                full_url = f"{self.BASE_URL}{path}"
        try:
            response = requests.get(full_url, headers=self.headers, verify=certifi.where())
            return response
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return None
    
    def connect(self):
        response = self._get('/api/v3/ping')
        if response.status_code == 200:
            print("Conexão com a Binance estabelecida.")
        else:
            print("Falha ao se conectar com a Binance.")

    def get_account_info(self):
        response = self._get('/api/v3/account', auth_required=True)
        return response.json() if response.ok else response.raise_for_status()

    def get_all_coins_info(self):
        response = self._get('/sapi/v1/capital/config/getall', auth_required=True)
        return response.json() if response.ok else response.raise_for_status()

    def get_price(self, symbol):
        if symbol == "USDT":
            return 1.0  # Preço de 1 USDT é sempre 1 USDT
        response = self._get(f'/api/v3/ticker/price?symbol={symbol}USDT')
        if response.ok:
            data = response.json()
            return float(data['price'])
        else:
            print(f"Erro ao buscar preço para {symbol}USDT: {response.text}")
            return None
        
    def get_usdt_to_eur_rate(self):
        response = self._get('/api/v3/ticker/price?symbol=EURUSDT')
        if response.ok:
            data = response.json()
            return 1 / float(data['price'])  # Converte USDT para EUR
        else:
            print(f"Erro ao buscar preço de conversão USDT para EUR: {response.text}")
            return None


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
        else:
            price_in_usdt = binance_client.get_price(coin['coin'])
            if price_in_usdt:
                eur_value = price_in_usdt * float(coin['free']) * usdt_to_eur_rate
            else:
                print(f"Preço para {coin['coin']} em USDT não encontrado.")
    return eur_value