from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ProcessingWindow(QMainWindow):
    """Muestra el login manual y el progreso del procesamiento."""

    continuar_login = Signal()

    def __init__(self, total):
        super().__init__()

        self.total = total

        self.setWindowTitle(
            "Procesando pedido - Altamira Bot"
        )

        self.setMinimumSize(
            650,
            450
        )

        self.resize(
            700,
            500
        )

        self._crear_interfaz()

    def _crear_interfaz(self):

        central = QWidget()
        central.setObjectName("central")

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout(
            central
        )

        layout.setContentsMargins(
            50,
            45,
            50,
            40
        )

        layout.setSpacing(
            20
        )

        # ============================================================
        # TÍTULO
        # ============================================================

        self.titulo = QLabel(
            "Preparando pedido"
        )

        self.titulo.setObjectName(
            "titulo"
        )

        self.titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.titulo
        )

        # ============================================================
        # DESCRIPCIÓN
        # ============================================================

        self.descripcion = QLabel(
            "Firefox se está preparando."
        )

        self.descripcion.setObjectName(
            "descripcion"
        )

        self.descripcion.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.descripcion.setWordWrap(
            True
        )

        layout.addWidget(
            self.descripcion
        )

        # ============================================================
        # TARJETA DE LOGIN
        # ============================================================

        self.login_frame = QFrame()
        self.login_frame.setObjectName(
            "login_frame"
        )

        login_layout = QVBoxLayout(
            self.login_frame
        )

        login_layout.setContentsMargins(
            25,
            20,
            25,
            20
        )

        login_layout.setSpacing(
            10
        )

        login_titulo = QLabel(
            "Iniciá sesión en Altamira"
        )

        login_titulo.setObjectName(
            "login_titulo"
        )

        login_descripcion = QLabel(
            "Completá el login en la ventana de Firefox. "
            "Cuando hayas terminado, presioná "
            "«Continuar»."
        )

        login_descripcion.setObjectName(
            "login_descripcion"
        )

        login_descripcion.setWordWrap(
            True
        )

        self.boton_continuar = QPushButton(
            "Continuar"
        )

        self.boton_continuar.setObjectName(
            "boton_continuar"
        )

        self.boton_continuar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.boton_continuar.clicked.connect(
            self.login_confirmado
        )

        login_layout.addWidget(
            login_titulo
        )

        login_layout.addWidget(
            login_descripcion
        )

        login_layout.addSpacing(
            10
        )

        login_layout.addWidget(
            self.boton_continuar,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.login_frame
        )

        # ============================================================
        # ÁREA DE PROGRESO
        # ============================================================

        self.progreso_frame = QFrame()
        self.progreso_frame.setObjectName(
            "progreso_frame"
        )

        progreso_layout = QVBoxLayout(
            self.progreso_frame
        )

        progreso_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        progreso_layout.setSpacing(
            15
        )

        self.estado = QLabel(
            "Esperando inicio..."
        )

        self.estado.setObjectName(
            "estado"
        )

        self.estado.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.progreso = QProgressBar()

        self.progreso.setRange(
            0,
            self.total
        )

        self.progreso.setValue(
            0
        )

        self.progreso.setTextVisible(
            True
        )

        self.contador = QLabel(
            f"0 / {self.total}"
        )

        self.contador.setObjectName(
            "contador"
        )

        self.contador.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        progreso_layout.addWidget(
            self.estado
        )

        progreso_layout.addWidget(
            self.progreso
        )

        progreso_layout.addWidget(
            self.contador
        )

        layout.addWidget(
            self.progreso_frame
        )

        layout.addStretch()

        # La pantalla comienza mostrando únicamente
        # la sección de login.
        self.progreso_frame.hide()

        # ============================================================
        # ESTILOS
        # ============================================================

        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f5f7;
            }

            QWidget#central {
                background-color: #f4f5f7;
                color: #202124;
                font-family: "Segoe UI";
            }

            QLabel {
                color: #202124;
            }

            QLabel#titulo {
                font-size: 28px;
                font-weight: 700;
                color: #202124;
            }

            QLabel#descripcion {
                font-size: 15px;
                color: #6b7280;
            }

            QFrame#login_frame {
                background-color: white;
                border: 1px solid #d9dde3;
                border-radius: 10px;
            }

            QLabel#login_titulo {
                font-size: 18px;
                font-weight: 600;
                color: #202124;
            }

            QLabel#login_descripcion {
                font-size: 14px;
                color: #6b7280;
            }

            QPushButton#boton_continuar {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 24px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#boton_continuar:hover {
                background-color: #b91c1c;
            }

            QPushButton#boton_continuar:pressed {
                background-color: #991b1b;
            }

            QLabel#estado {
                font-size: 15px;
                color: #6b7280;
            }

            QProgressBar {
                background-color: white;
                border: 1px solid #d9dde3;
                border-radius: 6px;
                height: 18px;
                text-align: center;
            }

            QProgressBar::chunk {
                background-color: #dc2626;
                border-radius: 5px;
            }

            QLabel#contador {
                font-size: 14px;
                color: #4b5563;
                font-weight: 600;
            }
        """)

    # ============================================================
    # LOGIN
    # ============================================================

    def mostrar_login(self):
        """Muestra la interfaz de login manual."""

        self.titulo.setText(
            "Iniciá sesión en Altamira"
        )

        self.descripcion.setText(
            "Firefox está abierto. "
            "Completá el login y continuá."
        )

        self.login_frame.show()
        self.progreso_frame.hide()

        self.boton_continuar.setEnabled(
            True
        )

    def login_confirmado(self):
        """Confirma el login y comienza a mostrar el progreso."""

        self.boton_continuar.setEnabled(
            False
        )

        self.titulo.setText(
            "Procesando pedido"
        )

        self.descripcion.setText(
            "La carga del pedido está en progreso."
        )

        self.login_frame.hide()
        self.progreso_frame.show()

        self.continuar_login.emit()

    # ============================================================
    # PROGRESO
    # ============================================================

    def actualizar_articulo(
        self,
        codigo,
        numero
    ):
        """Actualiza el artículo que se está procesando."""

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
        """Actualiza la barra y el contador de progreso."""

        self.progreso.setMaximum(
            total
        )

        self.progreso.setValue(
            numero
        )

        self.contador.setText(
            f"{numero} / {total}"
        )