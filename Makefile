HASH := $(shell git rev-parse --short HEAD)
CONTAINER := gcr.io/messaging-trioptima/messaging
TEST_CONTAINER := messaging

default: run

run:
	gunicorn 'app:get_app()' -b 0.0.0.0:8080 --access-logfile '-' 

build-image:
	docker build . -t $(CONTAINER):$(HASH)
	docker push $(CONTAINER):$(HASH)

push-image:
	docker tag $(CONTAINER):$(HASH) $(CONTAINER):latest
	docker push $(CONTAINER):latest
