import pyautogui
import time

print("5초 안에 캡처 영역의 좌상단을 클릭하세요.")
time.sleep(5)
x1, y1 = pyautogui.position()
print(f"좌상단 좌표: ({x1}, {y1})")

print("5초 안에 캡처 영역의 우하단을 클릭하세요.")
time.sleep(5)
x2, y2 = pyautogui.position()
print(f"우하단 좌표: ({x2}, {y2})")

# region = (x, y, width, height)
region = (x1, y1, x2 - x1, y2 - y1)
print(f"\n🟩 캡처 region = {region}")
