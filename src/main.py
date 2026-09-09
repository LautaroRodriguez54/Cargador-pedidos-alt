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

        # Esperar a que termine la navegación
        page.wait_for_load_state("domcontentloaded")

        print("Búsqueda realizada.")
        print("URL:", page.url)

        input("Verificá el resultado en Firefox y presioná ENTER para cerrar...")

        browser.close()


if __name__ == "__main__":
    main()