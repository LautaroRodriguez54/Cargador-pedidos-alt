from playwright.sync_api import Page


def buscar_articulo(page: Page, codigo: str) -> bool:
    """Busca un artículo en el catálogo y verifica que exista."""

    campo_busqueda = page.locator('input[name="busqueda_simple"]')
    campo_busqueda.fill(codigo)
    campo_busqueda.press("Enter")

    page.wait_for_load_state("domcontentloaded")

    boton_comprar = page.locator(
        f'.action[data-codigo="{codigo}"]'
    )

    if boton_comprar.count() == 0:
        print(f"ERROR: no se encontró el artículo {codigo}")
        return False

    print(f"Artículo {codigo} encontrado.")
    print("Texto del botón:", boton_comprar.first.inner_text())

    return True


def agregar_articulo(page: Page, codigo: str) -> bool:
    """Agrega un artículo al carrito."""

    boton_comprar = page.locator(
        f'.action[data-codigo="{codigo}"]'
    )

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

    return True


def actualizar_cantidad(
    page: Page,
    codigo: str,
    cantidad: int
) -> bool:
    """Actualiza la cantidad de un artículo del carrito."""

    formulario_cantidad = page.locator(
        f'.cantForm[data-codigo="{codigo}"]'
    )

    formulario_cantidad.wait_for(state="visible")

    print("Formulario de cantidad disponible.")

    campo_cantidad = formulario_cantidad.locator(
        'input[name="cantidad"]'
    )

    boton_confirmar = formulario_cantidad.locator("button")

    campo_cantidad.fill(str(cantidad))

    print(
        f"Actualizando cantidad de {codigo} "
        f"a {cantidad}..."
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

    return True