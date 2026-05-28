import argparse


def parsear_argumentos():
    """Parsear argumentos de la línea de comandos.

    Returns:
        argparse.Namespace: Argumentos leídos de la línea de comandos.
    """
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


# =========================================
# lectura del archivo fasta y guardado de secuencias en listas de tuplas (encabezado, secuencia)
# =========================================
# =========================================
# Responsabilidad: Leer secuencias desde archivo fasta y almacenarlas en una lista de tuplas (encabezado, secuencia)
# Entrada: archivo
# Salida: lista de tuplas de las secuencias
# =========================================
def leer_fasta(ruta):
    """Leer secuencias desde un archivo FASTA.

    Args:
        ruta (str): Ruta del archivo FASTA de entrada.

    Returns:
        list[tuple[str, str]]: Lista de tuplas (encabezado, secuencia).
    """
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


# =========================================
# Cálculo de contenido de gc (secuencia)
# =========================================
# =========================================
# Responsabilidad: calcular contenido gc de una secuencia dada
# Entrada: secuencia
# Salida: contenido gc
# =========================================
def calcular_gc(secuencia):
    """Calcular contenido GC de una secuencia de ADN.

    Args:
        secuencia (str): Secuencia de ADN.

    Returns:
        float: Proporción de bases G y C entre 0 y 1.
    """
    longitud = len(secuencia)
    if longitud == 0:
        return 0.0

    g_count = secuencia.count("G")
    c_count = secuencia.count("C")
    gc_content = (g_count + c_count) / longitud
    return gc_content


# =========================================
# Cálculo de estadísticas para tuplas (encabezado, secuencia)
# =========================================
# =========================================
# Responsabilidad: calcular estadísticas para una lista de tuplas (encabezado, secuencia)
# Entrada: lista de tuplas (encabezado, secuencia)
# Salida: lista de tuplas con estadísticas
# =========================================
def calcular_estadisticas(secuencias):
    """Calcular estadísticas de una lista de secuencias FASTA.

    Args:
        secuencias (list[tuple[str, str]]): Lista de tuplas (encabezado, secuencia).

    Returns:
        list[tuple[str, int, float]]: Lista de tuplas (encabezado, longitud, contenido_gc).
    """
    estadisticas = []
    for encabezado, secuencia in secuencias:
        encabezado = encabezado.strip()
        longitud = len(secuencia)
        gc_content = calcular_gc(secuencia)
        estadisticas.append((encabezado, longitud, gc_content))

    return estadisticas


# =========================================
# FILTROS para las estadísticas de las secuencias
# =========================================
# =========================================
# Responsabilidad: decidir si una secuencia debe conservarse según los filtros indicados por el usuario
# Entrada: estadísticas de una secuencia y argumentos de los filtros
# Salida: booleano indicando si la secuencia pasa los filtros o no
# =========================================
def pasa_filtros(estadisticas, args):
    if args.min_len > 0 and estadisticas[1] < args.min_len:
        return False
    if args.max_len > 0 and estadisticas[1] > args.max_len:
        return False
    if args.min_gc > 0 and estadisticas[2] < args.min_gc:
        return False
    if args.max_gc > 0 and estadisticas[2] > args.max_gc:
        return False

    return True  # si todas cumplen con false, entonces pasa los filtros


# =========================================
# Escribir resultados en un archivo TSV
# =========================================
# =========================================
# Responsabilidad: escribir resultados en un archivo TSV con encabezados y estadísticas de las secuencias que pasaron los filtros
# Entrada: estadísticas de las secuencias que pasaron los filtros y ruta del archivo de salida
# Salida: archivo TSV con los resultados
# =========================================


def escribir_resultados(stats, ruta):
    ##Esta función escribirá el archivo final en formato TSV.
    # Debe incluir una primera línea con los nombres de las columnas
    with open(ruta, "w") as archivo:
        archivo.write("Encabezado\tLongitud\tGC_Content\n")  # Escribir encabezado
        for estad in stats:
            archivo.write(
                f"{estad[0]}\t{estad[1]}\t{estad[2]:.2f}\n"
            )  # Escribir cada estadística


def main():
    """Punto de entrada principal del programa."""
    args = parsear_argumentos()

    print(f"Leyendo archivo: {args.input}")
    secuencias = leer_fasta(args.input)
    print(f"  {len(secuencias)} secuencias encontradas")

    estadisticas = calcular_estadisticas(secuencias)
    resultados_filtrados = [
        estad for estad in estadisticas if pasa_filtros(estad, args)
    ]
    escribir_resultados(resultados_filtrados, args.output)

    print(f"  {len(resultados_filtrados)} secuencias pasan los filtros")
    print(f"Resultados escritos en '{args.output}'")


if __name__ == "__main__":
    main()
