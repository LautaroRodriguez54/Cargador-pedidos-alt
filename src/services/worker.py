from threading import Event

from PySide6.QtCore import QObject, Signal, Slot
from playwright.sync_api import sync_playwright

from services.processor import procesar_articulo


URL_CATALOGO = (
    "https://webapp.altamiragroup.com.ar/catalogo"
)


class OrderProcessorWorker(QObject):
    """Ejecuta el procesamiento de un pedido en segundo plano."""

    progreso = Signal(int, int)
    articulo_iniciado = Signal(str, int)
    articulo_finalizado = Signal(dict)

    login_requerido = Signal()
    terminado = Signal(list)
    error = Signal(str)
    sesion_cerrada = Signal()

    def __init__(self, pedido):
        super().__init__()

        self.pedido = pedido

        # Controlan la comunicación entre la interfaz y el
        # worker mientras este permanece ocupado procesando.
        self._login_evento = Event()
        self._cerrar_evento = Event()

    @Slot()
    def ejecutar(self):
        """Inicia Playwright, procesa el pedido y mantiene
        Firefox abierto hasta que el usuario cierre la sesión.
        """

        resultados = []

        playwright = None
        browser = None

        try:
            playwright = sync_playwright().start()

            browser = playwright.firefox.launch(
                headless=False
            )

            page = browser.new_page()

            page.goto(URL_CATALOGO)

            # ----------------------------------------------------
            # LOGIN MANUAL
            # ----------------------------------------------------

            self.login_requerido.emit()

            while not self._login_evento.wait(
                timeout=0.1
            ):
                if self._cerrar_evento.is_set():
                    return

            if self._cerrar_evento.is_set():
                return

            # ----------------------------------------------------
            # PROCESAR PEDIDO
            # ----------------------------------------------------

            total = len(self.pedido)

            for numero, articulo in enumerate(
                self.pedido,
                start=1
            ):
                if self._cerrar_evento.is_set():
                    break

                codigo = articulo["codigo"]
                cantidad = articulo["cantidad"]

                self.articulo_iniciado.emit(
                    codigo,
                    numero
                )

                resultado = self._procesar_articulo(
                    codigo,
                    cantidad,
                    page
                )

                resultados.append(resultado)

                self.articulo_finalizado.emit(
                    resultado
                )

                self.progreso.emit(
                    numero,
                    total
                )

            # ----------------------------------------------------
            # RESULTADO
            # ----------------------------------------------------

            if self._cerrar_evento.is_set():
                return

            self.terminado.emit(
                resultados
            )

            # Firefox queda abierto para permitir la revisión
            # manual del carrito.
            while not self._cerrar_evento.wait(
                timeout=0.1
            ):
                pass

        except Exception as exc:
            self.error.emit(
                str(exc)
            )

        finally:
            self._cerrar_playwright(
                browser,
                playwright
            )

            self.sesion_cerrada.emit()

    def _procesar_articulo(
        self,
        codigo,
        cantidad,
        page
    ):
        """Procesa un artículo y captura sus errores."""

        try:
            return procesar_articulo(
                page,
                codigo,
                cantidad
            )

        except Exception as exc:
            return {
                "codigo": codigo,
                "cantidad": cantidad,
                "estado": "error",
                "error": str(exc),
            }

    @staticmethod
    def _cerrar_playwright(
        browser,
        playwright
    ):
        """Cierra Firefox y Playwright de forma segura."""

        if browser is not None:
            try:
                browser.close()
            except Exception:
                pass

        if playwright is not None:
            try:
                playwright.stop()
            except Exception:
                pass

    def continuar_despues_del_login(self):
        """Indica que el usuario terminó el login manual."""

        self._login_evento.set()

    def cerrar_sesion(self):
        """Solicita finalizar la sesión y cerrar Firefox."""

        self._cerrar_evento.set()
        self._login_evento.set()