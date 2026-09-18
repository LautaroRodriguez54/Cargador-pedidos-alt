from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class ResultWindow(QMainWindow):
    """Muestra el resultado final del procesamiento del pedido."""

    cerrar_solicitado = Signal()

    def __init__(self, resultados):
        super().__init__()

        self.resultados = resultados

        self.setWindowTitle(
            "Resultado del pedido - Altamira Bot"
        )

        self.setMinimumSize(
            700,
            550
        )

        self.resize(
            850,
            650
        )

        self._crear_interfaz()

    def _crear_interfaz(self):

        central = QWidget()
        central.setObjectName(
            "central"
        )

        self.setCentralWidget(
            central
        )

        layout = QVBoxLayout(
            central
        )

        layout.setContentsMargins(
            45,
            35,
            45,
            30
        )

        layout.setSpacing(
            18
        )

        # ============================================================
        # TÍTULO
        # ============================================================

        titulo = QLabel(
            "Pedido procesado"
        )

        titulo.setObjectName(
            "titulo"
        )

        subtitulo = QLabel(
            "El procesamiento terminó. "
            "Revisá el resultado antes de cerrar."
        )

        subtitulo.setObjectName(
            "subtitulo"
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            subtitulo
        )

        # ============================================================
        # CLASIFICAR RESULTADOS
        # ============================================================

        exitosos = [
            resultado
            for resultado in self.resultados
            if resultado["estado"] == "ok"
        ]

        errores = [
            resultado
            for resultado in self.resultados
            if resultado["estado"] == "error"
        ]

        # ============================================================
        # RESUMEN
        # ============================================================

        resumen = QFrame()
        resumen.setObjectName(
            "resumen"
        )

        resumen_layout = QHBoxLayout(
            resumen
        )

        resumen_layout.setContentsMargins(
            20,
            16,
            20,
            16
        )

        resumen_layout.setSpacing(
            40
        )

        total_label = QLabel(
            f"<b>Total</b><br>{len(self.resultados)}"
        )

        procesados_label = QLabel(
            f"<b>Procesados</b><br>{len(exitosos)}"
        )

        errores_label = QLabel(
            f"<b>Errores</b><br>{len(errores)}"
        )

        total_label.setObjectName(
            "dato_resumen"
        )

        procesados_label.setObjectName(
            "dato_resumen"
        )

        errores_label.setObjectName(
            "dato_resumen"
        )

        resumen_layout.addWidget(
            total_label
        )

        resumen_layout.addWidget(
            procesados_label
        )

        resumen_layout.addWidget(
            errores_label
        )

        resumen_layout.addStretch()

        layout.addWidget(
            resumen
        )

        # ============================================================
        # RESULTADOS
        # ============================================================

        titulo_resultados = QLabel(
            "Detalle del procesamiento"
        )

        titulo_resultados.setObjectName(
            "titulo_seccion"
        )

        layout.addWidget(
            titulo_resultados
        )

        # ============================================================
        # ÁREA SCROLLABLE
        # ============================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setObjectName(
            "scroll"
        )

        contenido = QWidget()

        contenido_layout = QVBoxLayout(
            contenido
        )

        contenido_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        contenido_layout.setSpacing(
            8
        )

        for resultado in self.resultados:

            codigo = resultado["codigo"]
            cantidad = resultado["cantidad"]
            estado = resultado["estado"]

            fila = QFrame()
            fila.setObjectName(
                "fila"
            )

            fila_layout = QHBoxLayout(
                fila
            )

            fila_layout.setContentsMargins(
                15,
                10,
                15,
                10
            )

            codigo_label = QLabel(
                codigo
            )

            codigo_label.setObjectName(
                "codigo"
            )

            codigo_label.setMinimumWidth(
                180
            )

            cantidad_label = QLabel(
                f"x {cantidad}"
            )

            cantidad_label.setObjectName(
                "cantidad"
            )

            cantidad_label.setMinimumWidth(
                80
            )

            fila_layout.addWidget(
                codigo_label
            )

            fila_layout.addWidget(
                cantidad_label
            )

            fila_layout.addStretch()

            if estado == "ok":

                estado_label = QLabel(
                    "✓ Procesado"
                )

                estado_label.setObjectName(
                    "estado_ok"
                )

            else:

                estado_label = QLabel(
                    "✕ Error"
                )

                estado_label.setObjectName(
                    "estado_error"
                )

            fila_layout.addWidget(
                estado_label
            )

            contenido_layout.addWidget(
                fila
            )

            # --------------------------------------------------------
            # DETALLE DEL ERROR
            # --------------------------------------------------------

            if estado == "error":

                mensaje_error = QLabel(
                    resultado.get(
                        "error",
                        "Error desconocido."
                    )
                )

                mensaje_error.setWordWrap(
                    True
                )

                mensaje_error.setObjectName(
                    "detalle_error"
                )

                contenido_layout.addWidget(
                    mensaje_error
                )

        contenido_layout.addStretch()

        scroll.setWidget(
            contenido
        )

        layout.addWidget(
            scroll,
            stretch=1
        )

        # ============================================================
        # MENSAJE FINAL
        # ============================================================

        if errores:

            mensaje = QLabel(
                f"Se procesaron {len(exitosos)} artículos "
                f"correctamente y se produjeron "
                f"{len(errores)} errores."
            )

            mensaje.setObjectName(
                "mensaje_error"
            )

        else:

            mensaje = QLabel(
                "✓ Todos los artículos fueron "
                "procesados correctamente."
            )

            mensaje.setObjectName(
                "mensaje_ok"
            )

        mensaje.setWordWrap(
            True
        )

        layout.addWidget(
            mensaje
        )

        # ============================================================
        # BOTÓN
        # ============================================================

        botones = QHBoxLayout()

        botones.addStretch()

        cerrar = QPushButton(
            "Cerrar"
        )

        cerrar.setObjectName(
            "boton_cerrar"
        )

        cerrar.setMinimumWidth(
            120
        )

        cerrar.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        cerrar.clicked.connect(
            self.cerrar
        )

        botones.addWidget(
            cerrar
        )

        layout.addLayout(
            botones
        )

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

            QLabel#subtitulo {
                font-size: 15px;
                color: #6b7280;
            }

            QFrame#resumen {
                background-color: white;
                border: 1px solid #d9dde3;
                border-radius: 10px;
            }

            QLabel#dato_resumen {
                color: #202124;
                font-size: 14px;
                min-width: 90px;
            }

            QLabel#titulo_seccion {
                font-size: 18px;
                font-weight: 600;
                color: #202124;
            }

            QScrollArea#scroll {
                background-color: white;
                border: 1px solid #d9dde3;
                border-radius: 8px;
            }

            QScrollArea#scroll > QWidget > QWidget {
                background-color: white;
            }

            QFrame#fila {
                background-color: white;
                border-bottom: 1px solid #e5e7eb;
            }

            QLabel#codigo {
                font-size: 14px;
                color: #202124;
            }

            QLabel#cantidad {
                font-size: 14px;
                color: #6b7280;
            }

            QLabel#estado_ok {
                font-size: 13px;
                font-weight: 600;
                color: #16803c;
            }

            QLabel#estado_error {
                font-size: 13px;
                font-weight: 600;
                color: #c62828;
            }

            QLabel#detalle_error {
                background-color: #fff7f7;
                color: #7f1d1d;
                border: 1px solid #f0caca;
                border-radius: 5px;
                padding: 8px 12px;
                margin-bottom: 5px;
            }

            QLabel#mensaje_ok {
                background-color: #f3faf4;
                color: #166534;
                border: 1px solid #c8e6c9;
                border-radius: 6px;
                padding: 12px;
                font-weight: 600;
            }

            QLabel#mensaje_error {
                background-color: #fff7f7;
                color: #991b1b;
                border: 1px solid #f0caca;
                border-radius: 6px;
                padding: 12px;
                font-weight: 600;
            }

            QPushButton#boton_cerrar {
                background-color: #dc2626;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#boton_cerrar:hover {
                background-color: #b91c1c;
            }

            QPushButton#boton_cerrar:pressed {
                background-color: #991b1b;
            }
        """)

    def cerrar(self):
        """Solicita cerrar la sesión y la ventana de resultados."""

        self.cerrar_solicitado.emit()
        self.close()