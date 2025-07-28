import streamlit as st
from PIL import Image

# 画像のパスとタイトルのリスト
images = [
    {
        "title": f"楽譜{i+1}",
        "path": f"C:\\Users\\kmgkx\\Documents\\wagakki\\src\\data\\IMG_{i:04d}.jpg",
    }
    for i in range(12)
]

# 3列×4行のグリッドを作成
cols = st.columns(3)
for i, image_info in enumerate(images):
    col = cols[i % 3]
    with col:
        st.markdown(f"##### {image_info['title']}")
        img = Image.open(image_info["path"])
        st.image(img, use_column_width=True)
    if (i + 1) % 3 == 0:
        st.write("")  # 行を分けるために空の行を追加
