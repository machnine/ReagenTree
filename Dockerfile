# python image
FROM python:3.12-slim

# set work directory
WORKDIR /app

# install dependencies
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

# Copy entrypoint script
COPY entrypoint.sh entrypoint.sh

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]