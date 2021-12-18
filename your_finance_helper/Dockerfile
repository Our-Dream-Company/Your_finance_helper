FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/app

COPY requirements.txt .
COPY entrypoint.sh .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . .

RUN chmod +x /usr/src/app/entrypoint.sh
ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]