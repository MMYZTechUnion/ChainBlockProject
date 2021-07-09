import hashlib
import os

import rsa

import units


class BlockChain:
    def __init__(self, storage_path, key_tuple=None):  # TODO set start
        if key_tuple is None:
            (self.PBA, self.PVA) = rsa.newkeys(1024)
        else:
            (self.PBA, self.PVA) = key_tuple
        print('PVA\n', self.PVA.save_pkcs1().decode(), '\nPBA\n', self.PBA.save_pkcs1().decode())

        # DEBUG
        self.BASE_DIR = storage_path  # 储存目录
        os.system('md %s\\root' % self.BASE_DIR)  # Windows
        # DEBUG END

        self.blocks = []
        self.current_block = units.Block()
        self.new_block()

    def add(self, data):  # 添加数据
        record = units.Record(data, self.PVA)
        # DEBUG
        exp = record.export()
        print('record:', exp)
        print('Verification： ',
              rsa.verify(('%s%d' % (record.abstract, record.timestamp)).encode(), record.sign, self.PBA))  # 验签测试
        with open('%s\\%s\\%s.json' % (  # Windows
                self.BASE_DIR, self.current_block.last_hash, hashlib.sha256(exp.encode()).hexdigest()), 'w') as fp:
            fp.write(exp)
        # DEBUG END
        if self.current_block.push(record) == -1:  # 下一区块
            self.new_block()
            self.current_block.push(record)

    def new_block(self):
        nb = units.Block(self.current_block.close())

        # DEBUG
        print('block:', self.current_block.export())
        with open('%s\\%s\\BL%s.json' % (self.BASE_DIR, self.current_block.last_hash, self.current_block.hash),
                  # Windows
                  'w') as fp:
            fp.write(self.current_block.export())
        # DEBUG END

        self.blocks.append(self.current_block)
        self.current_block = nb

        # DEBUG
        os.system('md %s\\%s' % (self.BASE_DIR, self.current_block.last_hash))  # Windows
        # DEBUG END

    # TODO 模块：从本地加载区块链
