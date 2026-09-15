from browser.altamira import (
    buscar_articulo,
    agregar_articulo,
    actualizar_cantidad,
)


def procesar_articulo(page, codigo, cantidad):
    """
    Procesa un artículo completo en Altamira.

    Devuelve un diccionario con el resultado
    del procesamiento.
    """

    try:
        encontrado = buscar_articulo(
            page,
            codigo
        )

        if not encontrado:
            return {
                "codigo": codigo,
                "cantidad": cantidad,
                "estado": "error",
                "error": "Artículo no encontrado",
            }

        agregado = agregar_articulo(
            page,
            codigo
        )

        if not agregado:
            return {
                "codigo": codigo,
                "cantidad": cantidad,
                "estado": "error",
                "error": "No se pudo agregar el artículo",
            }

        actualizada = actualizar_cantidad(
            page,
            codigo,
            cantidad
        )

        if not actualizada:
            return {
                "codigo": codigo,
                "cantidad": cantidad,
                "estado": "error",
                "error": "No se pudo actualizar la cantidad",
            }

        return {
            "codigo": codigo,
            "cantidad": cantidad,
            "estado": "ok",
        }

    except Exception as error:
        return {
            "codigo": codigo,
            "cantidad": cantidad,
            "estado": "error",
            "error": str(error),
        }


def procesar_pedido(page, pedido):
    """
    Procesa todos los artículos de un pedido.

    Devuelve una lista con el resultado de cada artículo.
    """

    resultados = []

    for articulo in pedido:
        resultado = procesar_articulo(
            page,
            articulo["codigo"],
            articulo["cantidad"]
        )

        resultados.append(resultado)

    return resultados