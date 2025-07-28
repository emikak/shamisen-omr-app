import os
from typing import List, Tuple

from PIL import Image, ImageOps


def results_to_txt_yolo(
    results: List[List[Tuple[str, List[int]]]], output_file: str = "yolo_results.txt"
) -> None:
    """YOLO推論結果をテキストファイルに書き出す"""
    with open(output_file, "w") as f:
        for i, image_results in enumerate(results):
            for label, bbox in image_results:
                f.write(f"Image {i}: Label={label}, BBox={bbox}\n")


def remove_temp_files(num_files: int) -> None:
    """一時保存された画像ファイルを削除する"""
    for i in range(num_files):
        file_path = f"temp_image_{i}.png"
        if os.path.exists(file_path):
            os.remove(file_path)


def convert_background_to_grayscale(
    image_path: str, output_path: str, threshold: int = 128
) -> None:
    """画像の背景を白黒に変換する"""
    with Image.open(image_path) as img:
        # 画像をグレースケールに変換
        grayscale_img = ImageOps.grayscale(img)

        # 2値化
        binarized_img = grayscale_img.point(
            lambda x: 255 if x > threshold else 0, mode="1"
        )

        # 変換した画像を保存
        binarized_img.save(output_path)

