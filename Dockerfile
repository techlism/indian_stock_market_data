ARG PORT=443
# ADD LATEST PYTHON
FROM python
# ADD LATEST BROWSERS

WORKDIR /app
# RUN apt-get install -y appstream/xenial-backports
RUN apt-get update && apt-get install -y wget unzip gnupg

# Download and install the latest Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable



RUN CHROME_VERSION=$(google-chrome-stable --version | grep -oP '(?<=Google Chrome )[^ ]+') && \
    CHROME_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROME_VERSION/linux64/chromedriver-linux64.zip && \
    wget -q $CHROME_URL && \
    unzip chromedriver-linux64.zip && \
    chmod +x chromedriver-linux64/chromedriver

COPY requirements.txt .
COPY app.py .
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

#ENV PORT=80
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT}"]
CMD uvicorn app:app --host 0.0.0.0 --port $PORT