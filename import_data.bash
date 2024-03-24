#!/bin/bash
unzip ./input_data/russiannames_db_bson.zip -d ./input_data/unpacked
docker exec -it names_db mongorestore /input_data/unpacked/dump
