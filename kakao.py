import uiautomation as auto
import time
import os, sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import (
    QThread,
    Signal,
    Qt,
    QFile,
    QIODevice,
)
import pyperclip

class WorkerThread(QThread):
    thread_signal = Signal(int)

    def __init__(self, index, interval):
        super().__init__()
        self.index = index
        self.interval = interval
    
    def run(self):
        while True:
            self.thread_signal.emit(self.index)
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
        

    def show(self):
        self.window.show()
        
        for index, _ in enumerate(self.textEdit):
            self.loadMsg(index)

    def find_window(self):
        # 전체 윈도우 검색 (깊이 1까지만)
        windows = auto.GetRootControl().GetChildren()

        target_window = None
        for win in windows:
            if '확인용' in win.Name:
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