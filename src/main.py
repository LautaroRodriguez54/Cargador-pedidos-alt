from playwright.sync_api import sync_playwright

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

            # Agregar artículo
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

            # Esperar a que termine la recarga y aparezca el formulario
            formulario_cantidad = page.locator(
                f'.cantForm[data-codigo="{CODIGO_PRUEBA}"]'
            )

            formulario_cantidad.wait_for(state="visible")

            print("Formulario de cantidad disponible.")

            if formulario_cantidad.count() == 0:
                print(
                    f"ERROR: no se encontró el formulario de cantidad "
                    f"para {CODIGO_PRUEBA}"
                )
            else:
                campo_cantidad = formulario_cantidad.locator(
                    'input[name="cantidad"]'
                )

                boton_confirmar = formulario_cantidad.locator("button")

                campo_cantidad.fill(str(CANTIDAD_PRUEBA))

                print(
                    f"Actualizando cantidad de {CODIGO_PRUEBA} "
                    f"a {CANTIDAD_PRUEBA}..."
                )

                with page.expect_response(
                    lambda response:
                        "/api/v2/carritos/actualizar" in response.url
                        and response.status == 200
                ) as response_info:
                    boton_confirmar.click()

                response = response_info.value

                print("Cantidad actualizada.")
                print("Respuesta:", response.status)

        input("Presioná ENTER para cerrar...")
        browser.close()


if __name__ == "__main__":
    main()