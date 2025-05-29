#Python image
FROM python:3.9-slim

#Env Var
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#create dir
WORKDIR /app

#Copy files
COPY . /app/

#Install dep
RUN pip install --upgrade pip && \
    pip install -r reqs.txt

#Port
EXPOSE 5000

#Run app
CMD ["python", "run.py"]
