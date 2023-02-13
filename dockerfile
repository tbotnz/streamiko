FROM python:3.10
ADD . /code
WORKDIR /code
RUN python3 -m pip install -r /code/requirements.txt

CMD uvicorn streamiko:app --reload --port 9005 --host "0.0.0.0"