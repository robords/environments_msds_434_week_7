SHELL := /bin/bash
.PHONY: setup install lambda lambda_layer_pandas
# A phony target is one that is not really the name of a file; rather it is just a name for a recipe to be executed when you make an explicit request. There are two reasons to use a phony target: to 
# avoid a conflict with a file of the same name, and to improve performance.

all: setup

setup:
	python3 -m venv ~/.venv/environments
        # https://docs.python.org/3/library/venv.html#creating-virtual-environments

install:
	pip install -r requirements.txt

lambda:
	zip -r ./lambda_update_predictor/lambda_update_predictor.zip lambda_update_predictor
# for zsh, it's: rm -r -v ^(stations.csv|lambda_update_s3_data.zip|update_weather_data.py|requirements.txt)
