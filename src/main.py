from playwright.sync_api import sync_playwright

from browser import (
    buscar_articulo,
    agregar_articulo,
    actualizar_cantidad,
)


URL_CATALOGO = "https://webapp.altamiragroup.com.ar/catalogo"

CODIGO_PRUEBA = "2279/00"
CANTIDAD_PRUEBA = 4


def main():
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

        # Buscar artículo
        encontrado = buscar_articulo(
            page,
            CODIGO_PRUEBA
        )

        if not encontrado:
            input("Presioná ENTER para cerrar...")
            browser.close()
            return

        # Agregar artículo
        agregado = agregar_articulo(
            page,
            CODIGO_PRUEBA
        )

        if not agregado:
            input("Presioná ENTER para cerrar...")
            browser.close()
            return

        # Actualizar cantidad
        actualizar_cantidad(
            page,
            CODIGO_PRUEBA,
            CANTIDAD_PRUEBA
        )

        input("Presioná ENTER para cerrar...")

        browser.close()


if __name__ == "__main__":
    main()