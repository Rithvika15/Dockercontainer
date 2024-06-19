FROM python:3.12.3

WORKDIR /django

RUN apt-get update && apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Rust and Cargo
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

# Ensure Rust and Cargo are in the PATH
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY  . .

CMD python manage.py runserver 0.0.0.0:8000
