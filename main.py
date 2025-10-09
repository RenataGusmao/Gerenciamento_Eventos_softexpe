from menu import run_menu
from sistemas_evento import SistemaEventos   # atenção: seu arquivo chama sistemas_evento.py
from memory_repo import MemoryRepo

def main():
    repo = MemoryRepo()
    sistema = SistemaEventos(repo=repo)
    try:
        run_menu(sistema)
    except KeyboardInterrupt:
        print("\nSaindo...")

if __name__ == "__main__":
    main()

