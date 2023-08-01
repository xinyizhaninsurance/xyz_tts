import os
import re
import uuid
import time
from datetime import datetime
from flask import Flask, request, send_file
from log_config import Mylogger
from _my_schedule import __scheduler_init

app = Flask(__name__)
app.config['SCHEDULER_API_ENABLED'] = True

scheduler = __scheduler_init(app)

voiceMap = {
    "xiaoxiao": "zh-CN-XiaoxiaoNeural",
    "xiaoyi": "zh-CN-XiaoyiNeural",
    "yunjian": "zh-CN-YunjianNeural",
    "yunxi": "zh-CN-YunxiNeural",
    "yunxia": "zh-CN-YunxiaNeural",
    "yunyang": "zh-CN-YunyangNeural",
    "xiaobei": "zh-CN-liaoning-XiaobeiNeural",
    "xiaoni": "zh-CN-shaanxi-XiaoniNeural",
    "hiugaai": "zh-HK-HiuGaaiNeural",
    "hiumaan": "zh-HK-HiuMaanNeural",
    "wanlung": "zh-HK-WanLungNeural",
    "hsiaochen": "zh-TW-HsiaoChenNeural",
    "hsioayu": "zh-TW-HsiaoYuNeural",
    "yunjhe": "zh-TW-YunJheNeural",
}

logger = Mylogger('/tmp/tts.app.log').get_logger()


def getDir():
    pwdPath = os.getcwd()
    filePath = pwdPath + "/audio/"
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    return filePath


@scheduler.task('cron', id='delete_old_mp3_files', minute='*')
def delete_old_mp3_files():
    target_directory = getDir()  # 替换为您的目标目录
    logger.info('begin delete file at ' + str(datetime.now()) + ', dir is ' + target_directory)
    print('begin delete file at ' + str(datetime.now()) + ', dir is ' + target_directory)

    current_time = time.time()
    five_minutes_ago = current_time - 5 * 60

    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)

        if filename.endswith('.mp3') and os.path.isfile(file_path):
            file_creation_time = os.path.getctime(file_path)

            if file_creation_time < five_minutes_ago:
                try:
                    os.remove(file_path)
                    logger.info(f"Deleted file: {file_path}")
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    logger.info(f"Error deleting file: {file_path}, Error: {e}")


def getVoiceById(voiceId):
    return voiceMap.get(voiceId)


# 删除html标签
def remove_html(string):
    regex = re.compile(r'<[^>]+>')
    return regex.sub('', string)


def createAudio(text, file_name, voiceId):
    new_text = remove_html(text)
    logger.info(f"create file {file_name}, Text without html tags: {new_text}")
    voice = getVoiceById(voiceId)
    if not voice:
        return "error params"

    filePath = getDir() + file_name
    dirPath = os.path.dirname(filePath)
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    if not os.path.exists(filePath):
        # 用open创建文件 兼容mac
        open(filePath, 'a').close()

    script = 'edge-tts --voice ' + voice + ' --text "' + new_text + '" --write-media ' + filePath
    os.system(script)
    return filePath


def getParameter(paramName):
    if request.args.__contains__(paramName):
        return request.args[paramName]
    else:
        return request.form.get(paramName)
    return ""


@app.route('/dealAudio', methods=['POST', 'GET'])
def dealAudio():
    text = getParameter('text')
    # file_name = getParameter('file_name')
    file_name = str(uuid.uuid4()) + '.mp3'
    voice = getParameter('voice')
    f_path = createAudio(text, file_name, voice)
    return send_file(f_path, as_attachment=True, download_name=file_name)


@app.route('/')
def index():
    return 'welcome to my tts!'


if __name__ == "__main__":
    logger.info('应用启动开始')

    app.run(port=2020, host="127.0.0.1", debug=False)
