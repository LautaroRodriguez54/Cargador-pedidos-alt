import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from excel.reader import leer_pedido
from ui.review_window import ReviewWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Altamira Bot")
        self.setMinimumSize(900, 600)
        self.resize(1000, 650)

        self._crear_interfaz()

    def seleccionar_archivo(self):
        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar pedido",
            "",
            "Archivos Excel (*.xlsx *.xls)"
        )

        if not ruta:
            return

        self.archivo_seleccionado.setText(ruta)
        self.estado.setText("Leyendo pedido...")

        try:
            pedido = leer_pedido(ruta)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Error al leer el pedido",
                f"No se pudo leer el archivo.\n\n{error}"
            )

            self.estado.setText(
                "No se pudo leer el pedido."
            )

            return

        if not pedido:
            QMessageBox.warning(
                self,
                "Pedido vacío",
                "No se encontraron artículos válidos "
                "en el archivo seleccionado."
            )

            self.estado.setText(
                "No se encontraron artículos."
            )

            return

        # ------------------------------------------------------------
        # Pedido leído correctamente
        # ------------------------------------------------------------

        self.estado.setText("Pedido cargado")

        self.review_window = ReviewWindow(
            pedido,
            ruta
        )

        self.review_window.cancelado.connect(
            self.pedido_cancelado
        )

        self.hide()
        self.review_window.show()

    def pedido_cancelado(self):
        self.estado.setText(
            "Pedido cancelado."
        )

        self.show()

    def cerrar(self):
        self.close()

    def _crear_interfaz(self):
        # ============================================================
        # VENTANA PRINCIPAL
        # ============================================================

        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout(central)
        layout_principal.setContentsMargins(40, 30, 40, 30)
        layout_principal.setSpacing(0)

        # ============================================================
        # ENCABEZADO
        # ============================================================

        encabezado = QVBoxLayout()
        encabezado.setSpacing(6)

        titulo = QLabel("Altamira Bot")
        titulo.setObjectName("titulo")

        subtitulo = QLabel(
            "Automatización de carga de pedidos"
        )
        subtitulo.setObjectName("subtitulo")

        encabezado.addWidget(titulo)
        encabezado.addWidget(subtitulo)

        layout_principal.addLayout(encabezado)

        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setObjectName("separador")

        layout_principal.addSpacing(25)
        layout_principal.addWidget(separador)
        layout_principal.addSpacing(35)

        # ============================================================
        # TARJETA PRINCIPAL
        # ============================================================

        tarjeta = QFrame()
        tarjeta.setObjectName("tarjeta")

        layout_tarjeta = QVBoxLayout(tarjeta)
        layout_tarjeta.setContentsMargins(35, 30, 35, 30)
        layout_tarjeta.setSpacing(0)

        titulo_tarjeta = QLabel("Nuevo pedido")
        titulo_tarjeta.setObjectName("titulo_tarjeta")

        descripcion = QLabel(
            "Seleccioná un archivo Excel para comenzar."
        )
        descripcion.setObjectName("descripcion")

        descripcion.setWordWrap(True)

        layout_tarjeta.addWidget(titulo_tarjeta)
        layout_tarjeta.addSpacing(8)
        layout_tarjeta.addWidget(descripcion)

        # ------------------------------------------------------------
        # ÁREA DEL ARCHIVO
        # ------------------------------------------------------------

        layout_tarjeta.addSpacing(30)

        area_archivo = QFrame()
        area_archivo.setObjectName("area_archivo")

        layout_archivo = QHBoxLayout(area_archivo)
        layout_archivo.setContentsMargins(20, 16, 20, 16)

        info_archivo = QVBoxLayout()
        info_archivo.setSpacing(4)

        etiqueta_archivo = QLabel("Archivo de pedido")
        etiqueta_archivo.setObjectName("etiqueta_archivo")

        self.archivo_seleccionado = QLabel("Ningún archivo seleccionado")
        self.archivo_seleccionado.setObjectName("nombre_archivo")

        info_archivo.addWidget(etiqueta_archivo)
        info_archivo.addWidget(self.archivo_seleccionado)

        layout_archivo.addLayout(info_archivo)
        layout_archivo.addStretch()

        layout_tarjeta.addWidget(area_archivo)

        # ------------------------------------------------------------
        # BOTÓN
        # ------------------------------------------------------------

        layout_tarjeta.addSpacing(30)

        self.boton_archivo = QPushButton("Seleccionar archivo")
        self.boton_archivo.setObjectName("boton_principal")
        self.boton_archivo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.boton_archivo.clicked.connect(self.seleccionar_archivo)

        self.boton_archivo.setSizePolicy(
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Fixed
        )

        layout_tarjeta.addWidget(
            self.boton_archivo,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        # ------------------------------------------------------------
        # ESTADO
        # ------------------------------------------------------------

        layout_tarjeta.addSpacing(25)

        estado = QLabel(
            "Esperando un pedido..."
        )
        estado.setObjectName("estado")

        layout_tarjeta.addWidget(estado)

        layout_principal.addWidget(tarjeta)

        # ============================================================
        # ESPACIO
        # ============================================================

        layout_principal.addStretch()

        # ============================================================
        # PIE
        # ============================================================

        pie = QHBoxLayout()

        version = QLabel("Altamira Bot")
        version.setObjectName("version")

        pie.addWidget(version)
        pie.addStretch()

        self.estado = QPushButton("Listo")
        self.estado.setObjectName("statusButton")
        self.estado.setCursor(Qt.CursorShape.PointingHandCursor)
        self.estado.clicked.connect(self.cerrar)

        pie.addWidget(self.estado)

        layout_principal.addLayout(pie)

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

            QLabel#titulo_tarjeta {
                font-size: 21px;
                font-weight: 600;
                color: #202124;
            }

            QLabel#descripcion {
                font-size: 14px;
                color: #6b7280;
            }

            QFrame#area_archivo {
                background-color: #f8f9fa;
                border: 1px solid #dfe3e8;
                border-radius: 7px;
            }

            QLabel#etiqueta_archivo {
                font-size: 12px;
                font-weight: 600;
                color: #6b7280;
            }

            QLabel#nombre_archivo {
                font-size: 14px;
                color: #343a40;
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

            QLabel#estado {
                font-size: 13px;
                color: #6b7280;
            }

            QLabel#version {
                font-size: 12px;
                color: #9aa0a6;
            }

            QLabel#estado_sistema {
                font-size: 12px;
                color: #16803c;
                font-weight: 600;
            }
        """)

        self.estado.setStyleSheet("""
            QPushButton#statusButton {
                border: 1px solid transparent;
                border-radius: 5px;
                background: transparent;
                color: #168000;
                font-weight: bold;
                padding: 5px 9px;
            }

            QPushButton#statusButton:hover {
                background-color: #eef8f0;
                border: 1px solid #b9ddc0;
                color: #0f5f00;
            }

            QPushButton#statusButton:pressed {
                background-color: #dcefe0;
                border: 1px solid #9fcda8;
            }
        """)


def run():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()