import socket
import os
import math
import json

class Callable:
    def sum(arr):
        print('sum')
        return arr[0] + arr[1]
    
    def floor(args):
        print('floor')
        return math.floor(float(args))
    
    def nroot(args):
        print('nroot')
        args=args[1:-1].split(',')
        print(args)
        x = int(args[0])
        y = int(args[1])
        print(x,y)
        return math.pow(x, 1/y)
    
    def reverse(args):
        print('reverse')
        return args[::-1]
    
    def validAnagram(args):
        print('validAnagram')
        args=args[1:-1].split(',')
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
    
    def sortArr(args):
        print('sort')
        args=args[1:-1].replace("'","").split(',')
        print(args)
        return sorted(args)

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
        params = dict['params']

        if method == 'sum':
            result = Callable.sum(params)
            return {
                'result': result,
                'error': None,
                'id': dict['id']
            }
        elif method == 'floor':
            result = Callable.floor(params)
            return {
                'result': result,
                'error': None,
                'id': dict['id']
            }
        elif method == 'nroot':
            result = Callable.nroot(params)
            return {
                'result': result,
                'error': None,
                'id': dict['id']
            }
        elif method == 'reverse':
            result = Callable.reverse(params)
            return {
                'result': result,
                'error': None,
                'id': dict['id']
            }
        elif method == 'validAnagram':
            result = Callable.validAnagram(params)
            return {
                'result': result,
                'error': None,
                'id': dict['id']
            }
        elif method == 'sort':
            result = Callable.sortArr(params)
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