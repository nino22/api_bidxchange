from rest_framework import serializers
from .models import Conta, Cotacao, CotacaoFornecedor, Proposta, convites, pesosELimitesObjetivos

class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = '__all__'
        
class ContaLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['email', 'senha']
        
class ContaModificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ['razaoSocial', 'nomeFantasia', 'email', 'telefone', 'endereco', 'cnpj']
        
class CotacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cotacao
        fields = ['nomeDaCotacao', 'Categoria', 'descricaoERequisitos', 'quantidade', 'unidadesDeMedida', 'receberPropostasaAte', 'entregaAte', 'urgencia']
        
class CotacaoSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Cotacao
        fields = '__all__'
        
class CotacaoFornecedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CotacaoFornecedor 
        fields = '__all__'

class PropostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposta 
        fields = ['valorTotal', 'dataDeEntrega', 'condicoesEDetalhesDoPagamento', 'marcaOuFabricante', 'observacoesComerciais', 'emiteDocumentoFiscal', 'cotacao']

class ConviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = convites
        fields = ['email', 'cargo']

class PesosELimitesObjetivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = pesosELimitesObjetivos
        fields = [
            'documentoFiscal',
            'exigirNotaFiscal',
            'melhorPreco',
            'valorMaximo',
            'entregaMaisRapida',
            'entregaAte'
        ]
class PesosELimitesObjetivosSerializer2(serializers.ModelSerializer):
    class Meta:
        model = pesosELimitesObjetivos
        fields = '__all__'