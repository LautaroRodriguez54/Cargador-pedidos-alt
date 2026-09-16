from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
)


class ProcessingWindow(QMainWindow):

    def __init__(self, total):
        super().__init__()

        self.total = total

        self.setWindowTitle(
            "Procesando pedido - Altamira Bot"
        )

        self.setMinimumSize(600, 400)

        self._crear_interfaz()

    def _crear_interfaz(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        layout.setContentsMargins(
            50, 50, 50, 50
        )

        layout.setSpacing(20)

        titulo = QLabel(
            "Procesando pedido"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
        """)

        self.estado = QLabel(
            "Preparando..."
        )

        self.estado.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.estado.setStyleSheet("""
            font-size: 16px;
            color: #6b7280;
        """)

        self.progreso = QProgressBar()

        self.progreso.setRange(
            0,
            self.total
        )

        self.progreso.setValue(0)

        self.contador = QLabel(
            f"0 / {self.total}"
        )

        self.contador.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addStretch()

        layout.addWidget(titulo)
        layout.addWidget(self.estado)
        layout.addWidget(self.progreso)
        layout.addWidget(self.contador)

        layout.addStretch()

    def actualizar_articulo(
        self,
        codigo,
        numero
    ):
        self.estado.setText(
            f"Procesando artículo: {codigo}"
        )

        self.contador.setText(
            f"{numero} / {self.total}"
        )

    def actualizar_progreso(
        self,
        numero,
        total
    ):
        self.progreso.setValue(
            numero
        )