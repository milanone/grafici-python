import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from dialogs import SeparatorDialog

def load_csv_with_separator(file_path, parent):
    try:
        data = pd.read_csv(file_path, sep=',')
        if data.shape[1] < 2:
            raise ValueError("Poche colonne")
        return data
    except Exception:
        dlg = SeparatorDialog(parent)
        if dlg.exec_() == dlg.Accepted:
            sep = dlg.get_separator()
            if sep is None:
                QMessageBox.warning(parent, "Separatore", "Separatore non selezionato.")
                return None
            try:
                data = pd.read_csv(file_path, sep=sep)
                if data.shape[1] < 2:
                    QMessageBox.warning(parent, "Errore", "CSV con meno di due colonne")
                    return None
                return data
            except Exception as e:
                QMessageBox.critical(parent, "Errore", f"Errore lettura file:\n{e}")
                return None
        return None