# syntax=docker/dockerfile:1
FROM python:3.9

# set the working directory in the container
WORKDIR /Arkansas

# update pip
RUN pip install --upgrade pip

# copy the dependencies file to the working directory
COPY requirements.txt .
COPY ./src ./src
# install dependencies
RUN pip install -r requirements.txt

# create folders inside container, those folder will be mounted from the host at runtime
RUN mkdir data
RUN mkdir output_folder

CMD [ "python", "./src/process_futures_data.py", "./data/crypto_hourly_data.csv", "./output_folder"]