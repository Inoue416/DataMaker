from cutVideos import CutVideos
import os
import sys
import options as opt

if __name__ == "__main__":
    opt = __import__('options')

def load_path(path):
    paths = []
    try:
        with open(path, 'r') as f:
            r = ((f.read()).split('\n'))
            r.remove('')
            paths.extend(r)
        return paths
    except:
        return None

if __name__ == "__main__":
    judge = True
    print(os.getcwd())
    # データのロード
    while judge:
        print("-"*10, ' LOAD DATA PATH ', "-"*10, '\n')
        print("Input name of load file.")
        filename = input("INPUT: ")
        # データのパスのロード
        path = os.path.join(opt.data_root, filename)
        print(path)
        path = load_path(path)
        print(path)
        if not path:
            print("No file.")
            break
        # インスタンスの作成
        cvs = CutVideos(path)
        if not cvs._cut_videos():
            print('Not found data.')
        while True:
            print("\n0: FINISH  1: CONTINUE")
            j = input("INPUT: ")
            if j == "0":
                judge = False
                break
            elif j == "1":
                break
            else:
                print("\nInput error.")
                print("Please input 0 or 1 only.")
    print("\n-"*10 ," END ", "-"*10)
