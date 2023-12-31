ARG PORT=443
# ADD LATEST PYTHON
FROM python
# ADD LATEST BROWSERS
WORKDIR /app
# RUN apt-get install -y appstream/xenial-backports
# RUN apt-get update && apt-get install -y wget unzip gnupg

# Install system dependencies
RUN apt-get update && apt-get install -y wget firefox-esr

# Install geckodriver (We are kinda automatically handling installation in code itself. So commenting out 👇)
# RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz && \
#     tar -xvzf geckodriver-v0.29.1-linux64.tar.gz && \
#     chmod +x geckodriver && \
#     mv geckodriver /usr/local/bin/ && \
#     rm geckodriver-v0.29.1-linux64.tar.gz

COPY requirements.txt .
COPY utils /app/utils
COPY app.py .
RUN apt-get install -y python3-pip
RUN pip install -r requirements.txt

CMD uvicorn app:app --host 0.0.0.0 --port $PORT