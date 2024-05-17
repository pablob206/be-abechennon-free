FROM python:3.12-slim as venv

RUN apt-get update && apt-get -y install git && \
    mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> /root/.ssh/known_hosts

COPY requirements.txt requirements.txt
RUN --mount=type=ssh python -m pip install --upgrade pip \
    pip install --no-cache-dir -r requirements.txt -t /packages/

FROM python:3.12-slim as app
WORKDIR /app/
ENV PATH /packages/bin:$PATH
ENV PYTHONPATH /packages

COPY --chmod=0744 ./deploy /
COPY --from=venv /packages /packages
COPY main.py /app/main.py
COPY ./app /app/app

EXPOSE 80
CMD /start.sh
