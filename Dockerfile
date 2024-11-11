# # base image
# FROM python:3.12-slim

# # setup working directory in container
# WORKDIR /inventory_management_system

# # copy all files to inventory_management_system directory
# COPY . /inventory_management_system/

# RUN pip install poetry

# RUN poetry install

# # command to run on container start
# CMD ["poetry", "run", "python", "inventory_management_system/main.py"]
# base image
FROM python:3.12-slim

# setup working directory in container
WORKDIR /inventory_management_system

# copy all files to inventory_management_system directory
COPY . /inventory_management_system/

# Install curl and the dependencies for Poetry installation
RUN apt-get update && apt-get install -y curl

# Install Poetry using the official install script
RUN curl -sSL https://install.python-poetry.org | python3 -

# Ensure the Poetry binary is in the PATH
ENV PATH="$PATH:/root/.local/bin"

# Install project dependencies
RUN poetry install

# command to run on container start
CMD ["poetry", "run", "python", "inventory_management_system/main.py"]
