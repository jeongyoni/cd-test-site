import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone

MENU_URL = "https://www.kopo.ac.kr/gm/content.do?menu=12623"
TEAMS_WEBHOOK_URL = os.environ["TEAMS_WEBHOOK_URL"]

KST = timezone(timedelta(hours=9))

DAY_MAP = {
    0: "월요일",
    1: "화요일",
    2: "수요일",
    3: "목요일",
    4: "금요일",
}

def get_today_menu():
    now = datetime.now(KST)
    weekday = now.weekday()

    if weekday not in DAY_MAP:
        return "주말", "오늘은 급식 운영일이 아닙니다."

    today_name = DAY_MAP[weekday]

    res = requests.get(MENU_URL, timeout=10)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    text = soup.get_text("\n", strip=True)

    pattern = rf"{today_name}\s+(.*?)(?=월요일|화요일|수요일|목요일|금요일|토요일|일요일|content_footer)"
    match = re.search(pattern, text, re.S)

    if not match:
        return today_name, "오늘 메뉴를 찾지 못했습니다."

    menu = match.group(1).strip()
    menu = re.sub(r"\s+", " ", menu)

    return today_name, menu

def send_to_teams(day, menu):
    message = {
        "text": f"""🍱 오늘의 점심 메뉴 ({day})

{menu}

출처: {MENU_URL}
"""
    }

    res = requests.post(TEAMS_WEBHOOK_URL, json=message, timeout=10)
    res.raise_for_status()

if __name__ == "__main__":
    day, menu = get_today_menu()
    send_to_teams(day, menu)
    print("Teams 전송 완료")