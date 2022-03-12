FROM python:3.9-buster
RUN mkdir /bot
WORKDIR /bot/
ADD . /bot/
RUN pip3 install -U -r requirements.txt
RUN apt update
RUN apt upgrade -y
RUN apt install libopus0 ffmpeg -y
CMD ["python3", "./bot.py"]