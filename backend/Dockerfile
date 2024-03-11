FROM python:3.11-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED=1

WORKDIR /Paradiso/backend

# Install system dependencies
RUN apt update -y \
    && apt install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


# Copies the files & folders to the working directory
COPY . .

RUN pip install poetry

# Install dependencies using Poetry
# Avoid creating a virtual environment
RUN poetry config virtualenvs.create false && \ 
    poetry install --no-dev

# Set entrypoint script as executable
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["./entrypoint.sh"]

# Expose the port Django runs on
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]