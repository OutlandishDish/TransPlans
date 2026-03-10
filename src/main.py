
                                        # TODO: Implement dynamic centering using screen().availableGeometry()
                                        # TODO: Add mousePressEvent/mouseMoveEvent for borderless dragging
                                        # TODO: Refactor day columns into 1-hour QLineEdit/QTextEdit blocks
                                        # TODO: Create a date-based naming convention for tasks.json for history
                                        # TODO: Explore PyInstaller for creating a standalone Windows executable
                                        # TODO: Increase day label and task font sizes



# import sys
# from PyQt6.QtWidgets import QApplication

# print(f"Python Version: {sys.version}")
# print("PyQt6 is successfully installed and ready!")


import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt

class AeroPlanner(QWidget):        # Creates a new class called AeroPlanner that inherits from QWidget (a basic window)
    def __init__(self):            # The constructor (init) method (Dunder) that initializes the AeroPlanner class
        super().__init__()         # Calls the constructor of the parent class (QWidget) to ensure proper initialization
        # print("Initializing Aero-Planner...")  # Debug print to indicate initialization has started
        # 1. THE "GHOST" SETTINGS
        # FramelessWindowHint removes the title bar and 'X' button
        # WindowStaysOnBottomHint keeps it on the desktop layer
        self.setWindowFlags(                                # Sets the window flags to customize the behavior and appearance of the window
            Qt.WindowType.FramelessWindowHint |             # Removes the title bar and borders, giving it a clean look
            Qt.WindowType.WindowStaysOnBottomHint           # Keeps the window on the desktop layer, allowing it to sit behind all other windows
        )
        
        # This makes the actual background of the window invisible
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # Allows the window to have a transparent background, so only the content (like our "card") will be visible

        # 2. THE DESIGN (Visuals)
        self.init_ui()                      # Calls the method to set up the user interface (UI) elements and design of the window

    # def init_ui(self):                      # This method sets up the user interface (UI) elements and design of the window
    #     # Create a layout to hold our content
    #     layout = QVBoxLayout()              # Creates a vertical box layout to arrange widgets vertically within the window

    #     # Create a "Card" look using CSS-style code (QSS)           
    #     # rgba(30, 30, 30, 180) is Dark Grey with 180/255 opacity
    #     self.container = QLabel("Getchya Rocks off Here")              # Creates a QLabel widget that will serve as the "card" to display the text "Aero-Planner Loaded"
    #     self.container.setStyleSheet("""
    #         background-color: rgba(30, 30, 30, 180);
    #         color: #FFFFFF;
    #         font-family: 'Segoe UI', sans-serif;
    #         font-size: 18px;
    #         padding: 20px;
    #         border-radius: 15px;
    #         border: 1px solid rgba(255, 255, 255, 30);
    #     """)
    #     self.container.setAlignment(Qt.AlignmentFlag.AlignCenter)

    #     layout.addWidget(self.container)
    #     self.setLayout(layout)

    #     # Set the starting size and position
    #     self.setGeometry(100, 100, 400, 150)
    #     self.show()


    def init_ui(self):
        # 1. Create the 'Main Tray' (Horizontal)
        main_layout = QHBoxLayout()                         # Creates a horizontal box layout to arrange widgets horizontally within the window, serving as the main container for our day columns
        
        # 2. Our list of days to loop through
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        # 3. An empty list to store our text boxes so 'self' can find them later
        self.task_widgets = []

        for day in days:
            # Create a 'Stack' for this specific day (Vertical)
            column = QVBoxLayout()
            
            # Create the Day Header
            day_label = QLabel(day)
            day_label.setStyleSheet("font-weight: bold; color: #000000;")
            day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            # Create the Text Entry box
            editor = QTextEdit()
            editor.setPlaceholderText("...")
            editor.setStyleSheet("background-color: rgba(255, 255, 255, 20); color: white; border-radius: 5px;")
            
            # IMPORTANT: Add the editor to our 'Memory Shelf' (the list)
            self.task_widgets.append(editor)
            
            # Put the Label and Editor into the Vertical Stack
            column.addWidget(day_label)
            column.addWidget(editor)
            
            # Finally, put the Stack into the Main Tray
            main_layout.addLayout(column)

            # 4. Tell the Window to use this 'Main Tray'
            self.setLayout(main_layout)
            
            # Set a wide size (Width: 1100, Height: 400)
            self.setGeometry(1370, 100, 1100, 400)
            self.show()

    def save_tasks(self):
        # We create a dictionary to map the day to the text
        data = {}
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        
        # We loop through our stored widgets and grab the text from each
        for i, widget in enumerate(self.task_widgets):                      # Loops through the list of task widgets (text editors) and their corresponding day index (i) using enumerate()
            data[days[i]] = widget.toPlainText()
        
        # This creates 'tasks.json' in your project folder
        with open("tasks.json", "w") as f:
            json.dump(data, f, indent=4)
        
        print("Flight plan saved to tasks.json!")       

    def closeEvent(self, event):
        self.save_tasks()  # Run the save logic
        event.accept()     # Allow the window to close 
    
           
    # The "Standard" Python Entry Point
if __name__ == "__main__":                    # This checks if the script is being run directly (as the main program) rather than imported as a module in another script. If this condition is true, the code inside this block will be executed.
    app = QApplication(sys.argv)             # Creates an instance of the QApplication class, which is necessary for any PyQt application. It takes command-line arguments (sys.argv) to allow for any command-line options that might be passed when running the script.   
    window = AeroPlanner()                    # Creates an instance of the AeroPlanner class, which initializes the window and its contents   
    sys.exit(app.exec())                     # Starts the application's event loop, allowing the GUI to be responsive and interactive. The sys.exit() ensures that the application exits cleanly when the event loop is terminated.





