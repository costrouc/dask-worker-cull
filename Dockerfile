FROM python:3.7-alpine

RUN pip install --no-cache-dir kubernetes

COPY dask-worker-cull.py /opt/dask-worker-cull.py

ENTRYPOINT ["python", "/opt/dask-worker-cull.py"]
