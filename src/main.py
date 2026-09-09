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

    print(f"{'Código':<15} {'Cantidad':>10}")
    print("-" * 27)

    for articulo in pedido:
        print(
            f'{articulo["codigo"]:<15} '
            f'{articulo["cantidad"]:>10}'
        )

    print("=" * 60)


def main():
    # Leer pedido
    ruta_archivo = input(
        "Ruta del archivo Excel: "
    ).strip()

    pedido = leer_pedido(ruta_archivo)

    if not pedido:
        print("ERROR: no se encontraron artículos en el pedido.")
        return

    # Mostrar preview
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
        for articulo in pedido[:2]:

            codigo = articulo["codigo"]
            cantidad = articulo["cantidad"]

            print()
            print(f"Procesando: {codigo} x {cantidad}")

            encontrado = buscar_articulo(
                page,
                codigo
            )

            if not encontrado:
                print(f"ERROR: no se encontró {codigo}")
                continue

            agregado = agregar_articulo(
                page,
                codigo
            )

            if not agregado:
                print(
                    f"ERROR: no se pudo agregar {codigo}"
                )
                continue

            actualizar_cantidad(
                page,
                codigo,
                cantidad
            )

            print(f"✓ {codigo} x {cantidad}")

        input(
            "\nPrueba finalizada. "
            "Presioná ENTER para cerrar..."
        )

        browser.close()


if __name__ == "__main__":
    main()