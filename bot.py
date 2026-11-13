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
i = state.get("next", 0) % len(questions)
q = questions[i]
sual, variantlar = q["q"], q["o"]
if q.get("m") and len(sual) + len(q["m"]) + 4 <= 300:
    sual = f"📚 {q['m']}\n{sual}"

if len(sual) > 300 or any(len(o) > 100 for o in variantlar):
    metn = f"❓ Sual\n\n{sual}\n\n" + "\n".join(
        f"{HERF[k]}) {o}" for k, o in enumerate(variantlar))
    call("sendMessage", {"chat_id": CHAT, "text": metn})
    sual = "Yuxarıdakı sualın doğru cavabını seçin 👆"
    variantlar = list(HERF[:len(variantlar)])

call("sendPoll", {
    "chat_id": CHAT,
    "question": sual,
    "options": json.dumps(variantlar, ensure_ascii=False),
    "type": "quiz",
    "correct_option_id": q["a"],
})

print(f"Göndərildi: sual {i + 1}/{len(questions)}")
state["next"] = (i + 1) % len(questions)
json.dump(state, open("state.json", "w", encoding="utf-8"))
