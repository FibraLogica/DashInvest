from .xtb_cliente import XTBClient
from .binance_cliente import BinanceClient, convert_coins_to_eur
import environ

env = environ.Env()
environ.Env.read_env()

def balance_processor(_request):
    context = {'balance': "Carregando..."}

    # Conexão com a Binance
    binance_client = BinanceClient()
    binance_client.connect()  # Isso deve imprimir "Conexão com a Binance estabelecida." se a conexão for bem-sucedida

    # Conversão de moedas para EUR na Binance
    total_eur_from_binance = convert_coins_to_eur()  # Certifique-se de que convert_coins_to_eur aceite o cliente como argumento

    # Conexão e operações com a XTB
    xtb_client = XTBClient(env('XTB_USER_ID'), env('XTB_PASSWORD'))
    xtb_client.connect()
    login_response = xtb_client.login()
    if login_response.get('status'):
        margin_level_response = xtb_client.get_margin_level()
        if margin_level_response.get('status'):
            xtb_balance_eur = float(margin_level_response['returnData']['balance'])
            total_balance_eur = xtb_balance_eur + total_eur_from_binance
            context['balance'] = f"{total_balance_eur:.2f}"
        else:
            context['balance'] = "Erro ao obter Caixa da XTB"
    else:
        context['balance'] = "Falha no login na XTB"
    xtb_client.disconnect()

    return context
