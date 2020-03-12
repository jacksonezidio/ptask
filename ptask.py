import schedule
import time
import subprocess
import configparser
import os

VERSION = '0.1'


def job():
    """
    Executa a lista de jobs
    """

    print("-> Iniciando execução de jobs..")
    print(f'{time.asctime(time.localtime(time.time()))}')

    lista = []
    lista_processos = []

    # leitura de jobs
    lista_jobs = open('jobs.txt', 'r')
    for linha in lista_jobs:
        lista.append(linha.replace('\n', ''))

    # configuracoes
    config = configparser.ConfigParser()
    config.read('config.ini')

    smartclient = config['CONFIG']['SMARTCLIENT']
    environment = config['CONFIG']['ENVIRONMENT']
    tcp_connection = config['CONFIG']['TCP_CONNECTION']

    for programa in lista:
        print(f"Executando job {programa}")
        # proc = subprocess.run(f'{SMARTCLIENT} {params} {param_programa}', capture_output=True)
        try:
            # path e parametros
            commandLine = [smartclient, f'-C={tcp_connection}', f'-E={environment}', f'-P={programa}', '-M']

            appPath = os.path.join(smartclient, 'smartclient.exe')
            proc = subprocess.Popen(commandLine, executable=appPath)

            lista_processos.append((programa, proc.pid, proc))
        except Exception as e:
            print(e)

    # status processos
    """ TODO: REVISAR POIS MESMO APOS FINALIZACAO DE EXECUCAO A FUNCAO POLL
    RETORNA INFORMACAO DE QUE ESTA EM EXECUCAO
    """
    """
    jobs_em_execucao = len(lista_processos)

    print('\n-> Status de execução\n')

    while jobs_em_execucao > 0:
        for processo in lista_processos:
            return_code = processo[2].poll() #processo[2].returncode

            status = 'Em execucao' if return_code != None  else 'Finalizado'
            try:
                outs, errs = proc.communicate(timeout=60)
            except Exception as e:
                print(e)
                proc.kill()
                outs, errs = proc.communicate()


            print(f'job: {processo[0]} - pid: {processo[1]} - status: {status}')

            #if status == 'Finalizado':
                #jobs_em_execucao -= 1
    """


def main():
    """
        Execucao de Jobs pre-configurados de funcoes do protheus
        autor: Jackson Ezidio de Deus
        contato: jacksonezidio@gmail.com
    """

    print(f'# schedule v{VERSION}')
    print(f'! instrucoes em arquivo readme.txt')
    print('------------------------------------------------')
    print('\n')
    print('-> Iniciando Schedule..')
    print(f'{time.asctime(time.localtime(time.time()))}')
    print('\n')

    time_minutes = 10  # minutes
    time_wait = 60  # seconds

    # configuracoes
    config = configparser.ConfigParser()
    config.read('config.ini')

    time_minutes = int(config['CONFIG']['TIME_MINUTES'])
    time_wait = int(config['CONFIG']['TIME_WAIT'])
    smartclient = config['CONFIG']['SMARTCLIENT']

    print(f'-> Intervalo configurado: {time_minutes} minutos')
    print(f'-> Smartclient configurado: {smartclient}')

    schedule.every(time_minutes).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(time_wait)


if __name__ == "__main__":
    main()