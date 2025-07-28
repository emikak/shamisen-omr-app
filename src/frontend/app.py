import streamlit as st
from PIL import Image

with st.sidebar:
    st.markdown("""## 音情報の事前入力""")
    st.selectbox(
        "楽譜の種類の指定",
        [
            "長唄",
            "地歌",
            "津軽",
        ],
    )

    st.number_input("周波数 [Hz]", value=442)
    st.number_input("テンポ [bpm]", value=80)
    scales = [
        ("1本", "A", "ラ"),
        ("2本", "A#", "ラ#"),
        ("3本", "B", "シ"),
        ("4本", "C", "ド"),
        ("5本", "C#", "ド#"),
        ("6本", "D", "レ"),
        ("7本", "D#", "レ#"),
        ("8本", "E", "ミ"),
        ("9本", "F", "ファ"),
        ("10本", "F#", "ファ#"),
        ("11本", "G", "ソ"),
        ("12本", "G#", "ソ#"),
    ]

    st.selectbox(
        "調弦(一の糸の開放弦)を選択",
        [f"{item[0]}  ,  {item[1]}  , {item[2]}" for item in scales],
    )

    st.selectbox(
        "調子の指定",
        [
            "本調子",
            "二上がり",
            "三下がり",
        ],
    )

    score = st.file_uploader(
        "楽譜の写真をアップロード",
    )

    if score:
        st.button(
            "楽譜の読み取り",
        )


# 音楽ファイルの指定
music_file = "./data/sakura_song.mp3"

if score:
    st.markdown("##### タイトル：さくらさくら")
    # 2分割レイアウト
    col1, col2 = st.columns(2)

    with col1:
        st.audio(music_file, format="audio/mpeg")

    # 画像をリサイズ
    img = Image.open(score)
    aspect_ratio = img.width / img.height
    new_height = 700  # ここで高さを指定
    new_width = int(new_height * aspect_ratio)
    resized_img = img.resize((new_width, new_height))

    st.image(resized_img)
