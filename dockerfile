# Use a slim version of Python 3.10 as the base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the current directory into the container's working directory
COPY ./ /app

# Install all dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable for Hugging Face cache (optional but recommended)
ENV HF_HOME=/tmp/huggingface_cache

# Create the cache directory and make sure it's writable
RUN mkdir -p /tmp/huggingface_cache && chmod -R 777 /tmp/huggingface_cache

# Expose the port the app will run on (7860 in this case)
EXPOSE 7860

# Command to run the FastAPI app with uvicorn (make sure your app is in main.py)
CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=7860", "--log-level", "error"]