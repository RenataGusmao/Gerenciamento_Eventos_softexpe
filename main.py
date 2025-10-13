# Importa a função que executa o menu interativo.
from menu import run_menu
# Importa o repositório que salva os dados em um arquivo JSON.
from json_repo import JsonRepo
# from memory_repo import MemoryRepo  # Alternativa que salva os dados apenas em memória.

def main():
    # Cria uma instância do repositório JSON, especificando o arquivo onde os dados serão guardados.
    repo = JsonRepo("data/events.json")
    # repo = MemoryRepo()  # Opção para usar o sistema sem salvar dados permanentemente.

    # Importa a classe principal do sistema de eventos.
    from sistemas_evento import SistemaEventos
    # Cria a instância do sistema, passando o repositório como dependência.
    sistema = SistemaEventos(repo=repo)

    try:
        # Carrega os dados do arquivo JSON para a memória.
        sistema.carregar()
        # Inicia o menu interativo para o usuário.
        run_menu(sistema)
    except KeyboardInterrupt:
        # Captura o comando de interrupção (Ctrl+C) para sair de forma elegante.
        print("\nSaindo...")
    finally:
        # Garante que os dados sejam salvos no arquivo JSON ao encerrar o programa.
        sistema.salvar()

# Verifica se o script está sendo executado diretamente para chamar a função main.
if __name__ == "__main__":
    main()