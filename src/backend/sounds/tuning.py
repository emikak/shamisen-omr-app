import json

# 全体の調弦を設定
# JSONファイルの読み込み
with open("src/backend/sounds/tuning_data.json", "r", encoding="utf-8") as f:
    tuning_data = json.load(f)
print(tuning_data)

# 音階リスト (シャープのみで表記)
scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


# 音階シフトと調整を同時に行う関数
def shift_and_adjust_tuning(tuning_data, scale_shift, adjustment_type):
    adjusted_tuning = {}

    # 音階シフトをまず適用
    for string, notes in tuning_data.items():
        shifted_notes = []
        for char, note in notes.items():
            pitch, octave = note[:-1], int(note[-1])
            new_pitch_index = (scale.index(pitch) + scale_shift) % len(
                scale
            )  # 音階シフト
            new_pitch = scale[new_pitch_index]
            if new_pitch_index < scale.index(pitch):
                octave += 1  # オクターブが上がる場合
            shifted_notes.append(f"{new_pitch}{octave}")
        adjusted_tuning[string] = shifted_notes

    # 調子の調整を適用
    if adjustment_type == "二上がり":
        # 2本目の弦を1音上げる
        for i, note in enumerate(adjusted_tuning["2本目"]):
            pitch, octave = note[:-1], int(note[-1])
            new_pitch_index = (scale.index(pitch) + 1) % len(scale)  # 1音上げる
            new_pitch = scale[new_pitch_index]
            if new_pitch_index < scale.index(pitch):
                octave += 1
            adjusted_tuning["2本目"][i] = f"{new_pitch}{octave}"

    elif adjustment_type == "三下がり":
        # 3本目の弦を1音下げる
        for i, note in enumerate(adjusted_tuning["3本目"]):
            pitch, octave = note[:-1], int(note[-1])
            new_pitch_index = (scale.index(pitch) - 1) % len(scale)  # 1音下げる
            new_pitch = scale[new_pitch_index]
            if new_pitch_index > scale.index(pitch):
                octave -= 1
            adjusted_tuning["3本目"][i] = f"{new_pitch}{octave}"

    return adjusted_tuning


adjusted_tuning_data = shift_and_adjust_tuning(
    tuning_data, scale_shift=0, adjustment_type="二上がり"
)
print(adjusted_tuning_data)
