#Inscructions to build the docker image

FROM python:3.14.6

WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]