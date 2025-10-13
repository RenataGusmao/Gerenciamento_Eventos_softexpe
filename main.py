from menu import run_menu
# use JsonRepo (persistência). Se preferir, pode voltar para MemoryRepo.
from json_repo import JsonRepo
# from memory_repo import MemoryRepo  # alternativa sem persistência

def main():
    repo = JsonRepo("data/events.json")   # arquivo onde será salvo
    # repo = MemoryRepo()                 # fallback (sem persistência)
    from sistemas_evento import SistemaEventos
    sistema = SistemaEventos(repo=repo)
    try:
        sistema.carregar()                # carrega do JSON (se existir)
        run_menu(sistema)
    except KeyboardInterrupt:
        print("\nSaindo...")
    finally:
        sistema.salvar()                  # salva no JSON ao sair

if __name__ == "__main__":
    main()



