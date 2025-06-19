import uiautomation as auto
import pyautogui
import time
import pytesseract
from PIL import ImageGrab

# Tesseract 실행 파일 경로 지정
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# 전체 윈도우 검색 (깊이 1까지만)
windows = auto.GetRootControl().GetChildren()

target_window = None
for win in windows:
    if '우리동네 국민상회 산곡점' in win.Name:
        target_window = win
        break

if target_window:
    print("✅ 채팅창 찾음:", target_window.Name)

    
    left, top, right, bottom = 0, 0, 0, 0

    # 하위 컨트롤 순회하며 위치 확인
    for ctrl in target_window.GetChildren():
        print(ctrl.Name, ctrl.ControlType, ctrl.BoundingRectangle)
        if ctrl.ControlType == 50033:
            # 메시지 영역 좌표 (스크린 기준 좌표로 수정해야 함)
            print(ctrl.BoundingRectangle)
            left, top, right, bottom = ctrl.BoundingRectangle.left, ctrl.BoundingRectangle.top, ctrl.BoundingRectangle.right, ctrl.BoundingRectangle.bottom
            break
    
    prev_text = ''
   
    while True:
        img = ImageGrab.grab(bbox=(left, top, right, bottom))
        text = pytesseract.image_to_string(img, lang='kor+eng')

        print("==================")
        print(text)
        print("==================")

        if text != prev_text:
            print("🔔 새로운 메시지 감지:")
            print(text)
            prev_text = text
            # TODO: 자동 응답 전송 로직

        time.sleep(0.01)