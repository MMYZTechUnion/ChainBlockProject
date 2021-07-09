import json
import time
import hashlib
import rsa
import random


class Record:  # 数据记录
    def __init__(self, data: str, PVA):
        self.data = data  # 原始数据
        self.PVA = PVA  # 私钥
        self.timestamp = int(round(time.time() * 1000))  # 时间戳
        self.abstract = hashlib.sha256(data.encode()).hexdigest()  # 摘要
        self.sign = rsa.sign(('%s%d' % (self.abstract, self.timestamp)).encode(), PVA, 'SHA-256')  # 签名
        print('DEBUG: Sign Field: ', ('%s%d' % (self.abstract, self.timestamp)).encode())  # DEBUG

    def export(self):  # 输出
        # bytes转十六进制字符串，如需验签则要将十六进制字符串转bytes
        # Refer to:  https://www.cnblogs.com/dreamblog/p/10219175.html
        sign_hex = ''.join(['%02X ' % b for b in self.sign])

        return json.dumps({'abstract': self.abstract,
                           'data': self.data,
                           'sign': sign_hex,
                           'timestamp': self.timestamp})


class Block:  # 区块
    def __init__(self, last_hash=None):
        self.records = []
        self.hash = ''
        self.timestamp = 0
        if last_hash is None:  # 创世区块
            self.last_hash = 'root'
        else:
            self.last_hash = last_hash

    def push(self, record: Record):  # 追加数据
        if len(self.records) >= 4:  # length of record set
            return -1
        else:
            self.records.append(record.export())
            return 0

    def close(self):  # 区块终了&封存
        hashes = self.last_hash
        for i in self.records:
            hashes = ''.join([hashes, hashlib.sha256(i.encode()).hexdigest()])
        self.timestamp = int(round(time.time() * 1000))
        hashes = '%s%d%06d' % (hashes, self.timestamp, random.randint(0, 1000000))
        self.hash = hashlib.sha256(hashes.encode()).hexdigest()
        return self.hash

    def export(self):
        if self.hash == '':
            return ''
        ret = {'last_hash': self.last_hash, 'timestamp': self.timestamp, 'hash': self.hash, 'records': []}
        for i in self.records:
            ret['records'].append(i)
        return json.dumps(ret)
