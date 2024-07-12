import argparse

from web import check_citas

def parse_args():
    # Initialize the command-line argument parser
    parser = argparse.ArgumentParser(description='Automate NIE submission.')
    parser.add_argument('nie_code', type=str, help='NIE code to submit')
    parser.add_argument('nombre_apellidos', type=str, help='Nombre y apellidos to submit')
    parser.add_argument('office', type=str, help='Office to select')
    parser.add_argument('tramite', type=str, help='Trámite to select')
    args = parser.parse_args()
    return args

def main():
    # Parse the arguments
    args = parse_args()
    nie_code = args.nie_code
    nombre_apellidos = args.nombre_apellidos
    office = args.office
    tramite = args.tramite

    # Check for citas
    citas_available = check_citas(nie_code, nombre_apellidos, office, tramite)
    if citas_available:
        print("Citas available")
    else:
        print("No citas available")

if __name__ == "__main__":
    main()
