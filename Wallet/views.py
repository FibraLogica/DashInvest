from django.shortcuts import render
from .xtb_cliente import XTBClient
from .binance_cliente import BinanceClient
import environ

env = environ.Env()
environ.Env.read_env()

def carteira_view(request):
    # Parte da Binance
    binance_client = BinanceClient()
    account_info = binance_client.get_account_info()
    usdt_to_eur_rate = binance_client.get_usdt_to_eur_rate()
    cripto_data = []

    for asset in account_info['balances']:
        if float(asset['free']) > 0:
            price_in_usdt = binance_client.get_price(asset['asset'])
            if price_in_usdt:
                price_in_eur = price_in_usdt * usdt_to_eur_rate
                saldo_em_eur = float(asset['free']) * price_in_eur
                cripto_data.append({
                    'nome_do_ativo': asset['asset'],
                    'quantidade': asset['free'],
                    'valor_atual': saldo_em_eur,
                    'corretora': 'Binance',
                    'tipo_ativo': 'Criptomoeda',
                })
    # # Parte da XTB
    # user_id = env('XTB_USER_ID')
    # password = env('XTB_PASSWORD')
    # xtb_client = XTBClient(user_id=user_id, password=password)
    # xtb_client.connect()
    # login_response = xtb_client.login()
    # xtb_data = []

    # if login_response.get('status'):
    #     raw_carteira_data = xtb_client.get_current_user_symbols()
    #     if 'returnData' in raw_carteira_data and isinstance(raw_carteira_data['returnData'], list):
    #         for asset in raw_carteira_data['returnData']:
    #             xtb_data.append({
    #                 'nome_do_ativo': asset['symbol'],
    #             })
    # else:
    #     print("Falha no login da XTB")

    # xtb_client.disconnect()

    # Combina os dados da Binance e da XTB
    carteira_data = cripto_data
    return render(request, 'front_end/carteira.html', {'carteira_data': carteira_data})
