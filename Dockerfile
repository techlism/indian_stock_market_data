ARG PORT=443
# ADD LATEST PYTHON
FROM python
# ADD LATEST BROWSERS
WORKDIR /app
# RUN apt-get install -y appstream/xenial-backports
# RUN apt-get update && apt-get install -y wget unzip gnupg

# Install system dependencies
RUN apt-get update && apt-get install -y wget firefox-esr

# Install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz && \
    tar -xvzf geckodriver-v0.29.1-linux64.tar.gz && \
    chmod +x geckodriver && \
    mv geckodriver /usr/local/bin/ && \
    rm geckodriver-v0.29.1-linux64.tar.gz

# RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 libexpat1 libfontconfig1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 ca-certificates fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils chromium libvulkan1



# # Download and install the latest Google Chrome
# RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
#     dpkg -i google-chrome-stable_current_amd64.deb && \
#     rm google-chrome-stable_current_amd64.deb



# RUN CHROME_DRIVER_URL=https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip && \
#     wget -q $CHROME_DRIVER_URL && \
#     unzip chromedriver-linux64.zip && \
#     chmod +x chromedriver-linux64/chromedriver

COPY requirements.txt .
COPY app.py .
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

CMD uvicorn app:app --host 0.0.0.0 --port $PORT