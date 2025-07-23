import uiautomation as auto
import time 
import os, sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog
from PySide6.QtCore import (
    QThread,
    Signal,
    Qt,
    QFile,
    QIODevice,
)
from PySide6.QtGui import QImage, QPixmap, QClipboard
import pyperclip
from datetime import datetime, time as dt
import holidays

# 한국 공휴일 설정
kr_holidays = holidays.KR()

def is_operating_now(now = None):
    if now is None:
        now = datetime.now()

    # 날짜가 공휴일이면 False 반환
    if now.date() in kr_holidays:
        return False

    weekday = now.weekday()  # 월요일=0, 토요일=5, 일요일=6
    current_time = now.time()

    # 공통 시작 시간: 07:30
    start_time = dt(7, 30)

    if weekday < 5:  # 월~금
        end_time = dt(20, 00)  # 평일은 20:00까지
    elif weekday == 5:  # 토요일은 14:00까지
        end_time = dt(14, 0)
    else:  # 일요일
        return False

    return start_time <= current_time <= end_time

class WorkerThread(QThread):
    thread_signal = Signal(int)

    def __init__(self, index, interval):
        super().__init__()
        self.index = index
        self.interval = interval
    
    def run(self):
        while True:
            if is_operating_now():
                print("✅ 운영 중입니다.")
                self.thread_signal.emit(self.index)
            else:
                print("⛔ 지금은 운영 시간이 아닙니다.")

            # time.sleep(self.interval * 60 * 60)
            time.sleep(60)
        

class MainWindow:
    def __init__(self, window):
        self.window = window

        self.textEdit = [self.window.msg0, self.window.msg1, self.window.msg2, self.window.msg3, 
                         self.window.rpt_msg0, self.window.msg4, self.window.msg5, self.window.rpt_msg1,]
        
        self.rptTime = [None, None, None, None, self.window.rptTime0, None, None, self.window.rptTime1,]
        self.worker = [None, None, None, None, None, None, None, None,]

        self.rptSendBtn = [None, None, None, None, self.window.btnRptSendMsg0, None, None, self.window.btnRptSendMsg1,]
        self.rptStopBtn = [None, None, None, None, self.window.btnRptStopMsg0, None, None, self.window.btnRptStopMsg1,]

        self.window.btnSendMsg0.clicked.connect(lambda:self.btnSendMsg_click(0))
        self.window.btnSaveMsg0.clicked.connect(lambda:self.btnSaveMsg_click(0))

        self.window.btnSendMsg1.clicked.connect(lambda:self.btnSendMsg_click(1))
        self.window.btnSaveMsg1.clicked.connect(lambda:self.btnSaveMsg_click(1))

        self.window.btnSendMsg2.clicked.connect(lambda:self.btnSendMsg_click(2))
        self.window.btnSaveMsg2.clicked.connect(lambda:self.btnSaveMsg_click(2))

        self.window.btnSendMsg3.clicked.connect(lambda:self.btnSendMsg_click(3))
        self.window.btnSaveMsg3.clicked.connect(lambda:self.btnSaveMsg_click(3))

        self.window.btnSendRptMsg0.clicked.connect(lambda:self.btnSendMsg_click(4))
        self.window.btnSaveRptMsg0.clicked.connect(lambda:self.btnSaveMsg_click(4))

        self.window.btnRptSendMsg0.clicked.connect(lambda:self.btnRptSendMsg_click(4))
        self.window.btnRptStopMsg0.clicked.connect(lambda:self.btnRptStopMsg_click(4))

        self.window.btnSendMsg4.clicked.connect(lambda:self.btnSendMsg_click(5))
        self.window.btnSaveMsg4.clicked.connect(lambda:self.btnSaveMsg_click(5))

        self.window.btnSendMsg5.clicked.connect(lambda:self.btnSendMsg_click(6))
        self.window.btnSaveMsg5.clicked.connect(lambda:self.btnSaveMsg_click(6))


        self.window.btnSendRptMsg1.clicked.connect(lambda:self.btnSendMsg_click(7))
        self.window.btnSaveRptMsg1.clicked.connect(lambda:self.btnSaveMsg_click(7))

        self.window.btnRptSendMsg1.clicked.connect(lambda:self.btnRptSendMsg_click(7))
        self.window.btnRptStopMsg1.clicked.connect(lambda:self.btnRptStopMsg_click(7))
        
        self.window.btnSaveChatTitle.clicked.connect(self.btnSaveChatTitle_click)

        self.window.btnSendImg.clicked.connect(lambda:self.btnSendImg("change_profile.jpg"))
        self.window.btnSendImg_2.clicked.connect(lambda:self.btnSendImg("turnoff_alarm.jpg"))

    def show(self):
        self.window.show()
        
        for index, _ in enumerate(self.textEdit):
            self.loadMsg(index)
        
        self.loadChatTitle()

    def find_window(self):
        # 전체 윈도우 검색 (깊이 1까지만)
        windows = auto.GetRootControl().GetChildren()

        target_window = None
        for win in windows:
            title = self.window.chatTitle.toPlainText()
            if title in win.Name:
                target_window = win
                break
        return target_window

    def btnSendMsg_click(self, index):
        if index < len(self.textEdit):
            textEdit = self.textEdit[index]
            msg = textEdit.toPlainText()
            if msg:
                target_window = self.find_window()
                if target_window:
                    print("✅ 채팅창 찾음:", target_window.Name)

                    input_box = target_window.DocumentControl()
                    if input_box.Exists():
                        input_box.SetFocus()
                        time.sleep(0.1)

                        # 1. 클립보드에 복사
                        pyperclip.copy(msg)
                        time.sleep(0.1)

                        # 3. Ctrl+V 붙여넣기
                        input_box.SendKeys('{Ctrl}v') 
                        time.sleep(0.1)

                        input_box.SendKeys('{Enter}')
                        print("✅ 메시지 전송 완료")
                    else:
                        print("❌ 입력창을 찾지 못했습니다.")
                else:
                    print("❌ 창을 찾지 못했습니다.")
            else:
                print("❌ 전송할 메시지가 없습니다.")
                target_window = self.find_window()
                if target_window:
                    print("✅ 채팅창 찾음:", target_window.Name)
                else:
                    print("❌ 창을 찾지 못했습니다.")


    def btnSaveMsg_click(self, index):
        if index < len(self.textEdit):
            textEdit = self.textEdit[index]

            dir_path = os.path.dirname(os.path.realpath(__file__))
            msg_file_name = os.path.join(dir_path, f"kakao_msg{index}.txt")

            with open(msg_file_name, "w", encoding='utf-8') as f:
                f.write(textEdit.toPlainText())
                f.close()
     
    def btnRptSendMsg_click(self, index):
        if index < len(self.textEdit):
            print(index, self.rptTime[index].currentIndex())
            self.worker[index] = WorkerThread(index, self.rptTime[index].currentIndex() + 1)
            self.worker[index].daemon = True
            self.worker[index].thread_signal.connect(self.btnSendMsg_click)

            if not self.worker[index].isRunning():
                self.rptSendBtn[index].setEnabled(False)
                self.rptStopBtn[index].setEnabled(True)

                self.worker[index].start()

    def btnRptStopMsg_click(self, index):
        if index < len(self.textEdit):
            if self.worker[index] and self.worker[index].isRunning():
                self.worker[index].terminate()
                self.worker[index].wait()

                self.rptSendBtn[index].setEnabled(True)
                self.rptStopBtn[index].setEnabled(False)
                print("✅ 반복 메시지 전송 중지")
            else:
                print("❌ 반복 메시지 전송이 실행 중이 아닙니다.")

    def btnSaveChatTitle_click(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        title_file_name = os.path.join(dir_path, "kakao_title.txt")

        with open(title_file_name, "w", encoding='utf-8') as f:
            f.write(self.window.chatTitle.toPlainText())
            f.close()
        print("✅ 채팅 제목 저장 완료")

    def btnSendImg(self, filename=None):
        target_window = self.find_window()
        if target_window:
            print("✅ 채팅창 찾음:", target_window.Name)

            input_box = target_window.DocumentControl()
            if input_box.Exists():
                input_box.SetFocus()
                time.sleep(1)

                dir_path = os.path.dirname(os.path.realpath(__file__))


                # 이미지 파일 선택
                img_path = os.path.join(dir_path, filename)

                if img_path:
                    # 1. 클립보드에 이미지 복사
                    # (여기서 이미지를 클립보드에 복사하는 코드 필요)
                    # 예: QImage/QPixmap 사용 등
                    image = QImage(img_path)

                    if not image.isNull():
                        pixmap = QPixmap.fromImage(image)
                        clipboard = QApplication.clipboard()
                        clipboard.setPixmap(pixmap, QClipboard.Clipboard)
                        time.sleep(0.1)

                        # 2. Ctrl+V 붙여넣기
                        input_box.SendKeys('{Ctrl}v') 
                        time.sleep(0.1)

                        target_window.SendKeys('{Enter}')
                        print("✅ 이미지 전송 완료")
                    else:
                        print("❌ 이미지 파일을 불러올 수 없습니다.")
                else:
                    print("❌ 이미지 파일을 선택하지 않았습니다.")
            else:
                print("❌ 입력창을 찾지 못했습니다.")
        else:
            print("❌ 창을 찾지 못했습니다.")

    def loadMsg(self, index):
        if index < len(self.textEdit):
            textEdit = self.textEdit[index]

            dir_path = os.path.dirname(os.path.realpath(__file__))
            msg_file_name = os.path.join(dir_path, f"kakao_msg{index}.txt")

            try:
                with open(msg_file_name, "r", encoding='utf-8') as f:
                    textEdit.setText(f.read())
            except FileNotFoundError:
                print("❌ 메시지 파일이 없습니다.")

    def loadChatTitle(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        title_file_name = os.path.join(dir_path, "kakao_title.txt")

        try:
            with open(title_file_name, "r", encoding='utf-8') as f:
                self.window.chatTitle.setText(f.read())
        except FileNotFoundError:
            print("❌ 채팅 제목 파일이 없습니다.")
            self.window.chatTitle.setText("확인용")

if __name__ == "__main__":
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ui_file_name = os.path.join(dir_path, "kakao_ui.ui")
    ui_file = QFile(ui_file_name)

    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)

    loader = QUiLoader()
    app = QApplication(sys.argv)

    window = loader.load(ui_file)

    ui_file.close()

    if not window:
        print(loader.errorString())
        sys.exit(-1)

    main_window = MainWindow(window)
    main_window.show()

    exec_id = app.exec()

    sys.exit(exec_id)