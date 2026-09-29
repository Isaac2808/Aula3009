from django.db import models


class Produto(models.Model):

    nome = models.CharField(
        max_length=150,
        verbose_name='Nome'
    )

    categoria = models.CharField(
        max_length=100,
        verbose_name='Categoria'
    )

    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Preço'
    )

    quantidade = models.PositiveIntegerField(
        default=0,
        verbose_name='Quantidade em Estoque'
    )

    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )

    imagem = models.ImageField(
        upload_to='produtos/',
        blank=True,
        null=True,
        verbose_name='Imagem'
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    atualizado_em = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

        ordering = [
            '-criado_em'
        ]

    def __str__(self):

        return f'{self.nome} - R$ {self.preco}'