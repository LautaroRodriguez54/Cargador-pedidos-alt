from playwright.sync_api import sync_playwright

from browser import (
    buscar_articulo,
    agregar_articulo,
    actualizar_cantidad,
)
from excel import leer_pedido


URL_CATALOGO = "https://webapp.altamiragroup.com.ar/catalogo"


def mostrar_preview(pedido, ruta_archivo):
    print()
    print("=" * 60)
    print("PEDIDO DETECTADO")
    print("=" * 60)
    print(f"Archivo: {ruta_archivo}")
    print(f"Artículos: {len(pedido)}")
    print()

    print("Primeros artículos:")

    for articulo in pedido[:10]:
        print(
            f'{articulo["codigo"]:<15} '
            f'x {articulo["cantidad"]}'
        )

    if len(pedido) > 10:
        print()
        print(f"... y {len(pedido) - 10} artículos más.")

    print()
    print("=" * 60)


def procesar_articulo(page, codigo, cantidad):
    """Procesa un artículo y devuelve True si fue exitoso."""

    encontrado = buscar_articulo(
        page,
        codigo
    )

    if not encontrado:
        return False

    agregado = agregar_articulo(
        page,
        codigo
    )

    if not agregado:
        return False

    actualizar_cantidad(
        page,
        codigo,
        cantidad
    )

    return True


def mostrar_resumen(resultados):
    exitosos = [
        resultado
        for resultado in resultados
        if resultado["estado"] == "ok"
    ]

    errores = [
        resultado
        for resultado in resultados
        if resultado["estado"] == "error"
    ]

    print()
    print("=" * 60)
    print("RESUMEN DEL PROCESAMIENTO")
    print("=" * 60)

    print(f"Total:       {len(resultados)}")
    print(f"Procesados:  {len(exitosos)}")
    print(f"Errores:     {len(errores)}")

    if errores:
        print()
        print("ERRORES:")
        print("-" * 60)

        for resultado in errores:
            print(
                f'- {resultado["codigo"]} '
                f'x {resultado["cantidad"]} '
                f'→ {resultado["error"]}'
            )

    print("=" * 60)

    print()
    print(
        "El procesamiento terminó. "
        "Revisá los errores y luego verificá manualmente "
        "el carrito en Altamira."
    )


def main():
    # Leer pedido
    ruta_archivo = input(
        "Ruta del archivo Excel: "
    ).strip()

    pedido = leer_pedido(ruta_archivo)

    if not pedido:
        print(
            "ERROR: no se encontraron artículos "
            "en el pedido."
        )
        return

    # Preview
    mostrar_preview(
        pedido,
        ruta_archivo
    )

    confirmacion = input(
        "\n¿Cargar este pedido? [S/N]: "
    ).strip().lower()

    if confirmacion != "s":
        print("Pedido cancelado.")
        return

    print("\nPedido confirmado.")

    resultados = []

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        page.goto(URL_CATALOGO)

        print("Página abierta.")
        print("URL:", page.url)

        input(
            "Hacé el login manualmente "
            "y presioná ENTER cuando termines..."
        )

        # Por ahora procesamos solamente los primeros 2.
        for numero, articulo in enumerate(
            pedido[:2],
            start=1
        ):
            codigo = articulo["codigo"]
            cantidad = articulo["cantidad"]

            print()
            print(
                f"[{numero}/{len(pedido[:2])}] "
                f"Procesando: {codigo} x {cantidad}"
            )

            try:
                procesado = procesar_articulo(
                    page,
                    codigo,
                    cantidad
                )

                if procesado:
                    print(
                        f"✓ {codigo} x {cantidad}"
                    )

                    resultados.append({
                        "codigo": codigo,
                        "cantidad": cantidad,
                        "estado": "ok",
                    })

                else:
                    print(
                        f"✗ {codigo} x {cantidad}"
                    )

                    resultados.append({
                        "codigo": codigo,
                        "cantidad": cantidad,
                        "estado": "error",
                        "error": "artículo no encontrado "
                                 "o no se pudo agregar",
                    })

            except Exception as error:
                print(
                    f"✗ {codigo} x {cantidad}"
                )
                print(f"  Error: {error}")

                resultados.append({
                    "codigo": codigo,
                    "cantidad": cantidad,
                    "estado": "error",
                    "error": str(error),
                })

        mostrar_resumen(resultados)

        input(
            "\nPresioná ENTER para cerrar..."
        )

        browser.close()


if __name__ == "__main__":
    main()