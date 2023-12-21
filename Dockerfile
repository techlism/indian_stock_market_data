ARG PORT=443
# ADD LATEST PYTHON
FROM python
# ADD LATEST BROWSERS

WORKDIR /app
# RUN apt-get install -y appstream/xenial-backports
RUN apt-get update && apt-get install -y wget unzip gnupg

# Download and install the latest Google Chrome
RUN wget -q https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chrome-linux64.zip && \
    unzip chrome-linux64.zip && \
    chmod +x chrome-linux64/chrome



RUN CHROME_DRIVER_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip && \
    wget -q $CHROME_DRIVER_URL && \
    unzip chromedriver-linux64.zip && \
    chmod +x chromedriver-linux64/chromedriver

COPY requirements.txt .
COPY app.py .
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

#ENV PORT=80
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT}"]
CMD uvicorn app:app --host 0.0.0.0 --port $PORT