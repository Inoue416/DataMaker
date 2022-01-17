import os

# TODO: USBなどのデバイスからorigindataフォルダーに抽出するデータのコピーを行うための処理を入れる

"""
    0: making short videos.
    1: making frames of 0 and extract voice of 0.
    2: check face in frames. if not find face, write log file.
    3: voice data to text data.
    4: extract lips from frames of 1.
"""

data_root = 'datas/'
"""origin = "originDatas"
data_origin = os.path.join(data_root, origin)
# this options is that save data and load data.
data_save = [
    os.path.join(data_root, "cut_videos"),
    [os.path.join(data_root, "frames"), os.path.join(data_root, "voice")],
    os.path.join(data_root, "lips")
]

d_path = [
          os.path.join(data_root, "cut_video_path"),
          os.path.join(data_root, "frames_path"),
          os.path.join(data_root, "voice_path")
          ]

s_path = [os.path.join(data_root, "cut_video_path"),
          [os.path.join(data_root, "frames_path"), os.path.join(data_root, "voice_path")],
          os.path.join(data_root, "face_logs"),
          os.path.join(data_root, "voice_to_anno"),
          os.path.join(data_root, "lips_path")]"""

# full auto mode options
full_folder = "originDatas" # this option is text file of data path list.
full_auto_path = os.path.join(data_root, full_folder)

fa_data_save = [
    os.path.join(data_root, "fa_cut_videos"),
    [os.path.join(data_root, "fa_frames"), os.path.join(data_root, "fa_voice")],
    os.path.join(data_root, "fa_lips"),
    os.path.join(data_root, "fa_anno")
]

fa_d_path = [
             os.path.join(data_root, "fa_cut_video_path"),
             os.path.join(data_root, "fa_frames_path"),
             os.path.join(data_root, "fa_voice_path")
             ]

fa_s_path = [os.path.join(data_root, "fa_cut_video_path"),
             [os.path.join(data_root, "fa_frames_path"), os.path.join(data_root, "fa_voice_path")],
             os.path.join(data_root, "fa_lips_path")
             ]

vr_preweight = "kan-bayashi/csj_asr_train_asr_transformer_raw_char_sp_valid.acc.ave"
