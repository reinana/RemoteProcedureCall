const net = require('net'); // requireでモジュールを読み込む サーバーサイドで使う場合はscriptが使えない
// netモジュール ネットワーク通信のためのモジュール
const socketFile = '/tmp/json_rpc_socket.sock';
// net.SocketオブジェクトはTCPまたはUNIXソケットを作る
const client = new net.Socket();

// リクエストの作成
const request = {
    jsonrpc: '2.0',
    method: 'sum',
    params: '[1, 2]',
    id: 1
};

// 入力の受付
function readUserInput(question) {
    const readline = require('readline').createInterface({
        input: process.stdin,
        output: process.stdout
    });
    return new Promise((resolve, reject) => {
        readline.question(question, (answer) => {
            resolve(answer);
            readline.close();
        });
    });
}

  // メイン処理
(async function main() {
    // 入力からリクエストの更新
    method = await readUserInput('Method? ');
    params = await readUserInput('Params? ');
    id = await readUserInput('Id? ');

    request.method = method == ""? request.method : method;
    request.params = params == ""? request.params : params;
    request.id = id == ""? request.id : id;

    console.log(request);
    
    
    client.connect(socketFile, () => {
        console.log('Connected to server');
        
        // リクエストの送信
        client.write(JSON.stringify(request));
    });
    
    // データの受信
    client.on('data', (data) => {
        const response = JSON.parse(data);
        
        if (response.error) {
            console.error('Error:', response.error);
        } else {
            console.log(request.method, response.result);
        }
        
        // クライアントのクローズ
        client.end();
    });
    
    // 接続終了時の処理
    client.on('close', () => {
        console.log('Connection closed');
    });
    
    // エラーハンドリング
    client.on('error', (error) => {
        console.error('Error:', error);
    });
    
})();
    