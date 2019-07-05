import hashlib
import time

from pymongo import MongoClient

from weibo import Weibo


def md5(Str):
    MD5 = hashlib.md5()
    MD5.update(Str.encode())
    return MD5.hexdigest()


class Spider(object):
    def __init__(self):
        client = MongoClient(host='139.196.91.125', port=27017)
        self.db_1 = client['weibo']['comment']
        self.db_2 = client['weibo']['star_id']
        pass



    def run(self):
        while 1:
            ret = self.db_2.find()
            for i in ret:
                uid = int(i['star_id'])
                filter = 1  # 值为0表示爬取全部微博（原创微博+转发微博），值为1表示只爬取原创微博
                pic_download = 1  # 值为0代表不下载微博原始图片,1代表下载微博原始图片
                wb = Weibo(uid, filter, pic_download)
                pn = 1
                while 1:
                    wb.get_one_page(pn)
                    pn += 1
                    if pn == 3:
                        break
                    try:
                        for obj in wb.weibo:
                            obj['_id'] = md5(obj['screen_name']+obj['text']+obj['created_at'])
                            self.db_1.insert_one(obj)
                            print(obj)
                    except Exception:
                        break
                    wb.weibo = []
            time.sleep(60)


if __name__ == '__main__':
    s = Spider()
    s.run()
