import sys
import os
import psutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer

class RamCleaner(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RAM Cleaner")
        self.setGeometry(100, 100, 800, 600)  # O'lchamni kattalashtirdik
        self.setStyleSheet("""
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        """)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("RAM Tozalovchi Dastur", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        layout.addWidget(self.label)

        self.ram_info = QLabel("", self)
        self.ram_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.ram_info)

        # Using QTableWidget instead of QListWidget
        self.process_table = QTableWidget(self)
        self.process_table.setColumnCount(4)  # 4 columns for Name, PID, User, Memory
        self.process_table.setHorizontalHeaderLabels(["Name", "PID", "User", "Memory (MB)"])
        self.process_table.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                border: 1px solid #ccc;
                border-radius: 5px;
                font-size: 14px;
                padding: 10px;
                gridline-color: #ccc;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #f2f2f2;
                font-weight: bold;
                padding: 10px;
            }
            QTableWidget::item:hover {
                background-color: #e0e0e0;  /* Hover color for table items */
            }
        """)
        self.process_table.horizontalHeader().setStretchLastSection(True)
        self.process_table.horizontalHeader().setSectionResizeMode(0, 1)
        self.process_table.horizontalHeader().setSectionResizeMode(1, 0)
        self.process_table.horizontalHeader().setSectionResizeMode(2, 0)
        self.process_table.horizontalHeader().setSectionResizeMode(3, 0)

        layout.addWidget(self.process_table)

        self.stat_label = QLabel("", self)
        self.stat_label.setAlignment(Qt.AlignCenter)
        self.stat_label.setStyleSheet("font-size: 14px; color: #555;")
        layout.addWidget(self.stat_label)

        button_layout = QHBoxLayout()
        
        # RAMni Tozalash tugmasi
        self.clean_button = QPushButton("RAMni Tozalash", self)
        self.clean_button.setStyleSheet("""
            font-size: 16px; padding: 10px; 
            background-color: #4CAF50; color: white; 
            border: none; border-radius: 5px; 
            transition: background-color 0.3s, transform 0.3s; 
        """)
        self.clean_button.setStyleSheet(self.clean_button.styleSheet() + """
            QPushButton:hover {
                background-color: #45a049; /* Hover color for clean button */
                transform: scale(1.05);
            }
        """)
        self.clean_button.clicked.connect(self.clear_ram)
        button_layout.addWidget(self.clean_button)

        # Ro'yxatni Yangilash tugmasi
        self.refresh_button = QPushButton("Ro'yxatni Yangilash", self)
        self.refresh_button.setStyleSheet("""
            font-size: 16px; padding: 10px; 
            background-color: #2196F3; color: white; 
            border: none; border-radius: 5px; 
            transition: background-color 0.3s, transform 0.3s; 
        """)
        self.refresh_button.setStyleSheet(self.refresh_button.styleSheet() + """
            QPushButton:hover {
                background-color: #1e88e5; /* Hover color for refresh button */
                transform: scale(1.05);
            }
        """)
        self.refresh_button.clicked.connect(self.update_process_list)
        button_layout.addWidget(self.refresh_button)

        # Jarayonni O'chirish tugmasi
        self.kill_button = QPushButton("Jarayonni O'chirish", self)
        self.kill_button.setStyleSheet("""
            font-size: 16px; padding: 10px; 
            background-color: #F44336; color: white; 
            border: none; border-radius: 5px; 
            transition: background-color 0.3s, transform 0.3s; 
        """)
        self.kill_button.setStyleSheet(self.kill_button.styleSheet() + """
            QPushButton:hover {
                background-color: #e53935; /* Hover color for kill button */
                transform: scale(1.05);
            }
        """)
        self.kill_button.clicked.connect(self.kill_selected_process)
        button_layout.addWidget(self.kill_button)

        layout.addLayout(button_layout)

        # Avtomatik RAM tozalash uchun checkbox
        self.auto_clean_checkbox = QCheckBox("Avtomatik RAM Tozalash", self)
        self.auto_clean_checkbox.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.auto_clean_checkbox)

        self.footer_label = QLabel("Created by Inforte.uz", self)
        self.footer_label.setAlignment(Qt.AlignCenter)
        self.footer_label.setStyleSheet("font-size: 12px; color: gray;")
        layout.addWidget(self.footer_label)

        central_widget.setLayout(layout)

        self.loader_label = QLabel("Yuklanmoqda...", self)
        self.loader_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.loader_label)

        self.update_ram_info()
        self.update_process_list()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_ram_usage)  # Check RAM usage every 5 seconds
        self.timer.start(5000)

        self.loader_label.show()
        self.update_process_list()

    def clear_ram(self):
        try:
            os.system("sync; echo 3 | sudo tee /proc/sys/vm/drop_caches")
            self.update_ram_info()
            self.update_process_list()
            QMessageBox.information(self, "RAM Tozalandi", "RAM muvaffaqiyatli tozalandi.")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Xatolik yuz berdi: {str(e)}")

    def check_ram_usage(self):
        mem = psutil.virtual_memory()
        used_percentage = mem.percent

        # Avtomatik tozalash
        if self.auto_clean_checkbox.isChecked() and used_percentage >= 50:
            self.clear_ram()

    def update_ram_info(self):
        mem = psutil.virtual_memory()
        used_memory = mem.used / (1024 * 1024)
        available_memory = mem.available / (1024 * 1024)
        total_memory = mem.total / (1024 * 1024)

        self.ram_info.setText(f"Foydalanilgan RAM: {used_memory:.2f} MB\nBo'sh RAM: {available_memory:.2f} MB")
        free_percentage = (available_memory / total_memory) * 100
        used_percentage = (used_memory / total_memory) * 100
        self.stat_label.setText(f"Bo'sh RAM: {free_percentage:.2f}% | Foydalanilgan RAM: {used_percentage:.2f}%")

    def update_process_list(self):
        self.process_table.setRowCount(0) 
        processes = []

        for proc in psutil.process_iter(['name', 'memory_info']):
            try:
                mem = proc.info['memory_info'].rss / (1024 * 1024)
                processes.append((proc.info['name'], proc.pid, proc.username(), mem))  # Include username
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if processes:
            processes.sort(key=lambda x: x[3], reverse=True)

            # Add processes to the table
            for name, pid, username, memory in processes:
                row_position = self.process_table.rowCount()
                self.process_table.insertRow(row_position)

                # Highlight memory usage
                item_color = Qt.black if memory < 50 else Qt.red  # Change 50 to your desired threshold
                self.process_table.setItem(row_position, 0, QTableWidgetItem(name))
                self.process_table.setItem(row_position, 1, QTableWidgetItem(str(pid)))
                self.process_table.setItem(row_position, 2, QTableWidgetItem(username))
                
                memory_item = QTableWidgetItem(f"{memory:.2f}")
                memory_item.setForeground(item_color)  # Set color for memory item
                self.process_table.setItem(row_position, 3, memory_item)

        self.loader_label.hide()

    def kill_selected_process(self):
        selected_item = self.process_table.currentRow()
        if selected_item >= 0:
            pid = int(self.process_table.item(selected_item, 1).text())
            # Tasdiqlash dialogi
            process_name = self.process_table.item(selected_item, 0).text()
            if process_name in ["chrome.exe", "firefox.exe", "Code.exe"]:  # Use the actual process names
                reply = QMessageBox.question(self, "Tasdiqlash", f"{process_name} jarayonini o'chirmoqchimisiz?", 
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.No:
                    return
            self.kill_process(pid)
        else:
            QMessageBox.warning(self, "Ogohlantirish", "Iltimos, o'chirish uchun jarayonni tanlang.")

    def kill_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
            self.update_process_list()
            QMessageBox.information(self, "Jarayon O'chirildi", f"{p.name()} jarayoni muvaffaqiyatli o'chirildi.")
        except Exception as e:
            QMessageBox.critical(self, "Xatolik", f"Jarayonni o'chirishda xatolik yuz berdi: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RamCleaner()
    window.show()
    sys.exit(app.exec_())