#!/bin/bash

set DATA_FOLDER="C:\path\to\data\folder"
set DESTINATION_FOLDER="C:\path\to\output\folder"

docker run -it ^
    --mount type=bind,source=%DATA_FOLDER%,target=/Arkansas/data/ ^
    --mount type=bind,source=%DESTINATION_FOLDER%,target=/Arkansas/output_folder/ ^
    arkansas/data_processing:0.1
