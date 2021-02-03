FROM python:3.7.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_SETTINGS=${APP_SETTINGS}
ENV DATABASE_URL=${DATABASE_URL}

CMD [ "python", "app.py" ]

EXPOSE 5000
