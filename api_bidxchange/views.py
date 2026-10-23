from datetime import datetime, timedelta
import random
import token

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, request

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .models import Avaliacoes, Conta, Cotacao, CotacaoFornecedor, FornecedoresFavoritos, mensagem, Proposta, convites, membro, equipe, equipe_membro, convites
from .serializers import ContaModificacaoSerializer, ContaSerializer, CotacaoFornecedorSerializer, CotacaoSerializer, PropostaSerializer, ConviteSerializer
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.core.mail import send_mail

import json




@api_view(['POST'])
@permission_classes([AllowAny])
def criar_conta(request):
    serializer = ContaSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Validacao do cnpj
            cnpjSemCaracteresEspeciais = serializer.validated_data['cnpj'].replace('.', '').replace('/', '').replace('-', '')
            if len(cnpjSemCaracteresEspeciais) != 14:
                return Response({'erro': 'CNPJ inválido'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                primeiroDigito = int(cnpjSemCaracteresEspeciais[12])
                segundoDigito = int(cnpjSemCaracteresEspeciais[13])
                primeiroDigitoFeito = 0
                segundoDigitoFeito = 0
                soma = 0
                

                for i in range(0, len(cnpjSemCaracteresEspeciais) - 2):
                    match i:
                        case 0:
                            soma += int(cnpjSemCaracteresEspeciais[0]) * 5
                        case 1:
                            soma += int(cnpjSemCaracteresEspeciais[1]) * 4
                        case 2:
                            soma += int(cnpjSemCaracteresEspeciais[2]) * 3
                        case 3:
                            soma += int(cnpjSemCaracteresEspeciais[3]) * 2
                        case 4:
                            soma += int(cnpjSemCaracteresEspeciais[4]) * 9
                        case 5:
                            soma += int(cnpjSemCaracteresEspeciais[5]) * 8
                        case 6:
                            soma += int(cnpjSemCaracteresEspeciais[6]) * 7
                        case 7:
                            soma += int(cnpjSemCaracteresEspeciais[7]) * 6
                        case 8:
                            soma += int(cnpjSemCaracteresEspeciais[8]) * 5
                        case 9:
                            soma += int(cnpjSemCaracteresEspeciais[9]) * 4
                        case 10:
                            soma += int(cnpjSemCaracteresEspeciais[10])  * 3
                        case 11:
                            soma += int(cnpjSemCaracteresEspeciais[11]) * 2
            
                            if soma % 11 < 2:
                                primeiroDigitoFeito = 0
                            else:
                                primeiroDigitoFeito = 11 - (soma % 11)
                
                soma = 0
                for i in range(0, len(cnpjSemCaracteresEspeciais) - 1):
                    match i:
                        case 0:
                            soma += int(cnpjSemCaracteresEspeciais[0]) * 6
                        case 1:
                            soma += int(cnpjSemCaracteresEspeciais[1]) * 5
                        case 2:
                            soma += int(cnpjSemCaracteresEspeciais[2]) * 4
                        case 3:
                            soma += int(cnpjSemCaracteresEspeciais[3]) * 3
                        case 4:
                            soma += int(cnpjSemCaracteresEspeciais[4]) * 2
                        case 5:
                            soma += int(cnpjSemCaracteresEspeciais[5]) * 9
                        case 6:
                            soma += int(cnpjSemCaracteresEspeciais[6]) * 8
                        case 7:
                            soma += int(cnpjSemCaracteresEspeciais[7]) * 7
                        case 8:
                            soma += int(cnpjSemCaracteresEspeciais[8]) * 6
                        case 9:
                            soma += int(cnpjSemCaracteresEspeciais[9]) * 5
                        case 10:
                            soma += int(cnpjSemCaracteresEspeciais[10]) * 4
                        case 11:
                            soma += int(cnpjSemCaracteresEspeciais[11]) * 3
                        case 12:
                            soma += int(cnpjSemCaracteresEspeciais[12]) * 2
            
                            if soma % 11 < 2:
                                segundoDigitoFeito = 0
                            else:
                                segundoDigitoFeito = 11 - (soma % 11)
                if (segundoDigitoFeito == segundoDigito) and (primeiroDigitoFeito == primeiroDigito):
                    Conta.objects.create(
                        nomeCompleto=serializer.validated_data['nomeCompleto'],
                        email=serializer.validated_data['email'],
                        razaoSocial=serializer.validated_data['razaoSocial'],
                        nomeFantasia=serializer.validated_data.get('nomeFantasia', ''),
                        cnpj=serializer.validated_data['cnpj'],
                        telefone=serializer.validated_data['telefone'],
                        endereco=serializer.validated_data['endereco'],
                        senha=serializer.validated_data['senha'],
                        eumainstuicaodeensino = serializer.validated_data.get('eumainstuicaodeensino', False)
                    )
                    conta = Conta.objects.get(email=serializer.validated_data['email'])
                    equipe.objects.create(nomeEquipe=serializer.validated_data.get('nomeFantasia', ''), donoDaEquipe=conta)
                    return Response({'mensagem': 'conta criada'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'erro': 'CNPJ inválido'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_conta(request):
    usuario = get_user_model()
    try:
        conta = Conta.objects.get(email=request.data['email'], senha=request.data['senha'])
        usuarioPego = usuario.objects.get(email=conta.email)
        usuarioPego.delete()
        Token.objects.get(user=usuarioPego).delete()
        usuarioFeito = usuario.objects.create_user(username=conta.nomeCompleto, email=conta.email, password=conta.senha)
        token = Token.objects.create(user=usuarioFeito)
        return Response({'mensagem': 'Login bem-sucedido, o seu token: ' + str(token.key)}, status=status.HTTP_200_OK)
        
        
    except usuario.DoesNotExist:
        conta = Conta.objects.get(email=request.data['email'], senha=request.data['senha'])
        usuarioFeito = usuario.objects.create_user(username=conta.nomeCompleto, email=conta.email, password=conta.senha)
        token = Token.objects.create(user=usuarioFeito)
        return Response({'mensagem': 'Login bem-sucedido, o seu token: ' + str(token.key)}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'erro': 'Credenciais inválidas, erro mais detalhado: ' + str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['PUT'])
def modificar_conta(request):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        conta = Conta.objects.get(id=usuarioDoToken.id)
        
        serializer = ContaModificacaoSerializer(conta, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def criar_cotacao(request):
    serializer = CotacaoSerializer(data=request.data)
    if serializer.is_valid():
        try:
            receberPropostasaAte = serializer.validated_data['receberPropostasaAte'] 
            entregaAte = serializer.validated_data['entregaAte']
            receberPropostasAteData = datetime.strptime(str(receberPropostasaAte), '%Y-%m-%d %H:%M:%S+00:00')
            entregaAteData = datetime.strptime(str(entregaAte), '%Y-%m-%d')
            if (receberPropostasAteData > entregaAteData):
                return Response({'erro': 'A entrega não pode ocorrer antes do encerramento da cotação. '}, status=status.HTTP_401_UNAUTHORIZED)
            elif (receberPropostasAteData < datetime.now()):
                return Response({'erro': 'A data de encerramento da cotação não pode ser anterior a data atual. '}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
                tokenPego = Token.objects.get(key=parteDoToken[1])
                usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
                
                cotacaoAtual = Cotacao.objects.create(
                    nomeDaCotacao=serializer.validated_data['nomeDaCotacao'],
                    Categoria=serializer.validated_data['Categoria'],
                    descricaoERequisitos=serializer.validated_data['descricaoERequisitos'],
                    quantidade=serializer.validated_data['quantidade'],
                    unidadesDeMedida=serializer.validated_data['unidadesDeMedida'],
                    receberPropostasaAte=serializer.validated_data['receberPropostasaAte'],
                    entregaAte=serializer.validated_data['entregaAte'],
                    urgencia=serializer.validated_data['urgencia'], 
                    melhorOferta=serializer.validated_data.get('melhorOferta', 'Sem propostas'),
                    status=serializer.validated_data.get('status', 'Aberta'),
                    contaCotacao=usuarioDoToken
                )
                
                idDaCotacao = cotacaoAtual.id            
                dataCotacaoFornecedor = {
                    'cotacao': idDaCotacao,
                    'fornecedor': usuarioDoToken.id
                }
                serializer2 = CotacaoFornecedorSerializer(data=dataCotacaoFornecedor)
                if serializer2.is_valid():
                    CotacaoFornecedor.objects.create(
                        cotacao=Cotacao.objects.get(id=idDaCotacao),
                        fornecedor=Conta.objects.get(id=usuarioDoToken.id)
                    )
                    return Response({'mensagem': 'Cotação criada'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'erro': 'Credenciais inválidas, erro mais detalhado: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'erro': 'Credenciais inválidas, erro mais detalhado: ' + str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'erro': 'Dados inválidos, erro mais detalhado: ' + str(serializer.errors)}, status=status.HTTP_400_BAD_REQUEST)
            

@api_view(['GET'])
def listar_cotacoes(request):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        conta = Conta.objects.get(id=usuarioDoToken.id)

        cotacoesSerializer = CotacaoSerializer(Cotacao.objects.all().filter(contaCotacao=conta.id), many=True)
        return Response(cotacoesSerializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'erro': 'Erro ao ver cotações, erro mais detalhado: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def encerrar_cotacao(request, id):
    try:
        cotacao = Cotacao.objects.get(id=id)
        cotacao.status = 'Encerrada sem escolha'
        cotacao.save()
        return Response({'mensagem': 'Cotação encerrada com sucesso'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def cotacao_id(request, id):
    try:
        cotacao = Cotacao.objects.get(id=id)
        cotacaoSerializer = CotacaoSerializer(cotacao)
        return Response(cotacaoSerializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def conta(request):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        conta = Conta.objects.get(id=usuarioDoToken.id)
        contaSerializer = ContaSerializer(conta)
        if (contaSerializer.is_valid()):
            return Response(contaSerializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def criar_avaliacao(request):
    try:
        cotacao = Cotacao.objects.get(id=request.data['cotacao_id'])
        fornecedor = Conta.objects.get(id=request.data['fornecedor_id'])
        nota = request.data['nota']
        comentario = request.data['comentario']
        situacao = request.data['situacao']
        status_avaliacao = request.data['status']

        avaliacao = Avaliacoes.objects.create(
            cotacao=cotacao,
            fornecedor=fornecedor,
            nota=nota,
            comentario=comentario,
            situacao="Avaliada",
            status="Concluída"
        )
        return Response({'mensagem': 'Avaliação criada com sucesso'}, status=status.HTTP_201_CREATED)
    except Cotacao.DoesNotExist:
        return Response({'erro': 'Cotação não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    except Conta.DoesNotExist:
        return Response({'erro': 'Fornecedor não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'erro': 'Erro ao criar avaliação: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

def ver_avaliacoes(request):
    try:
        conta = request.user.conta

        avaliacoes = Avaliacoes.objects.filter(
            fornecedor=conta
        )

        dados = []

        for avaliacao in avaliacoes:
            dados.append({
                'id': avaliacao.id,
                'cotacao': avaliacao.cotacao.nomeDaCotacao,
                'fornecedor': avaliacao.fornecedor.nomeCompleto,
                'nota': avaliacao.nota,
                'situacao': avaliacao.situacao,
                'status': avaliacao.status
            })

        return JsonResponse(dados, safe=False)
    except Exception as e:
        return Response({'erro': 'Erro ao ver avaliações, erro mais detalhado: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def adicionar_favorito(request, id, categoria, nota):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        fornecedor = Conta.objects.get(id=id)

        FornecedoresFavoritos.objects.create(
            conta=usuarioDoToken,
            fornecedor=fornecedor,
            categoria=categoria,
            avaliacao=nota,
            adicionado_em=timezone.now().date(),
            status='Verificado'
        )
        
        return Response({'mensagem': 'favorito adicionado '}, status=status.HTTP_200_OK) 
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def ver_favoritos(request):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        favoritos = FornecedoresFavoritos.objects.filter(conta=usuarioDoToken)
        
        dados = []
                
        for favorito in favoritos:
            dados.append({
                'conta': favorito.conta.id,
                'fornecedor': favorito.fornecedor.id,
                'categoria': favorito.categoria,
                'avaliacao': favorito.avaliacao,
                'adicionado_em': favorito.adicionado_em,
                'status': favorito.status
            })
        
        return JsonResponse(dados, safe=False)
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])    
def ver_todos_os_usuarios_mensagens(request):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)

        mensagens = mensagem.objects.filter(
            remetente=usuarioDoToken.id
        )

        dados = []

        for msg in mensagens:
            dados.append({
                'id': msg.id,
                'remetente': msg.remetente.id,
                'destinatario': msg.destinatario.id,
                'mensagem': msg.mensagem,
                'dataEnvio': msg.dataEnvio
            })

        return JsonResponse(dados, safe=False)
    except Exception as e:
        return Response({'erro': 'Erro ao ver mensagens, erro mais detalhado: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])    
def ver_mensagens_usuario(request, id):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        destinatario = Conta.objects.get(id=id)
        
        mensagens = mensagem.objects.filter(
            remetente=usuarioDoToken.id,
            destinatario=destinatario.id
        )
        
        dados = []

        for msg in mensagens:
            dados.append({
                'id': msg.id,
                'remetente': msg.remetente.id,
                'destinatario': msg.destinatario.id,
                'mensagem': msg.mensagem,
                'dataEnvio': msg.dataEnvio
            })

        return JsonResponse(dados, safe=False)
    except Exception as e:
        return Response({'erro': 'Erro ao ver mensagens do usuário, erro mais detalhado: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def enviar_mensagem(request, id_usuario_destinatario):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        destinario = Conta.objects.get(id=id_usuario_destinatario)
        mensagem_texto = request.data.get('mensagem_texto')
        if (id_usuario_destinatario == usuarioDoToken.id):
            return Response({'erro': 'Erro você não pode enviar mensagens a si mesmo'}, status=status.HTTP_400_BAD_REQUEST)
               
        mensagem.objects.create(
            remetente=usuarioDoToken,
            destinatario=destinario,
            mensagem=mensagem_texto,
            dataEnvio=timezone.now()
        )
        return Response({'mensagem': 'Mensagem enviada com sucesso'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'erro': 'Erro ao enviar mensagem, erro mais detalhado: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['POST'])
def criar_proposta(request):
    try:
        serializer = PropostaSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'erro': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        cotacao_id = request.data['cotacao']
        cotacao_obj = get_object_or_404(Cotacao, id=cotacao_id)

        Proposta.objects.create(
            valorTotal=serializer.validated_data['valorTotal'],
            dataDeEntrega=serializer.validated_data['dataDeEntrega'],
            condicoesEDetalhesDoPagamento=serializer.validated_data[
                'condicoesEDetalhesDoPagamento'
            ],
            marcaOuFabricante=serializer.validated_data['marcaOuFabricante'],
            observacoesComerciais=serializer.validated_data[
                'observacoesComerciais'
            ],
            emiteDocumentoFiscal=serializer.validated_data[
                'emiteDocumentoFiscal'
            ],
            cotacao=cotacao_obj
        )

        cotacao_obj.temProposta = True
        cotacao_obj.save()

        return Response(
            {'mensagem': 'Proposta criada com sucesso'},
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {'erro': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def ver_propostas(request):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        propostas = Proposta.objects.all().filter(cotacao=Cotacao.objects.get(contaCotacao=usuarioDoToken.id).id)
        
        dados = [
            {
                'id': proposta.id,
                'valorTotal': str(proposta.valorTotal),
                'dataDeEntrega': proposta.dataDeEntrega,
                'condicoesEDetalhesDoPagamento': proposta.condicoesEDetalhesDoPagamento,
                'marcaOuFabricante': proposta.marcaOuFabricante,
                'observacoesComerciais': proposta.observacoesComerciais,
                'emiteDocumentoFiscal': proposta.emiteDocumentoFiscal,
                'cotacao': proposta.cotacao.id
            }
            for proposta in propostas
        ]

        return Response(
            {'propostas': dados},
            status=status.HTTP_200_OK
        )                           
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)        

@api_view(['GET'])
def ver_proposta_id(request, id):
    try:
        propostaid = Proposta.objects.all().filter(id=id)
        dados = [
                {
                    'id': proposta.id,
                    'valorTotal': str(proposta.valorTotal),
                    'dataDeEntrega': proposta.dataDeEntrega,
                    'condicoesEDetalhesDoPagamento': proposta.condicoesEDetalhesDoPagamento,
                    'marcaOuFabricante': proposta.marcaOuFabricante,
                    'observacoesComerciais': proposta.observacoesComerciais,
                    'emiteDocumentoFiscal': proposta.emiteDocumentoFiscal,
                    'cotacao': proposta.cotacao.id
                }
                for proposta in propostaid
            ]
    
        return Response(
                {'proposta': dados},
                status=status.HTTP_200_OK
        )                          
        
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def enviar_mensagem_suporte(request):
    try:
        assunto = request.data['assunto']
        descricao = request.data['descricao']
        emailParaResposta = request.data['emailParaResposta']

        send_mail(
            subject=f'{assunto}',
            message=f'{descricao} \n email para resposta: {emailParaResposta}',
            from_email='nicolasrenovado12@gmail.com',
            recipient_list=['nicolasrenovado12@gmail.com'],
            fail_silently=False,
        )

        return Response(
            {'mensagem': 'Mensagem enviada com sucesso!'},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def enviar_email_senha(request):
    try:
        digito1 = random.randint(1, 100)
        digito2 = random.randint(1, 100)
        digito3 = random.randint(1, 100)
        codigoDeVerificacao = str(digito1) + '' + str(digito2) + '' + str(digito3)
        email = request.data['email']
        usuarioDoToken = Conta.objects.get(email=email)
                
        usuarioDoToken.codigoDeVerificacao = codigoDeVerificacao
        
        usuarioDoToken.save()   
                
        send_mail(
            subject=f'Código de verificação - BidXChange',
            message=f'Código de verificação: {codigoDeVerificacao}',
            from_email='nicolasrenovado12@gmail.com',
            recipient_list=['nicolasrenovado12@gmail.com'],
            fail_silently=False,
        )
        
        
        return Response(
            {'mensagem': 'Email enviado'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def mudar_senha(request):
    try:
        codigoDeVerificacao = request.data['codigoDeVerificacao']
        email = request.data['email']
        senha = request.data['senha']
        senhaRepetida = request.data['senha']
        conta = Conta.objects.get(email=email)
        
        if (codigoDeVerificacao == conta.codigoDeVerificacao):
            
            if (senhaRepetida == senha):
                
            else:
                return Response(
                    {'Senha invalida': 'As senhas não coincidem entre si'},
                    status=status.HTTP_400_BAD_REQUEST 
                )
        else:
            return Response(
                {'codigoDeVerificacao': 'Código de verificação incorreto'},
                status=status.HTTP_400_BAD_REQUEST 
            )
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)   

@api_view(['POST'])
def enviar_convite(request):
    try:
        serializer = ConviteSerializer(data=request.data)
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)

        if serializer.is_valid():
            convites.objects.create(email=request.data['email'], cargo=request.data['cargo'], enviado=timezone.now(), validade=timezone.now()+ timedelta(weeks=1), quemEnviou=usuarioDoToken)

            return Response({'mensagem': "Convite enviado"}, status=status.HTTP_200_OK)
        else:
            return Response({'mensagem': "Json invalido"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def ver_convites(request):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        usuarioDoToken = Conta.objects.get(email=tokenPego.user.email)
        convites1 = convites.objects.all().filter(quemEnviou=usuarioDoToken.id)
        dados = [
                {
                    'id': convite.id,
                    'email': convite.email,
                    'cargo': convite.cargo,
                    'enviado': convite.enviado,
                    'validade': convite.validade,
                    'quemEnviou': convite.quemEnviou.id,
                }
                for convite in convites1
        ]
    
        return Response(
                {'convites': dados},
                status=status.HTTP_200_OK
        ) 
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def deletar_convite(request, id):
    try:
        convites.objects.get(id=id).delete()
        return Response({"Convite deletado com sucesso"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)

def aceitar_convite(request, email):
    try:
        parteDoToken = request.META.get('HTTP_AUTHORIZATION').split(' ')
        tokenPego = Token.objects.get(key=parteDoToken[1])
        conta = Conta.objects.get(email=email)        
        
        membro = membro.objects.create(
            membro=conta.nomeCompleto,
            email=conta.email,
            cargo=convites.objects.get(email=email).cargo,
            ultimoAcesso=tokenPego.created,
            status="Ativo",
            acoes=convites.objects.get(email=email).cargo
        )
        convite = convites.objects.get(email=email)
        equipe = equipe.objects.get(donoDaEquipe=convite.quemEnviou)

        equipe_membro.objects.create(equipe=equipe, membro_equipe=membro)
        
        convites.objects.get(email=email).delete()
        
        return Response({"Convite deletado com sucesso"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'erro': 'Erro, erro mais detalhado: ' + str(e)}, status=status.HTTP_404_NOT_FOUND)
