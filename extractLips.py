from cutVideos import *
import numpy as np
import cv2
import face_alignment
import os
import shutil
import torch


"""
    TODO:
        フレーム数と口元領域のフレーム数の枚数が合わない小分けビデオデータ、音声データ、フレームデータ
        口元のフレームを削除するコードの追加
"""


class ExtractLips(CutVideos):
    def __init__(self, vps=None, svp="datas/lips"):
        super().__init__(vps, svp)

    def get_position(self, size, padding=0.25):

        x = [0.000213256, 0.0752622, 0.18113, 0.29077, 0.393397, 0.586856, 0.689483, 0.799124,
                        0.904991, 0.98004, 0.490127, 0.490127, 0.490127, 0.490127, 0.36688, 0.426036,
                        0.490127, 0.554217, 0.613373, 0.121737, 0.187122, 0.265825, 0.334606, 0.260918,
                        0.182743, 0.645647, 0.714428, 0.793132, 0.858516, 0.79751, 0.719335, 0.254149,
                        0.340985, 0.428858, 0.490127, 0.551395, 0.639268, 0.726104, 0.642159, 0.556721,
                        0.490127, 0.423532, 0.338094, 0.290379, 0.428096, 0.490127, 0.552157, 0.689874,
                        0.553364, 0.490127, 0.42689]

        y = [0.106454, 0.038915, 0.0187482, 0.0344891, 0.0773906, 0.0773906, 0.0344891,
                        0.0187482, 0.038915, 0.106454, 0.203352, 0.307009, 0.409805, 0.515625, 0.587326,
                        0.609345, 0.628106, 0.609345, 0.587326, 0.216423, 0.178758, 0.179852, 0.231733,
                        0.245099, 0.244077, 0.231733, 0.179852, 0.178758, 0.216423, 0.244077, 0.245099,
                        0.780233, 0.745405, 0.727388, 0.742578, 0.727388, 0.745405, 0.780233, 0.864805,
                        0.902192, 0.909281, 0.902192, 0.864805, 0.784792, 0.778746, 0.785343, 0.778746,
                        0.784792, 0.824182, 0.831803, 0.824182]

        x, y = np.array(x), np.array(y)

        x = (x + padding) / (2 * padding + 1)
        y = (y + padding) / (2 * padding + 1)
        x = x * size
        y = y * size
        # xとyを1組のセットにしてその組み合わせを配列にして、numpy配列に変換している
        return np.array(list(zip(x, y)))

    # 正規化や特異値分解で次元の削減
    def transformation_from_points(self, points1, points2):
        points1 = points1.astype(np.float64)
        points2 = points2.astype(np.float64)

        # 列ごとの平均値を返す
        c1 = np.mean(points1, axis=0)
        c2 = np.mean(points2, axis=0)

        # 全ての要素に-平均値をする
        points1 -= c1
        points2 -= c2
        # 標準偏差を求める
        s1 = np.std(points1)
        s2 = np.std(points2)
        # 正規化
        points1 /= s1
        points2 /= s2

        U, S, Vt = np.linalg.svd(points1.T * points2) #points1の転置とpoints2の積の値の特異値分解
        R = (U * Vt).T # UとVtの積を転置
        return np.vstack([np.hstack(((s2 / s1) * R,
                                           c2.T - (s2 / s1) * R * c1.T)),
                             np.matrix([0., 0., 1.])])

    def _run(self, path):
        files = os.listdir(path)
        if files == []:
            print('Message: ', path, ' is empty.')
            return
        files.sort()
        #files = [files[0], files[1]]
        array = [cv2.imread(os.path.join(path, file)) for file in files]
        # データがないものをフィルタ処理をしたデータの配列を返す
        array = list(filter(lambda im: not im is None, array))
        #array = [cv2.resize(im, (100, 50), interpolation=cv2.INTER_LANCZOS4) for im in array]

        # 2Dの画像の人の顔のランドマークを検出するオブジェクトのインスタンスを生成
        #fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False, device='cpu')

        fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, flip_input=False, device='cuda') #GPU使用の場合これを使う
        # フレームの画像のランドマークを配列として取得
        points = [fa.get_landmarks(I) for I in array]

        front256 = self.get_position(256)
        i=0
        print('\nExtract now ...')
        for point, scene in zip(points, array): # フレームのランドマークと対応しているフレームの画像を1セットにしてそれを順に回す。
        #(point: ランドマーク, scene: ランドマークに対応している画像)
            if(point is not None): # ランドマークがある場合
                shape = np.array(point[0])
                # 口元部分のランドマークだけをとる
                shape = shape[17:]
                M = self.transformation_from_points(np.matrix(shape), np.matrix(front256))

                img = cv2.warpAffine(scene, M[:2], (256, 256)) # アフィン変換 計算コストの軽量化
                (x, y) = front256[-20:].mean(0).astype(np.int32)
                w = 160//2
                img = img[y-w//2:y+w//2,x-w:x+w,...]
                img = cv2.resize(img, (128, 64)) # 128x64の大きさに変換
                # 保存先の設定
                cv2.imwrite(os.path.join(self.svp, (path.split('/')[-2]), (path.split('/')[-1]), files[i]), img)
                # パスの保存
            i=i+1
        print('start: ')
        print(os.system('nvidia-smi'))
        print()
        del fa
        torch.cuda.empty_cache()
        print('cache delete: ')
        print(os.system('nvidia-smi'))
        print()
        self._check_data(path)
    
    def _check_data(self, path):
        root, frame_path, parent_number, data_number = path.split('/')
        frames_len = len(os.listdir(path))
        lips_len = len(os.listdir(os.path.join(self.svp, parent_number, data_number)))
        if ((frames_len - lips_len) != 0):
            root, _, parent_number, data_number = path.split('/')
            lips_path = os.path.join(self.svp, parent_number, data_number)
            voice_path = os.path.join(root, "fa_voice", parent_number, data_number+'.wav')
            cut_video_path = os.path.join(root, "fa_cut_videos", parent_number, data_number+'.mp4')
            print('Short of lips frame.')
            print('Delete: ')
            print('frames: ', path)
            shutil.rmtree(path)
            print('lips: ', lips_path)
            shutil.rmtree(lips_path)
            print('cut_video: ', cut_video_path)
            os.remove(cut_video_path)
            print('voice: ', voice_path)
            os.remove(voice_path)
        else:
            print('Check pass.')
        print('frames_len: {}'.format(frames_len))
        print('lips_len: {}'.format(lips_len))

    def _extract_lips(self):
        print("-"*10, " START EXTRACT LIPS ", "-"*10)
        self.exists_folder(self.svp)
        if self.vps == None:
            print("-"*10, "FAILED", "-"*10, '\n')
            return
        for vp in self.vps:
            data_paths = [os.path.join(vp, file) for file in os.listdir(vp)]
            print("\nData: ", vp, "\n")
            if data_paths == []:
                continue
            data_paths.sort()
            for data in data_paths:
                print("\nData: ", data, "\n")
                fn = data.split('/')
                self.exists_folder(os.path.join(self.svp, fn[-2]))
                self.exists_folder(os.path.join(self.svp, fn[-2], fn[-1]))
                if 88 <= len(os.listdir(os.path.join(self.svp, fn[-2], fn[-1]))):
                    print('Exists more 88.')
                    print()
                    continue
                self._run(data)
        print("-"*10, " FINISH EXTRACT LIPS ", "-"*10)
        _, _, free = shutil.disk_usage('/')
        free = int((free/(10**9)))
        if (free <= 3):
            print('Must increase capacity.')
            exit()
