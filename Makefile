# Get image tag from current git head
TAG := $(shell git rev-parse --short HEAD)
IMAGE = costrouc/dask-worker-cull

dask-worker-cull:
	docker build -t $(IMAGE):$(TAG) .
	docker push $(IMAGE):$(TAG)
