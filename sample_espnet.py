import soundfile
from espnet2.bin.asr_inference import Speech2Text
from espnet_model_zoo.downloader import ModelDownloader

d = ModelDownloader()
d.download_and_unpack("kan-bayashi/csj_asr_train_asr_transformer_raw_char_sp_valid.acc.ave")
speech2text = Speech2Text.from_pretrained(
    "kan-bayashi/csj_asr_train_asr_transformer_raw_char_sp_valid.acc.ave",
    # Decoding parameters are not included in the model file
    maxlenratio=0.0,
    minlenratio=0.0,
    beam_size=20,
    ctc_weight=0.3,
    lm_weight=0.5,
    penalty=0.0,
    nbest=1
)
# Confirm the sampling rate is equal to that of the training corpus.
# If not, you need to resample the audio data before inputting to speech2text
speech, rate = soundfile.read("sample.wav")
nbests = speech2text(speech)

text, *_ = nbests[0]
print(text)
