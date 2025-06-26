import os
import subprocess
import pandas as pd
from PyQt5.QtWidgets import QMessageBox

CONVERTER_PATH = r"C:\Program Files (x86)\PerkinElmerSP2CSV\PerkinElmerSP2CSV.exe"

def try_load_sp_file(file_path, parent):
    try:
        subprocess.run([CONVERTER_PATH, file_path], check=True)
        csv_path = file_path + ".csv"
        df = pd.read_csv(csv_path)
        if df.shape[1] < 2:
            raise ValueError("CSV convertito con meno di due colonne")
        x, y = df.iloc[:, 0], df.iloc[:, 1]
        ask_delete_temp_csv(csv_path, parent)
        return x, y, True  # True = inverti asse X
    except Exception as e:
        QMessageBox.critical(parent, "Errore .sp", str(e))
        return None

def ask_delete_temp_csv(csv_path, parent):
    reply = QMessageBox.question(parent, "CSV temporaneo creato",
                                 f"Il file temporaneo {os.path.basename(csv_path)} è stato creato. Vuoi eliminarlo?",
                                 QMessageBox.Yes | QMessageBox.No)
    if reply == QMessageBox.Yes:
        try:
            os.remove(csv_path)
        except Exception:
            pass
