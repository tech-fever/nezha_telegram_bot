FROM python:3.9.13-alpine3.16
RUN cd /opt/ \
    mkdir nezha_telegram_bot \
    cd /opt/
WORKDIR /opt/nezha_telegram_bot
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"]
