import streamlit as st
import streamlit.components.v1 as components

# JavaScriptコードを含むHTMLテンプレート
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speech Recognition</title>
</head>
<body>
    <h2>音声認識デモ</h2>
    <select id="language-select">
        <option value="ja-JP">日本語</option>
        <option value="en-US">英語</option>
    </select>
    <button id="start-recording">録音開始</button>
    <button id="stop-recording">録音停止</button>
    <p id="result"></p>
    <script>
        let recognition;
        const languageSelect = document.getElementById('language-select');
        const resultElement = document.getElementById('result');
        
        document.getElementById('start-recording').onclick = function() {
            if (!('webkitSpeechRecognition' in window)) {
                resultElement.innerHTML = "このブラウザは音声認識をサポートしていません。";
                return;
            }

            recognition = new webkitSpeechRecognition();
            recognition.lang = languageSelect.value;
            recognition.interimResults = false;
            recognition.onresult = function(event) {
                resultElement.innerHTML = event.results[0][0].transcript;
                // Streamlitのテキスト表示エリアに結果を送信
                window.parent.postMessage({ type: 'SPEECH_RESULT', text: event.results[0][0].transcript }, '*');
            };
            recognition.start();
        };

        document.getElementById('stop-recording').onclick = function() {
            if (recognition) {
                recognition.stop();
            }
        };

        window.addEventListener('message', function(event) {
            if (event.data.type === 'SPEECH_RESULT') {
                window.parent.postMessage(event.data, '*');
            }
        });
    </script>
</body>
</html>
"""

# Streamlitのアプリケーション
st.title("音声認識アプリ")

# HTMLテンプレートを表示
components.html(HTML_TEMPLATE, height=400)

# 音声認識結果を表示するエリア
result = st.empty()

# JavaScriptからのメッセージを受信
def message_handler(message):
    if message['type'] == 'SPEECH_RESULT':
        result.write("音声認識結果: " + message['text'])

# メッセージのリスナーを設定
components.html("""
<script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'SPEECH_RESULT') {
            window.parent.postMessage(event.data, '*');
        }
    });
</script>
""")

# メッセージ受信を試みる
message_handler({"type": "SPEECH_RESULT", "text": "音声認識結果が表示されます"})
