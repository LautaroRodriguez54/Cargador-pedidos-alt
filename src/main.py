from playwright.sync_api import sync_playwright

URL_CATALOGO = "https://webapp.altamiragroup.com.ar/catalogo"
CODIGO_PRUEBA = "2279/00"


def main():
    with sync_playwright() as p:
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()

        page.goto(URL_CATALOGO)

        print("Página abierta.")
        print("URL:", page.url)

        input("Hacé el login manualmente y presioná ENTER cuando termines...")

        # Buscar artículo
        campo_busqueda = page.locator('input[name="busqueda_simple"]')
        campo_busqueda.fill(CODIGO_PRUEBA)
        campo_busqueda.press("Enter")

        page.wait_for_load_state("domcontentloaded")

        print("Búsqueda realizada.")
        print("URL:", page.url)

        # Buscar el botón del artículo
        boton_comprar = page.locator(
            f'.action[data-codigo="{CODIGO_PRUEBA}"]'
        )

        if boton_comprar.count() == 0:
            print(f"ERROR: no se encontró el artículo {CODIGO_PRUEBA}")
        else:
            print(f"Artículo {CODIGO_PRUEBA} encontrado.")
            print("Texto del botón:", boton_comprar.first.inner_text())

            print("Agregando artículo al carrito...")

        with page.expect_response(
            lambda response:
                "/api/v2/carritos/agregar" in response.url
                and response.status == 200
        ) as response_info:
            boton_comprar.first.click()

        response = response_info.value

        print("Artículo agregado.")
        print("Respuesta:", response.status)
        print("URL:", page.url)

        input("Presioná ENTER para cerrar...")

        # Esperar a que termine la navegación
        page.wait_for_load_state("domcontentloaded")

        print("Búsqueda realizada.")
        print("URL:", page.url)

        input("Verificá el resultado en Firefox y presioná ENTER para cerrar...")

        browser.close()


if __name__ == "__main__":
    main()