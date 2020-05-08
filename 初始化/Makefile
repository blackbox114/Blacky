# Files to copy to sd: cmdline.txt pi-init2 appliance

SHELL = /bin/bash
GOPATH=$(shell pwd)
GOOS=linux
GOARCH=arm
GOARM=6

all : src/projects.bytemark.co.uk/pi-init2
	@GOPATH=$(GOPATH) GOOS=$(GOOS) GOARCH=$(GOARCH) GOARM=$(GOARM) go build -o pi-init2 projects.bytemark.co.uk/pi-init2

