ARG PORT=443
# ADD LATEST PYTHON
FROM python:latest
# ADD LATEST BROWSERS
FROM cypress/browsers:latest
WORKDIR /app



COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .
#ENV PORT=80
#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT}"]
CMD uvicorn app:app --host 0.0.0.0 --port $PORT