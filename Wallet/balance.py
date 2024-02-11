from .xtb_cliente import XTBClient
from .convert import convert_coins_to_eur
import environ

env = environ.Env()
environ.Env.read_env()

def balance_processor(_request):
    context = {'balance': "Carregando..."}

    total_eur_from_binance = convert_coins_to_eur()

    client = XTBClient(env('XTB_USER_ID'), env('XTB_PASSWORD'))
    client.connect()

    login_response = client.login() 
    if login_response.get('status'):
        margin_level_response = client.get_margin_level()
        if margin_level_response.get('status'):
            xtb_balance_eur = float(margin_level_response['returnData']['balance'])
            total_balance_eur = xtb_balance_eur + total_eur_from_binance
            context['balance'] = f"{total_balance_eur:.2f}"
        else:
            context['balance'] = "Erro ao obter Caixa"
    else:
        context['balance'] = "Falha no login"
    client.disconnect()

    return context

    