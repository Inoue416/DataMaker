import random

train_datas = []
val_datas = []
def LoadFile(path):
    with open(path, 'r') as f:
        data = (f.read()).split('\n')
        data.remove('')
        random.shuffle(data)
        length = len(data)
        half_l = int(length*7/10)+1
        train_datas.extend(data[0:half_l])
        train_datas.sort()
        val_datas.extend(data[half_l:])
        val_datas.sort()
    return

def writeResults(path, typ):
    with open(path, 'w') as f:
        if 't' == typ:
            for data in train_datas:
                if '\n' in data:
                    data  = data.replace('\n', '')
                f.write(data+'\n')
        else:
            for data in val_datas:
                if '\n' in data:
                    data  = data.replace('\n', '')
                f.write(data+'\n')
    return 




def main():
    print('----- START -----\n')
    print('Load file')
    j = 0
    while j == 0:
        filename = input('Please filename or path: ')
        LoadFile(filename)
        print('0: CONTINUE  1: FINISH')
        j = int(input("Please select: "))
    print()
    print('Writting results now ...')
    writeResults("train_dataPath.txt", 't')
    writeResults("val_dataPath.txt", 'v')
    print('----- FINISH -----')
main()