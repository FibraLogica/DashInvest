from django.shortcuts import render
from .googlenews import GoogleNews
from dateutil.parser import parse as parse_date

def noticias_financeiras(request):
    # Inicializa o GoogleNews com o idioma e o país desejados
    gn = GoogleNews(lang='pt-PT', country='pt-PT')
    search_query = "Mercado financeiro AND bolsa de valores notícias site:.com"
    search_feed = gn.search(search_query)

    noticias = []

    if search_feed:
        # Ordena as notícias por data de publicação, da mais recente para a mais antiga
        sorted_entries = sorted(search_feed['entries'], key=lambda x: parse_date(x['published']), reverse=True)

        for entry in sorted_entries:
            noticia = {
                'titulo': entry.get('title'),
                'link': entry.get('link'),
                'publicado': entry.get('published'),
                'resumo': entry.get('summary_detail', {}).get('value', 'Sem resumo disponível.'),
            }
            noticias.append(noticia)
        noticias = noticias[:15]
    else:
        print("Não foi possível obter as notícias.")

    # Passa as notícias para o template
    return render(request, 'front_end/noticias_financeiras.html', {'noticias': noticias})

