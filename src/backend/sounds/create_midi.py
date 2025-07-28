import mido
from mido import Message, MidiFile, MidiTrack

# 音階データをMIDIノート番号に変換するための対応表
note_to_midi = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11,
}


# 音階データをMIDIノート番号に変換する関数
def note_to_midi_number(note):
    pitch = note[:-1]  # 音階 (例: "D", "C#")
    octave = int(note[-1])  # オクターブ (例: "4")
    midi_number = note_to_midi[pitch] + (octave + 1) * 12  # MIDI番号に変換
    return midi_number


# MIDIファイルを生成する関数
def create_midi(tuning_data, output_filename="output2.mid", tempo=500):
    midi = MidiFile()  # 新しいMIDIファイルを作成
    track = MidiTrack()  # 新しいトラックを作成
    midi.tracks.append(track)

    # 音階データをMIDIに変換して追加
    for string, notes in tuning_data.items():
        for note in notes:
            midi_number = note_to_midi_number(note)
            # ノートオンメッセージを追加 (音を鳴らす)
            track.append(Message("note_on", note=midi_number, velocity=64, time=0))
            # ノートオフメッセージを追加 (音を止める)
            track.append(Message("note_off", note=midi_number, velocity=64, time=tempo))

    # MIDIファイルとして保存
    midi.save(output_filename)
    print(f"MIDIファイルを生成しました: {output_filename}")


# 使用例: 調整された音階データをMIDIに変換
tuning_data = {
    "1本目": [
        "D3",
    ],
    "2本目": [
        "G3",
    ],
    "3本目": [
        "D4",
    ],
}

# MIDIファイルを生成
create_midi(tuning_data, "output2.mid")
