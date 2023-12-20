ARG PORT=443
# ADD LATEST PYTHON
FROM python
# ADD LATEST BROWSERS
FROM cypress/browsers
WORKDIR /app

RUN apt-get install wget
RUN sudo apt-get install unzip -y

RUN CHROME_VERSION=$(google-chrome-stable --version | grep -oP '(?<=Google Chrome )[^ ]+') && \
    CHROME_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip && \
    wget -q $CHROME_URL && \
    unzip chromedriver-linux64.zip && \
    chmod +x chromedriver-linux64/chromedriver

RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r requirements.txt

COPY . .
#ENV PORT=80
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT}"]
CMD uvicorn app:app --host 0.0.0.0 --port $PORT