from playwright.sync_api import sync_playwright

from services.processor import procesar_pedido
from excel.reader import leer_pedido

from ui.main_window import run


URL_CATALOGO = "https://webapp.altamiragroup.com.ar/catalogo"


def mostrar_preview(pedido, ruta_archivo):
    print()
    print("=" * 60)
    print("PEDIDO DETECTADO")
    print("=" * 60)
    print(f"Archivo: {ruta_archivo}")
    print(f"Artículos: {len(pedido)}")
    print()

    print("Primeros artículos:")

    for articulo in pedido[:10]:
        print(
            f'{articulo["codigo"]:<15} '
            f'x {articulo["cantidad"]}'
        )

    if len(pedido) > 10:
        print()
        print(f"... y {len(pedido) - 10} artículos más.")

    print()
    print("=" * 60)


def mostrar_resumen(resultados):
    exitosos = [
        resultado
        for resultado in resultados
        if resultado["estado"] == "ok"
    ]

    errores = [
        resultado
        for resultado in resultados
        if resultado["estado"] == "error"
    ]

    print()
    print("=" * 60)
    print("RESUMEN DEL PROCESAMIENTO")
    print("=" * 60)

    print(f"Total:       {len(resultados)}")
    print(f"Procesados:  {len(exitosos)}")
    print(f"Errores:     {len(errores)}")

    if errores:
        print()
        print("ERRORES:")
        print("-" * 60)

        for resultado in errores:
            print(
                f'- {resultado["codigo"]} '
                f'x {resultado["cantidad"]} '
                f'→ {resultado["error"]}'
            )

    print("=" * 60)

    print()
    print(
        "El procesamiento terminó. "
        "Revisá los errores y luego verificá manualmente "
        "el carrito en Altamira."
    )


def main():
    # Leer pedido
    ruta_archivo = input(
        "Ruta del archivo Excel: "
    ).strip()

    pedido = leer_pedido(ruta_archivo)

    if not pedido:
        print(
            "ERROR: no se encontraron artículos "
            "en el pedido."
        )
        return

    # Preview
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

    resultados = []

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

        resultados = procesar_pedido(
            page,
            pedido
        )

        mostrar_resumen(resultados)

        input(
            "\nPresioná ENTER para cerrar..."
        )

        browser.close()


if __name__ == "__main__":
    run()