

FROM python:3.10.12

# Set the working directory
WORKDIR /src

# Install required packages (nano, vim, and vi) and clean up afterward
RUN apt-get update && \
    apt-get install -y nano vim-tiny && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file first and install dependencies
COPY requirement.txt requirement.txt
RUN pip install -r requirement.txt

# Copy the application code after installing dependencies (to optimize caching)
COPY ./src /src

# Change ownership of the /src directory
RUN chown 1000:1000 /src

# Switch to non-root user
USER 1000:1000

# Set environment variables
ENV HOME=/src
