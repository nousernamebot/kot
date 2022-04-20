FROM python:3.9.7
COPY ./pytransform ./pytransform
COPY ./main.py ./main.py
COPY ./schema.json ./schema.json
COPY ./settings.cfg ./settings.cfg
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
CMD [ "python", "main.py" ]