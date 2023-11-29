import json

def extrair_job_step_ids(conteudo_json):
    job_step_ids = []

    # Obtém a lista de job-steps
    job_steps = conteudo_json.get('job-specification', {}).get('job-steps', {}).get('job-step', [])

    for job_step in job_steps:
        if (
            isinstance(job_step, dict) and
            job_step.get('@xsi:type') == 'visualization-store-job-step' and
            'job-step-id' in job_step
        ):
            job_step_ids.append(job_step['job-step-id'])

    return job_step_ids

# Substitua 'CAMINHO_DO_SEU_ARQUIVO_JSON' pelo caminho real do arquivo JSON no seu sistema
caminho_do_arquivo_json = 'teste.json'

# Carrega o conteúdo do arquivo JSON
with open(caminho_do_arquivo_json, 'r') as arquivo:
    conteudo_do_arquivo = json.load(arquivo)

# Extrai os job-step-ids
job_step_ids = extrair_job_step_ids(conteudo_do_arquivo)

if job_step_ids:
    print("Valores de 'job-step-id' para '@xsi:type' igual a 'visualization-store-job-step':")
    for job_step_id in job_step_ids:
        print(job_step_id)
    
    # Adiciona o último job-step-id à variável para uso no restante do script
    consuming_job_step_id_variavel = job_step_ids[-1]

    # Função para verificar se 'error-message' não está presente para um job-step com 'consuming-job-step-id'
    def has_error_message(job_steps, consuming_job_step_id):
        for job_step in job_steps:
            if 'job-step-links' in job_step:
                links = job_step['job-step-links']
                if 'out-stream' in links:
                    out_stream = links['out-stream']
                    if 'stream-consumers' in out_stream:
                        stream_consumers = out_stream['stream-consumers']['stream-consumer']
                        if isinstance(stream_consumers, list):
                            for field in out_stream.get('output-fields', {}).get('field', []):
                                if field.get('#text') == 'error-message':
                                    return False
                            return any(consumer.get('consuming-job-step-id') == consuming_job_step_id for consumer in stream_consumers)
                        elif stream_consumers.get('consuming-job-step-id') == consuming_job_step_id:
                            return 'error-message' not in [field.get('#text') for field in out_stream.get('output-fields', {}).get('field', [])]
        return False

    # Verificar se 'error-message' não está presente para o job-step com consuming-job-step-id variável
    if 'job-specification' in conteudo_do_arquivo and 'job-steps' in conteudo_do_arquivo['job-specification']:
        job_steps = conteudo_do_arquivo['job-specification']['job-steps']['job-step']
        if isinstance(job_steps, list):
            if has_error_message(job_steps, consuming_job_step_id_variavel):
                print(f"O job-step '{consuming_job_step_id_variavel}' não contém 'error-message'")
            else:
                print(f"O job-step '{consuming_job_step_id_variavel}' contém 'error-message'")
        elif isinstance(job_steps, dict):
            if has_error_message([job_steps], consuming_job_step_id_variavel):
                print(f"O job-step '{consuming_job_step_id_variavel}' não contém 'error-message'")
            else:
                print(f"O job-step '{consuming_job_step_id_variavel}' contém 'error-message'")
else:
    print("Nenhum 'job-step-id' encontrado para '@xsi:type' igual a 'visualization-store-job-step'")
