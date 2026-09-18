from playwright.sync_api import Page


def buscar_articulo(page: Page, codigo: str) -> bool:
    """Busca un artículo en el catálogo y verifica que exista."""

    campo_busqueda = page.locator(
        'input[name="busqueda_simple"]'
    )

    campo_busqueda.fill(codigo)
    campo_busqueda.press("Enter")

    page.wait_for_load_state(
        "domcontentloaded"
    )

    boton_articulo = page.locator(
        f'.action[data-codigo="{codigo}"]'
    )

    return boton_articulo.count() > 0


def agregar_articulo(page: Page, codigo: str) -> bool:
    """
    Agrega un artículo al carrito si todavía no está agregado.

    Si el artículo ya está en el carrito, no vuelve a agregarlo.
    """

    boton_articulo = page.locator(
        f'.action[data-codigo="{codigo}"]'
    )

    if boton_articulo.count() == 0:
        return False

    boton = boton_articulo.first

    clase = boton.get_attribute("class") or ""
    texto = boton.inner_text().strip().lower()

    # El artículo ya está en el carrito.
    # Volver a hacer click lo eliminaría.
    if "added" in clase or texto == "eliminar":
        return True

    with page.expect_response(
        lambda response:
            "/api/v2/carritos/agregar" in response.url
            and response.status == 200
    ):
        boton.click()

    return True


def actualizar_cantidad(
    page: Page,
    codigo: str,
    cantidad: int,
) -> bool:
    """Actualiza la cantidad de un artículo del carrito."""

    formulario_cantidad = page.locator(
        f'.cantForm[data-codigo="{codigo}"]'
    )

    formulario_cantidad.wait_for(
        state="visible"
    )

    campo_cantidad = formulario_cantidad.locator(
        'input[name="cantidad"]'
    )

    boton_confirmar = formulario_cantidad.locator(
        "button"
    )

    campo_cantidad.fill(
        str(cantidad)
    )

    with page.expect_response(
        lambda response:
            "/api/v2/carritos/actualizar" in response.url
            and response.status == 200
    ):
        boton_confirmar.click()

    return True