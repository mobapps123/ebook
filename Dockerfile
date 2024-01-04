FROM python:3.10
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install build dependencies
RUN apt-get update && apt-get install -y tzdata libpython3-dev gcc

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools
RUN pip install import_export
# Copy requirements and install dependencies
COPY requirements.txt .
# RUN pip install poetry
# RUN pip install django_cleanup

RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

EXPOSE 8004
CMD ["python", "manage.py", "runserver", "0.0.0.0:8004"]
