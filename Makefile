## Copyright (c) 2015-2019
## Mainflux
##
## SPDX-License-Identifier: Apache-2.0

BUILD_DIR = build
SERVICES = users things http normalizer ws lora influxdb-writer influxdb-reader cli bootstrap
DOCKERS = $(addprefix docker_,$(SERVICES))
DOCKERS_DEV = $(addprefix docker_dev_,$(SERVICES))
CGO_ENABLED ?= 0
GOOS ?= linux

define compile_service
	CGO_ENABLED=$(CGO_ENABLED) GOOS=$(GOOS) GOARCH=$(GOARCH) GOARM=$(GOARM) go build -ldflags "-s -w" -o ${BUILD_DIR}/mainflux-$(1) cmd/$(1)/main.go
endef

define make_docker
	docker build --no-cache --build-arg SVC_NAME=$(subst docker_,,$(1)) --tag=rkrikbaev/$(subst docker_,,$(1)) -f docker/Dockerfile .
endef

define make_docker_dev
	docker build --build-arg SVC_NAME=$(subst docker_dev_,,$(1)) --tag=rkrikbaev/$(subst docker_dev_,,$(1)) -f docker/Dockerfile.dev ./build
endef

all: $(SERVICES) mqtt

.PHONY: all $(SERVICES) dockers dockers_dev latest release mqtt

clean:
	rm -rf ${BUILD_DIR}
	rm -rf mqtt/node_modules

cleandocker: cleanghost
	# Stop all containers (if running)
	docker-compose -f docker/docker-compose.yml stop
	# Remove mainflux containers
	docker ps -f name=mainflux -aq | xargs -r docker rm
	# Remove old mainflux images
	docker images -q mainflux\/* | xargs -r docker rmi

# Clean ghost docker images
cleanghost:
	# Remove exited containers
	docker ps -f status=dead -f status=exited -aq | xargs -r docker rm -v
	# Remove unused images
	docker images -f dangling=true -q | xargs -r docker rmi
	# Remove unused volumes
	docker volume ls -f dangling=true -q | xargs -r docker volume rm

install:
	cp ${BUILD_DIR}/* $(GOBIN)

test:
	go test -v -race -count 1 -tags test $(shell go list ./... | grep -v 'vendor\|cmd')

proto:
	protoc --gofast_out=plugins=grpc:. *.proto

$(SERVICES):
	$(call compile_service,$(@))

$(DOCKERS):
	$(call make_docker,$(@))

#docker_ui:
#	$(MAKE) -C ui docker

docker_mqtt:
	# MQTT Docker build must be done from root dir because it copies .proto files
	docker build --tag=rkrikbaev/mqtt -f mqtt/Dockerfile .

dockers: $(DOCKERS) docker_mqtt 
# docker_ui

$(DOCKERS_DEV):
	$(call make_docker_dev,$(@))

dockers_dev: $(DOCKERS_DEV)

#ui:
#	$(MAKE) -C ui

mqtt:
	cd mqtt && npm install

define docker_push
	for svc in $(SERVICES); do \
		docker push rkrikbaev/$$svc:$(1); \
	done
#	docker push rkrikbaev/ui:$(1)
	docker push rkrikbaev/mqtt:$(1)
endef

changelog:
	git log $(shell git describe --tags --abbrev=0)..HEAD --pretty=format:"- %s"

latest: dockers
	$(call docker_push,latest)

release:
	$(eval version = $(shell git describe --abbrev=0 --tags))
	git checkout $(version)
	$(MAKE) dockers
	for svc in $(SERVICES); do \
		docker tag rkrikbaev/$$svc rkrikbaev/$$svc:$(version); \
	done
#	docker tag rkrikbaev/ui rkrikbaev/ui:$(version)
	docker tag rkrikbaev/mqtt rkrikbaev/mqtt:$(version)
	$(call docker_push,$(version))

rundev:
	cd scripts && ./run.sh

run:
	docker-compose -f docker/docker-compose.yml up
restart:
	docker-compose -f docker/docker-compose.yml down
	docker-compose -f docker/docker-compose.yml up
#runui:
#	$(MAKE) -C ui run

runlora:
	docker-compose -f docker/docker-compose.yml up -d
	docker-compose -f docker/addons/influxdb-writer/docker-compose.yml up -d
	docker-compose -f docker/addons/lora-adapter/docker-compose.yml up
