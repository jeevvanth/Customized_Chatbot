# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app1

# Copy the current directory contents into the container
COPY . /app1

# Install dependencies
RUN pip install --upgrade pip \
     && pip install gradio requests

# Expose the port Gradio uses
EXPOSE 7860

# Command to run the app (assuming your script is called app.py)
CMD ["python", "gradio_chatbot.py"]
