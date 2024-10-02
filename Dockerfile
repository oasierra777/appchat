FROM python:3.8
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

copy . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]