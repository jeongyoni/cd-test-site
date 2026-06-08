def send_to_teams(day, menu):
    payload = {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "type": "AdaptiveCard",
                    "version": "1.4",
                    "body": [
                        {
                            "type": "TextBlock",
                            "size": "Large",
                            "weight": "Bolder",
                            "text": f"🍱 오늘의 점심 메뉴 ({day})"
                        },
                        {
                            "type": "TextBlock",
                            "wrap": True,
                            "text": menu
                        }
                    ]
                }
            }
        ]
    }

    requests.post(
        TEAMS_WEBHOOK_URL,
        json=payload,
        timeout=10
    ).raise_for_status()