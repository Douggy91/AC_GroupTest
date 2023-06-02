FROM python:3.11-slim
COPY ./pyweb-app/ /pyweb3/
WORKDIR /pyweb3/
EXPOSE 7710
RUN python3 -m pip install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["./index.py"]