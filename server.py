import socket
import os
import math
import json

class Callable:
    #ラムダにする
    def sum(args):
        print('sum')
        def func(args):
            x = int(args[0])
            y = int(args[1])
            return x + y
        return func(args)

    def floor(args):
        print('floor')
        def func(args):
            return math.floor(float(args[0]))
        return func(args)
    
    def nroot(args):
        print('nroot')
        def f(args):
 
            print(args)
            x = int(args[0])
            y = int(args[1])
            print(x,y)
            return math.pow(x, 1/y)
        return f(args)
    
    def reverse(args):
        print('reverse')
        def f(args):
            return args[0][::-1]
        return f(args)
    
    def validAnagram(args):
        print('validAnagram')
        def f(args):

            # 小文字に変換して、空白を削除します
            s1 = args[0].lower().replace(" ", "").replace("'","")
            s2 = args[1].lower().replace(" ", "").replace("'","")
            print(s2)

            if len(s1) != len(s2): return False

            # a-z分までのキャッシュを作成します
            cache = []
            for i in range(26):
                cache.append(0)

            # s1とs2を同時にチェックします
            for i in range(len(s1)):
                # aの文字コードは97
                # a=97, b=98, c=99, d=100, ... , z=122 を
                # a=0, b=1, c=2, d=3, ... , z=25 へ変換
                cache[ord(s1[i]) - 97] += 1
                cache[ord(s2[i]) - 97] -= 1

            # 最大値0、最小値0の時のみ、アナグラムになります
            return max(cache) == 0 and min(cache) == 0
        return f(args)
    
    def sortArr(args):
        print('sort')
        def f(args):
            for i in range(len(args)):
                args[i] = args[i].replace("'","")
            newArr = sorted(args)
            return newArr
        return f(args)

# ソケット生成クラス
class Socket:

    def createSocket():     

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_address = "/tmp/json_rpc_socket.sock"

        # ファイルが既に存在しないことを確認する
        try:
            os.unlink(server_address)
        except FileNotFoundError:
            pass

        # ソケットをアドレスに紐付ける
        print("Starting up on {}".format(server_address))
        sock.bind(server_address)

        # 接続
        sock.listen(1)

        # # サーバが常に接続を待ち受けるためのループ
        while True:
            connection, client_address = sock.accept()
            try:
                print("connection from", client_address)

                while True:
                    data = connection.recv(1024)
                    data_str = data.decode("utf-8")
                    # リクエストをdictに変換
                    dict = json.loads(data)
                    answer = Handler.handle_request(dict)

                    # レスポンスの送信
                    if data:
                        connection.sendall(json.dumps(answer).encode())

                    else:
                        print("no data from", client_address)
                        break

            finally:
                # 接続のクリーンアップ
                print("Closing current connection")
                connection.close()
                break

class Handler:
    def handle_request(dict):
                # リクエストの処理
        # ここでは単純にパラメータの合計を計算して返す例を示します
        method = dict['method']
        params = dict['params'][1:-1].split(',')
        #<string, callable>ハッシュマップ
        table = {
            'sum': Callable.sum,
            'floor': Callable.floor,
            'nroot': Callable.nroot,
            'reverse': Callable.reverse,
            'validAnagram': Callable.validAnagram,
            'sort': Callable.sortArr,
        }
        if table[method]:
            result = table[method](params)
            return {
                'result': result,
                'error': None,
                'id': dict['id']
            }
        else:
            return {
                'result': None,
                'error': 'Unknown method',
                'id': dict['id']
            }


def main():
    Socket.createSocket()
    return 0


if __name__ == '__main__':
    main()