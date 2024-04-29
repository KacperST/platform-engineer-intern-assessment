# import python3.10 image
FROM python:3.10-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the setup file
COPY setup.py .

# Install dependencies for testing
RUN pip install -e .

# Copy the current directory contents into the container at /app
COPY . .

# Execute command
CMD ["python", "src/main.py"]

# Uncomment the following line to run the test
# ENTRYPOINT ["./entrypoint.sh"]