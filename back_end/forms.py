from django.forms import ModelForm
from .models import Ativo

class AtivoForm(ModelForm):
    class Meta:
        model = Ativo
        fields = ['nome', 'tipo', 'quantidade', 'preco_medio']  # Adicione ou remova campos conforme necessário