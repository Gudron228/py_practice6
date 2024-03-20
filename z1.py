
import sys
from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListView


class Note:
    def __init__(self, text):
        self.text = text
        self.id = id(self)


class NoteListModel(QAbstractListModel):
    def __init__(self, notes=None):
        super().__init__()
        self.notes = notes or []

    def rowCount(self, parent=QModelIndex()):
        return len(self.notes)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.notes[index.row()].text
        return None

    def add_note(self, text):
        if text.strip():
            self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
            self.notes.append(Note(text))
            self.endInsertRows()

    def remove_note_by_id(self, note_id):
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                self.beginRemoveRows(QModelIndex(), i, i)
                del self.notes[i]
                self.endRemoveRows()
                break


class NoteWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Заметки")
        layout = QVBoxLayout()

        self.note_model = NoteListModel()

        self.note_input = QLineEdit()
        layout.addWidget(self.note_input)

        add_button = QPushButton("Добавить заметку")
        add_button.clicked.connect(self.add_note)
        layout.addWidget(add_button)

        self.notes_list = QListView()
        self.notes_list.setModel(self.note_model)
        layout.addWidget(self.notes_list)

        self.setLayout(layout)

    def add_note(self):
        text = self.note_input.text()
        self.note_model.add_note(text)
        self.note_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoteWindow()
    window.show()
    sys.exit(app.exec())
