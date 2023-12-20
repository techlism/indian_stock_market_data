ARG PORT=443
# ADD LATEST PYTHON
FROM python
# ADD LATEST BROWSERS
FROM cypress/browsers
WORKDIR /app

RUN apt-get install -y chromedriver

COPY requirements.txt .

RUN apt-get update && apt-get install -y python3-pip
RUN pip install -r requirements.txt

COPY . .
#ENV PORT=80
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT}"]
CMD uvicorn app:app --host 0.0.0.0 --port $PORT