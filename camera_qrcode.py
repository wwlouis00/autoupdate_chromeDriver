import sys
import time
import cv2
import xlwt
import xlrd
from xlutils.copy import copy
from pyzbar import pyzbar
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLCDNumber, QWidget

class QRCodeFocusApp(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize attributes
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.frame_data = None
        self.qrcode_data = ""
        self.current_record_id = 1

        # Setup UI
        self.init_ui()
        self.init_slots()

    def init_ui(self):
        # Main layout
        main_layout = QHBoxLayout()
        button_layout = QVBoxLayout()

        # Widgets
        self.camera_label = QLabel()
        self.camera_label.setFixedSize(640, 480)
        
        self.label_status = QLabel('以下為灰階圖片方差')
        self.label_qrcode = QLabel('機台編號:')
        
        self.focus_value_display = QLCDNumber(5)
        
        self.btn_open_camera = QPushButton('Open CAMERA')
        self.btn_close = QPushButton('Quit')
        self.btn_check_focus = QPushButton('焦距檢測:')
        self.btn_open_db = QPushButton('開啟資料庫')
        self.btn_save_db = QPushButton('儲存到資料庫')
        self.btn_read_qrcode = QPushButton('讀取 QR Code')

        # Button styling
        buttons = [self.btn_open_camera, self.btn_close]
        for button in buttons:
            button.setStyleSheet(
                "QPushButton {color: black; background-color: rgb(78,255,255); border-radius: 10px; padding: 4px;}"
                "QPushButton:hover {color: red;}"
            )

        # Add buttons to layout
        button_layout.addWidget(self.label_qrcode)
        button_layout.addWidget(self.btn_open_camera)
        button_layout.addWidget(self.label_status)
        button_layout.addWidget(self.focus_value_display)
        button_layout.addWidget(self.btn_check_focus)
        button_layout.addWidget(self.btn_read_qrcode)
        button_layout.addWidget(self.btn_save_db)
        button_layout.addWidget(self.btn_open_db)
        button_layout.addWidget(self.btn_close)

        # Combine layouts
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.camera_label)
        self.setLayout(main_layout)

        # Window settings
        self.setWindowTitle('焦距檢測')

    def init_slots(self):
        self.btn_open_camera.clicked.connect(self.toggle_camera)
        self.timer_camera.timeout.connect(self.update_camera_view)
        self.btn_close.clicked.connect(self.close)
        self.btn_save_db.clicked.connect(self.save_to_database)
        self.btn_open_db.clicked.connect(self.open_database)
        self.btn_read_qrcode.clicked.connect(self.read_qrcode)

    def toggle_camera(self):
        if not self.timer_camera.isActive():
            if self.cap.open(self.CAM_NUM):
                self.timer_camera.start(30)
                self.btn_open_camera.setText('關閉相機')
            else:
                QMessageBox.warning(self, "Warning", "請檢測相機與電腦是否連線正確")
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.camera_label.clear()
            self.btn_open_camera.setText('開啟相機')

    def update_camera_view(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        self.frame_data = frame
        frame_resized = cv2.resize(frame, (640, 480))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        gray_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_BGR2GRAY)

        # Calculate focus measure
        focus_measure = int(cv2.Laplacian(gray_frame, cv2.CV_64F).var())
        self.focus_value_display.display(focus_measure)

        if focus_measure > 100:
            self.btn_check_focus.setText('焦距檢測: 對焦成功')
            self.btn_check_focus.setStyleSheet("QPushButton {color: green;}")
        else:
            self.btn_check_focus.setText('焦距檢測: 對焦失敗')
            self.btn_check_focus.setStyleSheet("QPushButton {color: red;}")

        # Update camera view
        image = QtGui.QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], frame_rgb.strides[0], QtGui.QImage.Format.Format_RGB888)
        self.camera_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def read_qrcode(self):
        if self.frame_data is not None:
            decoded_objects = pyzbar.decode(self.frame_data)
            if decoded_objects:
                self.qrcode_data = decoded_objects[0].data.decode('utf-8')
                self.label_qrcode.setText(f'機台編號: {self.qrcode_data}')

    def save_to_database(self):
        if self.frame_data is None:
            QMessageBox.warning(self, "Warning", "尚未捕捉到影像資料！")
            return

        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        file_name = f"{time.strftime('%Y-%m-%d', time.localtime())}.xls"
        image_name = f"{current_time.replace(':', '-')}.png"

        cv2.imwrite(image_name, self.frame_data)

        focus_result = 'Pass' if self.focus_value_display.value() > 100 else 'Fail'
        data = [
            self.current_record_id,
            current_time,
            self.qrcode_data,
            self.focus_value_display.value(),
            focus_result,
            image_name
        ]

        try:
            # 嘗試打開 Excel 檔案
            workbook = xlrd.open_workbook(file_name, formatting_info=True)
            writable_workbook = copy(workbook)
            sheet = writable_workbook.get_sheet(0)
        except FileNotFoundError:
            # 若檔案不存在，則創建新檔案
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('Data', cell_overwrite_ok=True)
            headers = ['ID', '日期', '機台編號', '灰階圖偏方差值', '對焦結果', '存檔名稱']
            for col, header in enumerate(headers):
                sheet.write(0, col, header)
            writable_workbook = workbook  # 這裡直接用 workbook，確保變數存在
            self.current_record_id = 1  # 新建 Excel 時，從 ID=1 開始

        # 寫入數據
        for col, value in enumerate(data):
            sheet.write(self.current_record_id, col, value)

        # 保存 Excel 文件
        writable_workbook.save(file_name)
        self.current_record_id += 1


    def open_database(self):
        file_name = 'OUTPUT.xls'
        try:
            workbook = xlrd.open_workbook(file_name)
            sheet = workbook.sheet_by_index(0)
            for row in range(sheet.nrows):
                print(sheet.row_values(row))
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "資料庫檔案不存在！")

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        if self.timer_camera.isActive():
            self.timer_camera.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QRCodeFocusApp()
    window.show()
    sys.exit(app.exec())
