FROM python:3.12

WORKDIR /serverSide

COPY ../. .

RUN pip install scipy
CMD ["python", "-m", "serverSide.server"]