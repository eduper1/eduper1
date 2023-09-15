FROM python:3
COPY .  /usr/src/network
WORKDIR /usr/src/network
RUN pip install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
