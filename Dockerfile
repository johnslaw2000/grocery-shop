# Start from an official Python image — a known-good environment
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first, then install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app code into the image
COPY . .

# Document which port the app uses
EXPOSE 5000

# The command that runs when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
