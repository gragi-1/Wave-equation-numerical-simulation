import os
import colorama
from colorama import Fore, Style

# Inicializa colorama para Windows
colorama.init(autoreset=True)

def select_files(directory, extension):
    pass

def main():
    while True:
        # Limpia la terminal (Windows)
        os.system('cls')

        print(Fore.CYAN + "===============================================")
        print(Fore.CYAN + "    SIMULADOR DE LA ECUACIÓN DE SCHRÖDINGER"    )
        print(Fore.CYAN + "===============================================")
        print(Fore.YELLOW + "Seleccione una opción:")
        print(Fore.GREEN + "  1. Simulación 1D")
        print(Fore.GREEN + "  2. Simulación 2D (vista 2D)")
        print(Fore.GREEN + "  3. Simulación 2D (vista 3D)")
        print(Fore.RED + "  q. Salir")
        opcion = input(Fore.MAGENTA + "Ingrese su opción: ").strip().lower()

        if opcion == "1":
            os.system("start python ecuacion1D.py")
        elif opcion == "2":
            os.system("start python ecuacion2d.py")
        elif opcion == "3":
            os.system("start python ecuacion2d_3d.py")
        elif opcion == "q":
            print(Fore.YELLOW + "Saliendo del simulador...")
            break
        else:
            print(Fore.RED + "Opción no válida. Intente nuevamente.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()