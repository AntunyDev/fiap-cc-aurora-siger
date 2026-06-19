"""
Arquivo principal SIGIC - Aurora Siger.

"""

from sigic.interface import menu_principal


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\nOperacao interrompida pelo usuario.")
