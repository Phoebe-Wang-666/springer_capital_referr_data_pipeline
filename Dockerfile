# 1. base image
FROM python:3.11-slim

# 2. set working directory
WORKDIR /app

# 3. copy project files
COPY . /app

# 4. install dependencies
RUN pip install --no-cache-dir pandas

# 5. run the pipeline
CMD ["sh", "-c", "python src/profiling.py && python src/preprocess.py && python src/business_logic.py"]

