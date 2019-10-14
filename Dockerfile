FROM python:3.7

RUN pip install kubernetes

COPY dask-worker-cull.py /opt/dask-worker-cull.py

ENTRYPOINT ["python", "/opt/dask-worker-cull.py"]
