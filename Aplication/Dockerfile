FROM python:3.12

WORKDIR /clientSide

COPY ../. .

RUN pip install keyboard
RUN pip install scipy
CMD ["python", "-m", "clientSide.interface_grafica"]