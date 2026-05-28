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


def leer_fasta(ruta):
    secuencias = []
    encabezado_actual = None
    secuencia_actual = ""

    try:
        with open(ruta, "r") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue

                if linea.startswith(">"):
                    if encabezado_actual is not None:
                        secuencias.append((encabezado_actual, secuencia_actual))
                    encabezado_actual = linea[1:].strip()
                    secuencia_actual = ""
                else:
                    secuencia_actual += linea

            if encabezado_actual is not None:
                secuencias.append((encabezado_actual, secuencia_actual))
    except FileNotFoundError as error:
        raise SystemExit(f"ERROR: archivo no encontrado '{ruta}'") from error

    return secuencias


def calcular_gc(secuencia):
    longitud = len(secuencia)
    if longitud == 0:
        return 0.0

    g_count = secuencia.count("G")
    c_count = secuencia.count("C")
    gc_content = (g_count + c_count) / longitud
    return gc_content
