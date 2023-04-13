#!/bin/bash

DATA_FOLDER=/path/to/data/folder/
DESTINATION_FOLDER=/path/to/output_folder/

docker run -it \
 --mount type=bind,source=$DATA_FOLDER,target=/Arkansas/data/ \
 --mount type=bind,source=$DESTINATION_FOLDER,target=/Arkansas/output_folder/ \
 arkansas/data_processing:0.1
