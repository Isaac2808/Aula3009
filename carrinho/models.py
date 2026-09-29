from django.db import models


class Produto(models.Model):

    nome = models.CharField(max_length=150)

    categoria = models.CharField(max_length=100)

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantidade = models.PositiveIntegerField()

    descricao = models.TextField()

    imagem = models.ImageField(
        upload_to='produtos/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.nome
# Create your models here.
