FROM us.gcr.io/platform-205701/harness/ubi8/python3:3.11

WORKDIR /project

ADD ./requirements.txt /project

USER root

RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

ADD . /project

CMD ["python", "main.py"]