import os
from pydub import AudioSegment


def convert_wav_to_mp3(wav_file_path, mp3_output_path):
 
    try:
        audio = AudioSegment.from_file(wav_file_path, format="wav")
        audio.export(mp3_output_path, format="mp3", bitrate="8k") 
        
        print(f"変換成功: '{wav_file_path}' -> '{mp3_output_path}'")
        
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません - '{wav_file_path}'")
    except Exception as e:
        print(f"変換中にエラーが発生しました: {e}")

input_wav = "C:/Users/okaji/Music/nogi.wav" 
output_mp3 = "C:/Users/okaji/Music/nogi8.mp3"

convert_wav_to_mp3(input_wav, output_mp3)