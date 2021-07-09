import os.path

import blockchain_operator


def writeKeys(key, path):
    with open(path, 'wb') as fp:
        fp.write(key.save_pkcs1())


if __name__ == '__main__':
    BASE_DIR = 'bc'  # 储存目录
    if os.path.exists(BASE_DIR):
        print('Warning: The BASE_DIR has already existed.')
    bc = blockchain_operator.BlockChain(BASE_DIR, key_tuple=None)
    writeKeys(bc.PBA, os.path.join(BASE_DIR, 'Public.pem'))
    writeKeys(bc.PVA, os.path.join(BASE_DIR, 'Private.pem'))
    i = 1
    while True:
        data = input('Enter Data %d: ' % i)
        i += 1
        bc.add(data)
        print()
