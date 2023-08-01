FROM python:3.8.4
COPY requirements.txt ./
RUN pip install  -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . /app/
WORKDIR /app/

CMD ["gunicorn", "edge-tts:app", "-c","gunicorn.py"]
