FROM python:3.13
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5001
RUN chmod a+x boot.sh
ENTRYPOINT [ "/app/boot.sh" ]
