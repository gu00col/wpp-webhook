from fastapi import APIRouter,BackgroundTasks, Depends, HTTPException,Request
import pprint
import os
import json
from datetime import datetime
import time



# Cria uma instância de APIRouter que será usada para adicionar as rotas
router = APIRouter()

def gravar_dicionario(nome_arquivo, dicionario):
    # Define o nome do arquivo com a extensão .txt
    nome_arquivo_completo = f"{nome_arquivo}.json"
    
    # Verifica se o arquivo existe
    if not os.path.exists(nome_arquivo_completo):
        # Cria o arquivo se não existir
        with open(nome_arquivo_completo, 'w') as arquivo:
            pass  # Apenas cria o arquivo vazio

    # Abre o arquivo no modo append para adicionar conteúdo
    with open(nome_arquivo_completo, 'a') as arquivo:
        # Converte o dicionário para uma string JSON formatada
        json_str = json.dumps(dicionario, ensure_ascii=False, indent=4)
        # Escreve o JSON no arquivo, seguido por uma nova linha
        arquivo.write(json_str + ',')


# Supondo que você tenha um router configurado
@router.post("/webhook/{endpoint}")
async def  webhook(
    endpoint: str,
    request: Request,
    background_tasks: BackgroundTasks
):
    print(f"\n {'-'*30}")
    print(f'Inicio do Webhook: {endpoint}')
    try:
  
        json_data = await request.json()

        gravar_dicionario(f'{json_data["instance"]}-{endpoint}',json_data)

        
        return {
            "sistema": "Webhook Whatsapp",
            "versão": "0.1",
            'endpoint': endpoint
        }
    except Exception as e:
        # Se ocorrer algum erro, uma exceção HTTP é levantada com o detalhe do erro
        raise HTTPException(status_code=400, detail=str(e))