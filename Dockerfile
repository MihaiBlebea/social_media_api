FROM python:3

# ENV VIRTUAL_ENV=./app/virtualenv

WORKDIR /app

RUN python -m venv virtualenv

# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .

RUN ./virtualenv/bin/pip3 install --upgrade pip

RUN ./virtualenv/bin/pip3 install -r requirements.txt

EXPOSE 5000

COPY . .

RUN chmod +x ./execute.sh

CMD ["./execute.sh", "api"]