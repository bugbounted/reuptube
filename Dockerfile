# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Install Python 3 and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Install necessary Python packages
RUN pip3 install playwright selenium

# Copy the Python script to the container
COPY main.py /app/

# Set up cron job to run the Python script every hour
RUN echo "0 * * * * /usr/bin/python3 /app/main.py" > /etc/cron.d/my-cron
RUN chmod 0644 /etc/cron.d/my-cron
RUN crontab /etc/cron.d/my-cron

# Start cron in the foreground
CMD ["cron", "-f"]
