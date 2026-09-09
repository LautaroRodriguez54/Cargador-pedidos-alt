from playwright.sync_api import sync_playwright

from browser import (
    buscar_articulo,
    agregar_articulo,
    actualizar_cantidad,
)
from excel import leer_pedido


URL_CATALOGO = "https://webapp.altamiragroup.com.ar/catalogo"


def main():
    # Leer pedido
    ruta_archivo = input("Ruta del archivo Excel: ").strip()

    pedido = leer_pedido(ruta_archivo)

    print()
    print(f"Artículos encontrados: {len(pedido)}")
    print()

    for articulo in pedido[:2]:
        print(
            f'{articulo["codigo"]} x {articulo["cantidad"]}'
        )

    input(
        "\nPresioná ENTER para abrir Firefox "
        "y procesar los primeros 2 artículos..."
    )

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

        # Procesar solamente los primeros 2 artículos
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
                print(f"ERROR: no se pudo agregar {codigo}")
                continue

            actualizar_cantidad(
                page,
                codigo,
                cantidad
            )

            print(f"✓ {codigo} x {cantidad}")

        input("\nPrueba finalizada. Presioná ENTER para cerrar...")

        browser.close()


if __name__ == "__main__":
    main()