"""Telegram kanalına növbəti quiz sualını göndərir.
Sual 300, variant 100 simvoldan uzundursa: mətn ayrıca mesajla
göndərilir, quiz isə qısa formada (A, B, C...) onun altında gəlir."""
import json, os, urllib.request, urllib.parse

TOKEN = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHANNEL_ID"]
API = f"https://api.telegram.org/bot{TOKEN}/"
HERF = "ABCDEFGHIJ"


def call(method, data):
    req = urllib.request.Request(API + method, data=urllib.parse.urlencode(data).encode())
    resp = json.load(urllib.request.urlopen(req))
    if not resp.get("ok"):
        raise SystemExit(f"Xəta: {resp}")
    return resp


questions = json.load(open("questions.json", encoding="utf-8"))
state = json.load(open("state.json", encoding="utf-8"))
i = state["next"] % len(questions)
q = questions[i]
sual, variantlar = q["q"], q["o"]

if len(sual) > 300 or any(len(o) > 100 for o in variantlar):
    # Uzun sual: tam mətni ayrıca mesajla göndər
    metn = f"❓ Sual {i + 1}\n\n{sual}\n\n" + "\n".join(
        f"{HERF[k]}) {o}" for k, o in enumerate(variantlar))
    call("sendMessage", {"chat_id": CHAT, "text": metn})
    sual = "Yuxarıdakı sualın doğru cavabını seçin 👆"
    variantlar = list(HERF[:len(variantlar)])

data = {
    "chat_id": CHAT,
    "question": sual,
    "options": json.dumps(variantlar, ensure_ascii=False),
    "type": "quiz",
    "correct_option_id": q["a"],
}
if q.get("izah"):
    data["explanation"] = q["izah"][:200]
call("sendPoll", data)

print(f"Göndərildi: sual {i + 1}/{len(questions)}")
state["next"] = (i + 1) % len(questions)
json.dump(state, open("state.json", "w", encoding="utf-8"))
