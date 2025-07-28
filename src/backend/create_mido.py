import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage


def note_to_midi_number(note):
    name, octave = note[:-1], int(note[-1])
    if name in note_to_midi:
        print(name, octave)
        print(note_to_midi[name] + (octave - 4) * 12)
        return note_to_midi[name] + (octave - 4) * 12
    else:
        raise ValueError(f"Invalid note name: {note}")


def get_note_from_dic_value(dic_value):

    # イ＋漢数字の場合、一本目
    for i in dic_value:
        if i == "イ":
            string = "1本目"
            dic_value = dic_value[1:]
            break
    else:
        for i in dic_value:
            if i in chinese_character:
                string = "2本目"
                break
        else:
            string = "3本目"

    if string not in shamisen_to_scale:
        raise ValueError(f"Invalid string: {string}")

    note = 0
    velocity = 127
    for i in range(len(dic_value)):
        print(dic_value[i])
        if dic_value[i] in chinese_character:
            note += chinese_character_to_number[dic_value[i]]
            continue

        if dic_value[i] in number_to_index.keys():
            note += number_to_index[dic_value[i]]
            continue

        if dic_value[i] == "・":
            note += 9

        # TODO スリが入った時の処理
        # TODO はじき、すくい、打つの処理
        if dic_value[i] == "ス":
            velocity = 127 * SUKUI_VOLUME

        if dic_value[i] == "^":
            velocity = 127 * HAJIKI_VOLUME

        if dic_value[i] == "ゥ":
            velocity = 127 * UTSU_VOLUME

    print(dic_value[i])
    print(string, note)
    position = shamisen_to_scale[string][note]
    print(position)
    midi_number = note_to_midi_number(position)
    return note, midi_number, velocity


# MIDIファイルを作成する関数
def create_midi_file(note_sequence, file_name):
    tempo = 180
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage("set_tempo", tempo=mido.bpm2tempo(tempo)))

    ku_flag = 0
    # タプルのリスト
    # 一つのタプルは、一小節
    # タプルの中には複数の音階
    notes = []

    for note in note_sequence:
        if note == ["◯"] or note == [""] or note == ["△"]:
            track.append(Message("note_off", time=480))  # 休符
            notes.append((0))
        else:
            if note == ["スリ上下"]:
                midi_number = notes[-1] - 1
                track.append(
                    Message(
                        "note_on",
                        note=midi_number,
                        velocity=int(127 * SURI_VOLUME),
                        time=0,
                    )
                )
                track.append(Message("note_off", note=midi_number, time=240))
                midi_number = notes[-1] + 1
                track.append(
                    Message(
                        "note_on",
                        note=midi_number,
                        velocity=int(127 * SURI_VOLUME),
                        time=0,
                    )
                )
                track.append(Message("note_off", note=midi_number, time=240))
                # 便宜上追加
                notes.append((0))
                continue

            if note == ["ゝ"]:
                for i in range(2):
                    track.append(track[-4])
                notes.append(notes[-1])
                continue

            # くについて
            if ku_flag:
                ku_flag = 0
                continue
            elif note == ["く"]:
                ku_flag = 1
                for i in range(4):
                    track.append(track[-4])
                notes.append(notes[-2])
                notes.append(notes[-2])
                continue

            if note == ["ス"]:
                velocity = 127 * SUKUI_VOLUME
                track.append(
                    Message(
                        "note_on",
                        note=notes[-1],
                        velocity=int(127 * SUKUI_VOLUME),
                        time=0,
                    )
                )
                track.append(Message("note_off", note=notes[-1], time=480))
                # 便宜上追加
                notes.append((0))
                continue

            # TODO スリのときの実装
            if note == ["スリ上"]:
                track.append(
                    Message(
                        "note_on",
                        note=notes[-1] - 1,
                        velocity=int(127 * SURI_VOLUME),
                        time=0,
                    )
                )
                track.append(Message("note_off", note=notes[-1] - 1, time=480))
                # 便宜上追加
                notes.append((0))
                continue
            if note == ["スリ下"]:
                track.append(
                    Message(
                        "note_on",
                        note=notes[-1] + 1,
                        velocity=int(127 * SURI_VOLUME),
                        time=0,
                    )
                )
                track.append(Message("note_off", note=notes[-1] + 1, time=480))
                # 便宜上追加
                notes.append((0))
                continue

            note_name, midi_number, velocity = get_note_from_dic_value(note)
            track.append(
                Message("note_on", note=midi_number, velocity=int(velocity), time=0)
            )
            track.append(Message("note_off", note=midi_number, time=480))
            notes.append(midi_number)

    mid.save(file_name)
