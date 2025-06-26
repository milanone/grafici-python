import pyqtgraph as pg
from PyQt5.QtGui import QColor
from utils import is_color_dark

def create_plot(plot_widget, x, y, color, name):
    pen = pg.mkPen(color=color, width=2)
    return plot_widget.plot(x, y, pen=pen, symbol=None, symbolBrush=None, name=name)

def apply_plot_style(ui, index):
    line = ui.plots[index]
    show_line = ui.show_line_cb.isChecked() if index == ui.selected_index else True
    show_symbol = ui.show_symbol_cb.isChecked() if index == ui.selected_index else False

    color = ui.plot_colors[index]
    pen = pg.mkPen(color=color if show_line else QColor(0,0,0,0), width=2 if show_line else 0)
    line.setPen(pen)
    line.setSymbol('o' if show_symbol else None)
    if show_symbol:
        line.setSymbolBrush(color)
    ui.plot_widget.repaint()

def toggle_line_visibility(ui):
    if 0 <= ui.selected_index < len(ui.plots):
        apply_plot_style(ui, ui.selected_index)

def toggle_symbol_visibility(ui):
    if 0 <= ui.selected_index < len(ui.plots):
        apply_plot_style(ui, ui.selected_index)

def update_controls_from_plot(ui):
    idx = ui.selected_index
    if 0 <= idx < len(ui.plots):
        line = ui.plots[idx]
        pen = line.opts.get('pen')
        color = pen.color() if pen else QColor('k')
        ui.plot_colors[idx] = color
        ui.color_btn.setStyleSheet(
            f"background-color: {color.name()}; color: {'white' if is_color_dark(color) else 'black'}"
        )
        ui.show_line_cb.blockSignals(True)
        ui.show_symbol_cb.blockSignals(True)
        ui.show_line_cb.setChecked(line.opts.get('pen') is not None and line.opts['pen'].width() > 0)
        ui.show_symbol_cb.setChecked(line.opts.get('symbol') is not None)
        ui.show_line_cb.blockSignals(False)
        ui.show_symbol_cb.blockSignals(False)
    else:
        ui.color_btn.setStyleSheet("")
        ui.show_line_cb.setChecked(True)
        ui.show_symbol_cb.setChecked(False)
