import argparse


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Generar estadísticas de secuencias a partir de un archivo FASTA"
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Ruta del archivo FASTA de entrada",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Ruta del archivo TSV de salida",
        required=True,
    )
    parser.add_argument(
        "--min_len",
        type=int,
        default=0,
        help="Longitud mínima permitida de las secuencias",
    )
    parser.add_argument(
        "--max_len",
        type=int,
        default=0,
        help="Longitud máxima permitida de las secuencias",
    )
    parser.add_argument(
        "--min_gc",
        type=float,
        default=0.0,
        help="Contenido GC mínimo permitido de las secuencias (0-1)",
    )
    parser.add_argument(
        "--max_gc",
        type=float,
        default=0.0,
        help="Contenido GC máximo permitido de las secuencias (0-1)",
    )

    return parser.parse_args()
