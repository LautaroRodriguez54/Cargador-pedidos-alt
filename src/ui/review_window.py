from pathlib import Path

from PySide6.QtCore import (
    Qt,
    Signal,
    QTimer,
    QThread,
)

from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.worker import OrderProcessorWorker

from ui.processing_window import ProcessingWindow
from ui.result_window import ResultWindow


class ReviewWindow(QMainWindow):

    confirmado = Signal()
    cancelado = Signal()

    def __init__(self, pedido, ruta_archivo):
        super().__init__()

        self.pedido = pedido
        self.ruta_archivo = ruta_archivo

        self.thread = None
        self.worker = None

        self.processing_window = None
        self.result_window = None

        self.setWindowTitle(
            "Revisar pedido - Altamira Bot"
        )

        self.setMinimumSize(
            900,
            600
        )

        self.resize(
            1000,
            700
        )

        self._crear_interfaz()

    def _crear_interfaz(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout(central)

        layout_principal.setContentsMargins(
            40,
            30,
            40,
            30
        )

        layout_principal.setSpacing(0)

        # ============================================================
        # ENCABEZADO
        # ============================================================

        titulo = QLabel(
            "Revisar pedido"
        )

        titulo.setObjectName(
            "titulo"
        )

        subtitulo = QLabel(
            "Verificá los artículos antes de comenzar la carga."
        )

        subtitulo.setObjectName(
            "subtitulo"
        )

        layout_principal.addWidget(
            titulo
        )

        layout_principal.addSpacing(
            6
        )

        layout_principal.addWidget(
            subtitulo
        )

        # ============================================================
        # SEPARADOR
        # ============================================================

        separador = QFrame()

        separador.setFrameShape(
            QFrame.Shape.HLine
        )

        separador.setObjectName(
            "separador"
        )

        layout_principal.addSpacing(
            25
        )

        layout_principal.addWidget(
            separador
        )

        layout_principal.addSpacing(
            25
        )

        # ============================================================
        # INFORMACIÓN DEL PEDIDO
        # ============================================================

        tarjeta_info = QFrame()

        tarjeta_info.setObjectName(
            "tarjeta"
        )

        layout_info = QVBoxLayout(
            tarjeta_info
        )

        layout_info.setContentsMargins(
            25,
            20,
            25,
            20
        )

        layout_info.setSpacing(
            6
        )

        nombre_archivo = Path(
            self.ruta_archivo
        ).name

        archivo = QLabel(
            f"<b>Archivo:</b> {nombre_archivo}"
        )

        archivo.setObjectName(
            "info"
        )

        cantidad = QLabel(
            f"<b>Artículos:</b> {len(self.pedido)}"
        )

        cantidad.setObjectName(
            "info"
        )

        layout_info.addWidget(
            archivo
        )

        layout_info.addWidget(
            cantidad
        )

        layout_principal.addWidget(
            tarjeta_info
        )

        layout_principal.addSpacing(
            20
        )

        # ============================================================
        # TABLA
        # ============================================================

        self.tabla = QTableWidget()

        self.tabla.setObjectName(
            "tabla"
        )

        self.tabla.setColumnCount(
            2
        )

        self.tabla.setHorizontalHeaderLabels(
            [
                "Código",
                "Cantidad"
            ]
        )

        self.tabla.setRowCount(
            len(self.pedido)
        )

        for fila, articulo in enumerate(
            self.pedido
        ):
            codigo = QTableWidgetItem(
                articulo["codigo"]
            )

            cantidad = QTableWidgetItem(
                str(
                    articulo["cantidad"]
                )
            )

            cantidad.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.tabla.setItem(
                fila,
                0,
                codigo
            )

            self.tabla.setItem(
                fila,
                1,
                cantidad
            )

        self.tabla.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.tabla.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.tabla.verticalHeader().setVisible(
            False
        )

        header = self.tabla.horizontalHeader()

        header.setStretchLastSection(
            True
        )

        header.resizeSection(
            0,
            500
        )

        layout_principal.addWidget(
            self.tabla
        )

        # ============================================================
        # BOTONES
        # ============================================================

        layout_principal.addSpacing(
            20
        )

        botones = QHBoxLayout()

        boton_cancelar = QPushButton(
            "Cancelar"
        )

        boton_cancelar.setObjectName(
            "boton_secundario"
        )

        boton_cancelar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        boton_cancelar.clicked.connect(
            self.cancelar
        )

        boton_confirmar = QPushButton(
            "Cargar pedido"
        )

        boton_confirmar.setObjectName(
            "boton_principal"
        )

        boton_confirmar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        boton_confirmar.clicked.connect(
            self.confirmar
        )

        botones.addWidget(
            boton_cancelar
        )

        botones.addStretch()

        botones.addWidget(
            boton_confirmar
        )

        layout_principal.addLayout(
            botones
        )

        # ============================================================
        # ESTILOS
        # ============================================================

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f5f7;
            }

            QWidget {
                font-family: "Segoe UI";
                color: #202124;
            }

            QLabel#titulo {
                font-size: 30px;
                font-weight: 700;
                color: #202124;
            }

            QLabel#subtitulo {
                font-size: 15px;
                color: #6b7280;
            }

            QFrame#separador {
                color: #dfe1e5;
                background-color: #dfe1e5;
                max-height: 1px;
            }

            QFrame#tarjeta {
                background-color: white;
                border: 1px solid #e1e4e8;
                border-radius: 10px;
            }

            QLabel#info {
                font-size: 14px;
                color: #4b5563;
            }

            QTableWidget#tabla {
                background-color: white;
                border: 1px solid #e1e4e8;
                border-radius: 8px;
                gridline-color: #e5e7eb;
                font-size: 14px;
                selection-background-color: #f3f4f6;
                selection-color: #202124;
            }

            QHeaderView::section {
                background-color: #f8f9fa;
                color: #374151;
                font-size: 13px;
                font-weight: 600;
                padding: 10px;
                border: none;
                border-bottom: 1px solid #dfe3e8;
            }

            QPushButton#boton_principal {
                background-color: #d92d2d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 11px 22px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#boton_principal:hover {
                background-color: #c32626;
            }

            QPushButton#boton_principal:pressed {
                background-color: #aa1f1f;
            }

            QPushButton#boton_secundario {
                background-color: white;
                color: #4b5563;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#boton_secundario:hover {
                background-color: #f9fafb;
            }

            QPushButton#boton_secundario:pressed {
                background-color: #f3f4f6;
            }

            QLabel#toast {
                background-color: #202124;
                color: white;
                border-radius: 8px;
                padding: 12px 18px;
                font-size: 14px;
                font-weight: 600;
            }
        """)

    # ================================================================
    # TOAST
    # ================================================================

    def mostrar_toast(self):

        toast = QLabel(
            f"✓  Pedido cargado\n"
            f"{len(self.pedido)} artículos detectados"
        )

        toast.setObjectName(
            "toast"
        )

        toast.setParent(
            self
        )

        toast.adjustSize()

        margen = 30

        x = (
            self.width()
            - toast.width()
            - margen
        )

        y = margen

        toast.move(
            x,
            y
        )

        toast.show()
        toast.raise_()

        QTimer.singleShot(
            3000,
            toast.deleteLater
        )

    # ================================================================
    # INICIAR PROCESAMIENTO
    # ================================================================

    def confirmar(self):

        self.confirmado.emit()

        self.processing_window = ProcessingWindow(
            len(self.pedido)
        )

        self.thread = QThread()

        self.worker = OrderProcessorWorker(
            self.pedido
        )

        self.worker.moveToThread(
            self.thread
        )

        # ============================================================
        # THREAD → WORKER
        # ============================================================

        self.thread.started.connect(
            self.worker.ejecutar
        )

        # ============================================================
        # WORKER → PROCESSING WINDOW
        # ============================================================

        self.worker.login_requerido.connect(
            self.processing_window.mostrar_login
        )

        self.processing_window.continuar_login.connect(
            self.worker.continuar_despues_del_login,
            Qt.ConnectionType.DirectConnection
        )

        self.worker.articulo_iniciado.connect(
            self.processing_window.actualizar_articulo
        )

        self.worker.progreso.connect(
            self.processing_window.actualizar_progreso
        )

        # ============================================================
        # FINALIZACIÓN
        # ============================================================

        self.worker.terminado.connect(
            self.procesamiento_terminado
        )

        self.worker.error.connect(
            self.procesamiento_error
        )

        self.worker.sesion_cerrada.connect(
            self.sesion_cerrada
        )

        # ============================================================
        # LIMPIEZA DEL THREAD
        # ============================================================

        self.thread.finished.connect(
            self.worker.deleteLater
        )

        self.thread.finished.connect(
            self.thread.deleteLater
        )

        self.thread.finished.connect(
            QApplication.instance().quit
        )

        # ============================================================
        # MOSTRAR VENTANA
        # ============================================================

        self.close()

        self.processing_window.show()

        self.thread.start()

    # ================================================================
    # PROCESAMIENTO TERMINADO
    # ================================================================

    def procesamiento_terminado(
        self,
        resultados
    ):
        self.processing_window.close()

        self.result_window = ResultWindow(
            resultados
        )

        self.result_window.cerrar_solicitado.connect(
            self.cerrar_sesion
        )

        self.result_window.show()

    # ================================================================
    # CERRAR SESIÓN DE PLAYWRIGHT
    # ================================================================

    def cerrar_sesion(self):

        if self.worker is not None:

            self.worker.cerrar_sesion()

    # ================================================================
    # SESIÓN CERRADA
    # ================================================================

    def sesion_cerrada(self):

        if self.thread is not None:

            self.thread.quit()

    # ================================================================
    # ERROR
    # ================================================================

    def procesamiento_error(
        self,
        mensaje
    ):

        if self.processing_window is not None:

            self.processing_window.close()

        self.result_window = ResultWindow(
            [
                {
                    "codigo": "PROCESAMIENTO",
                    "cantidad": 0,
                    "estado": "error",
                    "error": mensaje,
                }
            ]
        )

        self.result_window.cerrar_solicitado.connect(
            self.cerrar_sesion
        )

        self.result_window.show()

    # ================================================================
    # CANCELAR
    # ================================================================

    def cancelar(self):

        self.cancelado.emit()
        self.close()