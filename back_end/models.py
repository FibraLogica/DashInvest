from django.db import models

class Ativo(models.Model):
    TIPO_CHOICES = (
        ('ACAO', 'Ação'),
        ('ETF', 'ETF'),
        ('FII', 'Fundo Imobiliário'),
        # Adicione mais conforme necessário
    )
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=4, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    preco_medio = models.DecimalField(max_digits=10, decimal_places=2)
    # Pode adicionar mais campos conforme necessário

    def __str__(self):
        return f"{self.nome} ({self.tipo})"

class Transacao(models.Model):
    ativo = models.ForeignKey(Ativo, on_delete=models.CASCADE)
    data_transacao = models.DateField()
    tipo = models.CharField(max_length=10, choices=(('COMPRA', 'Compra'), ('VENDA', 'Venda')))
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo} de {self.quantidade} x {self.ativo.nome} em {self.data_transacao}"
