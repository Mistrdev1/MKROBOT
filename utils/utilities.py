# Text Editor Function
def text_editor(message: str):
    try:
        malumotlar = message.rsplit(" ")
        liss = malumotlar[2].rsplit("\n")
        text = f"💴 <i>Valyuta:</i> {malumotlar[0]}\n"
        text += f"💰 <i>Kripto:</i> {malumotlar[1]}\n"
        text += f"✅ <i>Sof foyda:</i> {malumotlar[2].replace(f'{liss[1]}', '')}"
        data = malumotlar[2].replace(f'{liss[0]}\n', '')
        text += f"🏦 <i>Hamyonlar:</i> {data} {malumotlar[3]} {malumotlar[4]} {malumotlar[5]} {malumotlar[6]}"
    except: pass
    return text