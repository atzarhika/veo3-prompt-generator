import streamlit as st
from googletrans import Translator

# Kamus emosi
emotion_dict = {
    "senang": "happy",
    "sedih": "sad",
    "marah": "angry",
    "malu": "shy",
    "kaget": "surprised",
    "senyum": "smiling",
    "kecewa": "disappointed",
    "gugup": "nervous",
    "bingung": "confused",
    "tertawa": "laughing",
    "serius": "serious"
}
emotion_options = list(emotion_dict.keys())

translator = Translator()
st.set_page_config(page_title="🎬 Veo 3 Prompt Generator", layout="centered")
st.title("🎬 Veo 3 Prompt Generator")
st.markdown("✨ Buat prompt video sinematik otomatis untuk Veo 3 (Google AI Video Generator)")

# === Deskripsi Skenario
st.header("📍 Deskripsi Skenario")
col1, col2 = st.columns(2)
with col1:
    scene_location = st.text_input("📌 Lokasi Adegan", "pasar malam")
with col2:
    time_of_day = st.selectbox("🕒 Waktu", ["Siang", "Sore", "Malam", "Dini Hari"])

style = st.selectbox("🎨 Gaya Visual", ["Realistik", "Cinematic", "Kartun", "Anime", "Surreal"])
scene_description = st.text_area("📖 Cerita Singkat / Sinopsis", "Seseorang bertemu orang dari masa lalunya di tengah keramaian.")

# === Karakter
st.header("🧍 Karakter")
char_count = st.slider("Jumlah Karakter", 1, 5, 2)
character_profiles = []

for i in range(char_count):
    with st.expander(f"Character {i+1}"):
        gender = st.selectbox(f"Jenis Kelamin", ["Pria", "Wanita", "Tidak Diketahui"], key=f"g_{i}")
        age = st.text_input("Usia", "30", key=f"a_{i}")
        clothing = st.text_input("Pakaian", "jaket dan celana panjang", key=f"c_{i}")
        posture = st.text_input("Postur / Bahasa Tubuh", "gelisah dan penuh harap", key=f"p_{i}")
        character_profiles.append(
            f"Character {i+1} is a {gender.lower()} around {age} years old, wearing {clothing}, moving with a {posture} posture."
        )

# === Dialog
st.header("💬 Dialog Karakter")
use_dialog = st.checkbox("Aktifkan Dialog?")
dialog_data = []
accent = st.text_input("Aksen Dialog (contoh: Jawa halus, Betawi, Sunda)")

if use_dialog:
    dialog_lines = st.number_input("Jumlah Baris Dialog", min_value=1, max_value=10, value=2)
    for i in range(dialog_lines):
        col1, col2, col3 = st.columns([1.5, 3, 2])
        with col1:
            speaker = st.selectbox(f"🧍 Karakter (Dialog {i+1})", [f"Character {j+1}" for j in range(char_count)], key=f"dsp_{i}")
        with col2:
            line = st.text_input(f"💬 Kalimat Dialog {i+1}", key=f"dln_{i}")
        with col3:
            emotion = st.selectbox(f"😐 Ekspresi", emotion_options, key=f"emo_{i}")
        dialog_data.append((speaker, line, emotion))

subtitle = st.radio("📝 Tampilkan Subtitle?", ["Ya", "Tidak"], horizontal=True)

# === Audio
st.header("🔊 Audio & Musik")
ambience = st.multiselect("Suasana Latar", ["Sunyi", "Ramai", "Hujan", "Angin", "Suasana pasar"])
effects = st.text_input("Efek Suara Tambahan", "langkah kaki, suara teriakan")
music = st.text_input("Musik Latar", "musik tradisional pelan")

# === Kamera
st.header("🎥 Kamera")
motion = st.selectbox("Gerakan Kamera", ["Static", "Pan", "Tracking", "Zoom", "Crane", "Handheld"])
angle = st.text_input("Sudut Kamera", "low angle looking up at the crowd")

# === Generate Prompt
if st.button("🚀 Generate Prompt"):

    prompt_base = f"Create an 8-second {style.lower()} scene set in {scene_location} during the {time_of_day.lower()}.\n"

    if scene_description:
        prompt_base += f"Story: {scene_description.strip()}\n"

    prompt_base += f"Characters: {char_count}. "
    prompt_base += " ".join(character_profiles) + "\n"

    if use_dialog:
        prompt_base += f"The scene includes dialogue with {accent or 'natural'} accent. "
        prompt_base += f"Subtitles {'ON' if subtitle == 'Ya' else 'OFF'}.\n"

    if ambience:
        prompt_base += f"Ambience: {', '.join(ambience)}.\n"
    if effects:
        prompt_base += f"Sound effects: {effects.strip()}.\n"
    if music:
        prompt_base += f"Background music: {music.strip()}.\n"
    if motion or angle:
        prompt_base += f"Camera movement: {motion}, Angle: {angle.strip()}.\n"

    # Terjemahkan prompt base (non-dialog)
    try:
        translated_base = translator.translate(prompt_base, dest='en').text
    except Exception as e:
        translated_base = f"[Translation error]: {e}"

    # Tambahkan dialog asli dengan ekspresi terjemahan
    dialog_section = ""
    if use_dialog and dialog_data:
        dialog_section += "\nDialog lines (do NOT translate):\n"
        for speaker, line, emotion in dialog_data:
            eng_emotion = emotion_dict.get(emotion.lower(), emotion)
            dialog_section += f"{speaker} ({eng_emotion}): \"{line}\"\n"

    final_prompt = translated_base.strip() + "\n" + dialog_section.strip()

    # Tampilkan hasil
    st.subheader("🎯 Prompt Final untuk Veo (EN)")
    st.code(final_prompt, language="markdown")

    st.subheader("📝 Prompt Asli (Campuran ID + EN)")
    st.code(prompt_base + dialog_section, language="markdown")
