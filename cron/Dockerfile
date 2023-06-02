FROM python:3.11-slim
COPY ./* /pyweb3
WORKDIR /pyweb3/
RUN apt update && apt install -y cron
RUN chmod 0644 /pyweb3/crawling_data.py && \
    rm -rf /etc/localtime  && \ 
    ln -s /usr/share/zoneinfo/Asia/Seoul /etc/localtime &&  \ 
    cat /etc/localtime
RUN crontab -l | { cat; echo "*/5 * * * * python3 /pyweb3/crawling_data.py"; } | crontab -
RUN python3 -m pip install -r requirements.txt
CMD ["cron", '-f']
