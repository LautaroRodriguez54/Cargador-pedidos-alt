from browser.altamira import (
    buscar_articulo,
    agregar_articulo,
    actualizar_cantidad,
)


def procesar_articulo(
    page,
    codigo,
    cantidad,
):
    """
    Procesa un artículo completo en Altamira.

    Devuelve un diccionario con el resultado del procesamiento.
    """

    try:
        # --------------------------------------------------------
        # BUSCAR ARTÍCULO
        # --------------------------------------------------------

        encontrado = buscar_articulo(
            page,
            codigo,
        )

        if not encontrado:
            return {
                "codigo": codigo,
                "cantidad": cantidad,
                "estado": "error",
                "error": "Artículo no encontrado",
            }

        # --------------------------------------------------------
        # AGREGAR AL CARRITO
        # --------------------------------------------------------

        agregado = agregar_articulo(
            page,
            codigo,
        )

        if not agregado:
            return {
                "codigo": codigo,
                "cantidad": cantidad,
                "estado": "error",
                "error": (
                    "No se pudo agregar el artículo "
                    "al carrito"
                ),
            }

        # --------------------------------------------------------
        # ACTUALIZAR CANTIDAD
        # --------------------------------------------------------

        actualizada = actualizar_cantidad(
            page,
            codigo,
            cantidad,
        )

        if not actualizada:
            return {
                "codigo": codigo,
                "cantidad": cantidad,
                "estado": "error",
                "error": (
                    "No se pudo actualizar "
                    "la cantidad"
                ),
            }

        # --------------------------------------------------------
        # ÉXITO
        # --------------------------------------------------------

        return {
            "codigo": codigo,
            "cantidad": cantidad,
            "estado": "ok",
        }

    except Exception as exc:
        return {
            "codigo": codigo,
            "cantidad": cantidad,
            "estado": "error",
            "error": str(exc),
        }