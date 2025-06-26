from PyQt5.QtWidgets import QDialog, QVBoxLayout, QRadioButton, QDialogButtonBox, QButtonGroup

class SeparatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Scegli Separatore CSV")
        layout = QVBoxLayout(self)

        self.buttons = QButtonGroup(self)
        self.sep_options = {
            "Tabulazione (\\t)": "\t",
            "Punto e virgola (;)": ";",
            "Spazio": " ",
            "Virgola (,)": ","
        }

        for i, text in enumerate(self.sep_options):
            btn = QRadioButton(text)
            self.buttons.addButton(btn, i)
            layout.addWidget(btn)
            if text == "Virgola (,)":
                btn.setChecked(True)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)

    def get_separator(self):
        selected_id = self.buttons.checkedId()
        if selected_id < 0:
            return None
        key = list(self.sep_options.keys())[selected_id]
        return self.sep_options[key]
