from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QCheckBox, QListWidget, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pandas as pd
import os

from plot_manager import create_plot, apply_plot_style, toggle_line_visibility, toggle_symbol_visibility, update_controls_from_plot
from file_loader import load_csv_with_separator
from sp_loader import try_load_sp_file
from utils import is_color_dark

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CSV Plotter con Drag&Drop e scelta separatore")
        self.resize(900, 700)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout()
        central.setLayout(layout)

        self.setAcceptDrops(True)

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('w')
        self.plot_widget.showGrid(x=True, y=True)
        layout.addWidget(self.plot_widget, stretch=4)

        self.plot_list = QListWidget()
        layout.addWidget(QLabel("Grafici:"))
        layout.addWidget(self.plot_list, stretch=1)

        controls = QHBoxLayout()
        layout.addLayout(controls)

        self.color_btn = QPushButton("Cambia Colore")
        self.color_btn.clicked.connect(self.change_color)
        controls.addWidget(self.color_btn)

        self.show_line_cb = QCheckBox("Mostra Linea")
        self.show_line_cb.setChecked(True)
        self.show_line_cb.stateChanged.connect(self.on_toggle_line)
        controls.addWidget(self.show_line_cb)

        self.show_symbol_cb = QCheckBox("Mostra Simboli")
        self.show_symbol_cb.setChecked(False)
        self.show_symbol_cb.stateChanged.connect(self.on_toggle_symbol)
        controls.addWidget(self.show_symbol_cb)

        self.load_btn = QPushButton("Carica CSV/SP")
        self.load_btn.clicked.connect(self.load_csv_dialog)
        controls.addWidget(self.load_btn)

        self.clear_btn = QPushButton("Pulisci Dati")
        self.clear_btn.clicked.connect(self.clear_data)
        controls.addWidget(self.clear_btn)

        self.data = None
        self.plots = []
        self.plot_colors = []
        self.color_sequence = ['k', 'r', 'g', 'b', 'c', 'm', '#804000']

        self.plot_list.currentRowChanged.connect(self.on_plot_selected)
        self.selected_index = -1

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(('.csv', '.sp')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            self.load_csv(file_path)

    def load_csv_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleziona file CSV o SP", "", "CSV/SP Files (*.csv *.sp)")
        if file_path:
            self.load_csv(file_path)

    def load_csv(self, file_path):
        if file_path.lower().endswith(".sp"):
            result = try_load_sp_file(file_path, self)
            if result is None:
                return
            x, y, reverse_x = result

            self.plot_widget.clear()
            self.plot_widget.getViewBox().invertX(reverse_x)
            self.plots.clear()
            self.plot_colors.clear()
            self.plot_list.clear()

            color = self.color_sequence[0]
            plot_item = create_plot(self.plot_widget, x, y, color, "Spettro IR")
            self.plots.append(plot_item)
            self.plot_colors.append(QColor(color))
            self.plot_list.addItem("Spettro IR")
            self.plot_widget.addLegend()
            self.selected_index = 0
            self.plot_list.setCurrentRow(0)
            update_controls_from_plot(self)
            return

        self.data = load_csv_with_separator(file_path, self)
        if self.data is None:
            return

        numeric_cols = self.data.select_dtypes(include='number').columns
        if len(numeric_cols) < 2:
            QMessageBox.warning(self, "Attenzione", "Il CSV deve contenere almeno due colonne numeriche")
            return

        self.plot_widget.clear()
        self.plot_widget.getViewBox().invertX(False)
        self.plots.clear()
        self.plot_colors.clear()
        self.plot_list.clear()

        for i in range(0, len(numeric_cols)-1, 2):
            x = self.data[numeric_cols[i]]
            y = self.data[numeric_cols[i+1]]
            color = self.color_sequence[len(self.plots) % len(self.color_sequence)]
            plot_item = create_plot(self.plot_widget, x, y, color, str(numeric_cols[i+1]))
            self.plots.append(plot_item)
            self.plot_colors.append(QColor(color))
            self.plot_list.addItem(f"{numeric_cols[i+1]} vs {numeric_cols[i]}")

        self.plot_widget.addLegend()
        self.selected_index = 0
        self.plot_list.setCurrentRow(0)
        update_controls_from_plot(self)

    def clear_data(self):
        self.plot_widget.clear()
        self.plots.clear()
        self.plot_colors.clear()
        self.plot_list.clear()
        self.data = None
        self.selected_index = -1
        self.show_line_cb.setChecked(True)
        self.show_symbol_cb.setChecked(False)

    def on_plot_selected(self, index):
        self.selected_index = index
        update_controls_from_plot(self)

    def change_color(self):
        from PyQt5.QtWidgets import QColorDialog
        if self.selected_index < 0 or self.selected_index >= len(self.plots):
            return
        color = QColorDialog.getColor(self.plot_colors[self.selected_index], self, "Scegli colore")
        if color.isValid():
            self.plot_colors[self.selected_index] = color
            apply_plot_style(self, self.selected_index)

    def on_toggle_line(self):
        toggle_line_visibility(self)

    def on_toggle_symbol(self):
        toggle_symbol_visibility(self)
