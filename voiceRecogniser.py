import os
from cutVideos import *
from espnet2.bin.asr_inference import Speech2Text
from espnet_model_zoo.downloader import ModelDownloader

class VoiceRecogniser(CutVideos):
    def __init__(self, vps=None, svp="datas/anno_data", pre_weight):
        super().__init__(vps, svp)
        self.pre_weight = pre_weight

    def _write_anno(self, text, foldername, filename):
        #self.exists_folder(os.path.join(self.svp, foldername))
        """try:
            with open(os.path.join(self.svp, foldername, filename+".txt"), 'w') as f:
                f.write(text)
        except:
            print("Not found {}\n".format(os.path.join(self.svp, foldername)))
            print("Can't write result.\n")"""

    def _voice_recognition(self):
        #self.exists_folder(self.svp)
        """d = ModelDownloader()
        d.download_and_unpack(self.pre_weight)
        speech2text = Speech2Text.from_pretrained(
            self.pre_weight,
            maxlenratio=0.0,
            minlenratio=0.0,
            beam_size=20,
            ctc_weight=0.3,
            lm_weight=0.5,
            penalty=0.0,
            nbest=1
        )"""
        for vp in self.vps:
            print(vp)
            filename = vp.split('/')
            filename.remove('')
            foldername = filename[-2]
            filename = filename[0]
            filename, _ = os.path.spplitext(filename)
            print(filename, foldername)
            """speech, rate = soundfile.read(vp)
            nbests = speech2text(speech)
            text, *_ = nbests[0]
            filename = vp.split('/')
            filename.remove('')
            foldername = filename[-2]
            filename = filename[0]
            filename, _ = os.path.spplitext(filename)
            self._write_anno(text, foldername, filename)"""
