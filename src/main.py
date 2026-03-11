import sys
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, 
                             QHBoxLayout, QTextEdit)
from PyQt6.QtCore import Qt, QPoint

class AeroPlanner(QWidget):
    def __init__(self):
        super().__init__()
        # 1. Window Setup (Translucent & Borderless)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.inputs = {}  # Dictionary to store our text boxes
        self.load_data()  # Load tasks and geometry from JSON
        self.init_ui()
        
        # 2. Style (Force Black Text)
        self.setStyleSheet("""
            QLabel { color: black; font-weight: bold; font-size: 14px; }
            QTextEdit { 
                color: black; 
                background-color: rgba(255, 255, 255, 180); 
                border: 1px solid #555; 
                border-radius: 5px;
            }
        """)

    def init_ui(self):
        # 1. Create the "Outer Container" (Vertical)
        outer_layout = QVBoxLayout()
        
        # 2. Create the Drag Handle (The Anchor)
        self.handle = QLabel("⠿ DRAG TO MOVE ⠿")
        self.handle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.handle.setStyleSheet("""
            background-color: rgba(255, 255, 255, 100); 
            color: black; 
            font-size: 10px; 
            padding: 2px;
            border-radius: 5px;
        """)
        outer_layout.addWidget(self.handle)

        # 3. Your current 7-day layout (Horizontal)
        main_layout = QHBoxLayout()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        
        for day in days:
            v_layout = QVBoxLayout()
            label = QLabel(day)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            text_edit = QTextEdit()
            text_edit.setPlainText(self.tasks.get(day, ""))
            self.inputs[day] = text_edit
            
            v_layout.addWidget(label)
            v_layout.addWidget(text_edit)
            main_layout.addLayout(v_layout)

        # 4. Nest the days inside the outer container
        outer_layout.addLayout(main_layout)
        
        # 5. Set the final layout to the window
        self.setLayout(outer_layout)
        self.resize(1000, 300)
        
        # Position the window
        if hasattr(self, 'saved_geometry'):
            self.move(self.saved_geometry['x'], self.saved_geometry['y'])
        else:
            # Center on your 3840x1200 screen by default
            qr = self.frameGeometry()
            cp = self.screen().availableGeometry().center()
            qr.moveCenter(cp)
            self.move(qr.topLeft())

    # --- Interaction (The Dragging Logic) ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.globalPosition().toPoint()
            diff = new_pos - self.drag_pos
            self.move(self.pos() + diff)
            self.drag_pos = new_pos

    # --- The Panic Button ---
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    # --- Data Handling (Saving & Loading) ---
    def load_data(self):
        try:
            with open('tasks.json', 'r') as f:
                data = json.load(f)
                self.tasks = data.get("tasks", {})
                self.saved_geometry = data.get("geometry", {"x": 100, "y": 100})
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = {}
            # No saved geometry yet

    def save_data(self):
        # Harvest text from the boxes
        current_tasks = {day: box.toPlainText() for day, box in self.inputs.items()}
        
        data_to_save = {
            "geometry": {"x": self.x(), "y": self.y()},
            "tasks": current_tasks
        }
        
        with open('tasks.json', 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def closeEvent(self, event):
        self.save_data()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AeroPlanner()
    window.show()
    sys.exit(app.exec())