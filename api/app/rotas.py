from fastapi.responses import JSONResponse,StreamingResponse
from fastapi.encoders import jsonable_encoder
from datetime import datetime
from fastapi import APIRouter, Request, status
from classes import AcelerometroModel
import matplotlib.pyplot as plt
import numpy as np
import io


router = APIRouter(prefix='/acelerometro', tags=['acelerometro'])

@router.post('/acelerometro')
async def salvar_dados_acelerometro_json(request: Request, data: AcelerometroModel):
    dados_acelerometro = {
        'nome_empresa':data.nome_empresa,
        "nome_equip": data.nome_equip,
        "acelerometroY": data.acelerometroY,
        'temp':data.temp,
        "dt_cria": datetime.now()
    }

    acelerometro_json = jsonable_encoder(dados_acelerometro)
    db = request.app.state.mongodb.db_acelerometro
    acelerometro_nova= await db["acelerometro"].insert_one(acelerometro_json)   
    inserted_id = str(acelerometro_nova.inserted_id)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"id": inserted_id})

@router.get('/acelerometro/{empresa},{equipe}')
async def recuperar_dados_acelerometro_json(request: Request, empresa: str, equipe: str):
    db = request.app.state.mongodb.db_acelerometro
    dados = await db["acelerometro"].find({
        'nome_empresa': empresa, 
        'nome_equip': equipe
    }).sort([("dt_cria",-1)]).limit(1).to_list(1)
    
    if not dados:
        return {"error": "No data found"}
    # Transformando '_id' para string
    for item in dados:
        item['_id'] = str(item['_id'])
    # Supondo que os dados relevantes para o gráfico estão em um campo chamado 'transf'
    transf = dados[0].get('acelerometroY', [])
    # Convertendo os dados para numpy array
    dados6 = np.array(transf)
    # Número de pontos no sinal
    N = len(dados6)
    fs = 1000  
    # Criando o vetor de tempo
    T = 1 / fs
    t = np.arange(0, N / fs, T)
    # Calculando a FFT
    f = np.fft.fftfreq(N, T)
    fft_values = np.fft.fft(dados6)
    # Gerando o gráfico
    plt.figure()
    plt.plot(f[f > 0], np.abs(fft_values[f > 0]) * 1 / N, label='FFT')
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Transformada de Fourier')
    plt.legend()
    # Criando o buffer de memória
    buf = io.BytesIO()
    # Salvando o gráfico no buffer em formato PNG
    plt.savefig(buf, format='png')
    # Reposicionando o ponteiro do buffer para o início
    buf.seek(0)
    plt.close()
    # Retornando a imagem gerada
    return StreamingResponse(buf, media_type="image/png")    





