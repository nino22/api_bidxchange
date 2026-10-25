from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Conta(models.Model):
    nomeCompleto = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True) 
    razaoSocial = models.CharField(max_length=100)
    nomeFantasia = models.CharField(max_length=100, blank=True, null=True, unique=True) 
    cnpj = models.CharField(max_length=20, unique=True)
    telefone = models.DecimalField(max_digits=15, decimal_places=0)
    endereco = models.CharField(max_length=100)
    senha = models.CharField(max_length=100)
    eumainstuicaodeensino = models.BooleanField(default=False)
    codigoDeVerificacao = models.DecimalField(max_digits=3, decimal_places=0, default='123')
    
    def __str__(self):
        return self.nomeCompleto

class Cotacao(models.Model):
    nomeDaCotacao = models.CharField(max_length=100)
    Categoria = models.CharField(max_length=100)
    descricaoERequisitos = models.CharField(max_length=100)
    quantidade = models.IntegerField(validators=[MaxValueValidator(10000000000000)])
    unidadesDeMedida = models.CharField(max_length=100)
    receberPropostasaAte = models.DateTimeField()
    entregaAte = models.DateField()
    urgencia = models.CharField(max_length=100)
    melhorOferta = models.CharField(max_length=100, default='Sem propostas')
    status = models.CharField(max_length=100, default='Aberta')
    temProposta = models.BooleanField(null=True)
    contaCotacao = models.ForeignKey(Conta, on_delete=models.CASCADE, default=1)
    
    
    def __str__(self):
        return self.nomeDaCotacao
    

class Avaliacoes(models.Model):
    cotacao = models.ForeignKey(Cotacao, on_delete=models.CASCADE, null=True)
    fornecedor = models.ForeignKey(Conta, on_delete=models.CASCADE, null=True)
    nota = models.DecimalField(max_digits=1, decimal_places=0, validators=[MaxValueValidator(5)])
    situacao = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Avaliação de {self.fornecedor.nomeCompleto} para a cotação {self.cotacao.nomeDaCotacao}: Nota {self.nota}, Situação: {self.situacao}, Status: {self.status}"

class CotacaoFornecedor(models.Model):
    cotacao = models.ForeignKey(Cotacao, on_delete=models.CASCADE, null=True)
    fornecedor = models.ForeignKey(Conta, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Cotação {self.cotacao.nomeDaCotacao} - Fornecedor {self.fornecedor.nomeCompleto}"    

class FornecedoresFavoritos(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='conta')
    fornecedor = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='fornecedor')
    categoria = models.CharField(max_length=100)
    avaliacao = models.DecimalField(max_digits=1, decimal_places=0, validators=[MaxValueValidator(5)], default=0)
    adicionado_em = models.DateField()
    status = models.CharField(max_length=100)
    
    def __str__(self):
        return f"Cotação {self.cotacao.nomeDaCotacao} - Conta {self.fornecedor.nomeCompleto}"    

class convites(models.Model):
    email = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100) 
    enviado = models.DateField()
    validade = models.DateField()
    quemEnviou = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='quemEnviou', null=True)

    def __str__(self):
        return f"email: {self.email}"

class membro(models.Model):
    membro = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100) 
    ultimoAcesso = models.DateTimeField() 
    status = models.CharField(max_length=100) 
    acoes = models.CharField(max_length=100)

    def __str__(self):
        return f"email: {self.email}" 

class mensagem(models.Model):
    remetente = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='remetente')
    destinatario = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='destinatario', null=True)
    mensagem = models.TextField()
    dataEnvio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensagem de {self.remetente} para {self.destinario}: {self.assunto}"
  

class equipe(models.Model):
    nomeEquipe = models.CharField(max_length=100, default='nenhuma', unique=True) 
    donoDaEquipe = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='donoDaEquipe')

    def __str__(self):
        return f"Nome equipe: {self.nomeEquipe}"

class equipe_membro(models.Model):
    equipe = models.ForeignKey(equipe, on_delete=models.CASCADE, related_name='equipe', null=True)
    membro_equipe = models.ForeignKey(membro, on_delete=models.CASCADE, related_name='membro_equipe', null=True)

    def __str__(self):
        return f"equipe: {self.equipe}, membro equipe: {self.membro_quipe}"

class mensagensEmail(models.Model):
    assunto = models.CharField(max_length=100) 
    descricao = models.CharField(max_length=100) 
    emailParaResposta = models.EmailField()

    def __str__(self):
        return f"assunto: {self.assunto}"

class pesosELimitesObjetivos(models.Model):
    documentoFiscal = models.CharField(max_length=100) 
    exigirNotaFiscal = models.BooleanField(default=True)
    melhorPreco = models.CharField(max_length=100) 
    valorMaximo = models.DecimalField(max_digits=10000000, decimal_places=2, default=0, null=True, blank=True)
    entregaMaisRapida = models.CharField(max_length=100) 
    entregaAte = models.DateField(null=True, blank=True)
        
class Proposta(models.Model):
    valorTotal = models.DecimalField(max_digits=14, decimal_places=2)       
    dataDeEntrega = models.DateField() 
    condicoesEDetalhesDoPagamento = models.CharField(max_length=100) 
    marcaOuFabricante = models.CharField(max_length=100) 
    observacoesComerciais = models.CharField(max_length=100)
    emiteDocumentoFiscal = models.BooleanField()
    cotacao = models.ForeignKey(Cotacao, on_delete=models.CASCADE, null=True)
    pesosELimitesObjetivos = models.ForeignKey(pesosELimitesObjetivos, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"Condicoes {self.condicoesEDetalhesDoPagamento}"

class notificacoes(models.Model):
    conta = models.ForeignKey(Conta, on_delete=models.CASCADE, related_name='membro_equipe', null=True)
    titulo = models.CharField(max_length=100) 
    descrição = models.CharField(max_length=100) 
    lida = models.BooleanField()