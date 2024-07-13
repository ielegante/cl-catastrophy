# Generate docker file
# Use the official Python image as a base
FROM --platform=linux/amd64 python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY ./docker-pkg /app

# # Expose port 5000 to the outside world
EXPOSE 8000

# # Run the Flask app when the container launches
# CMD ["flask", "run"]