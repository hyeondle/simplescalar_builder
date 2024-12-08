from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/exec', methods=['POST'])
def execute_command():
    try:
        # 입력된 명령어를 JSON 데이터로 받음
        data = request.get_json()
        command = data.get('command')

        if not command:
            return jsonify({"error": "No command provided"}), 400

        # 명령어 실행
        result = subprocess.run(
            command, shell=True, text=True, capture_output=True
        )

        # 실행 결과 반환
        return jsonify({
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"message": "OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
