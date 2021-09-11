FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Install Pipenv
RUN pip install --upgrade pip \
    && pip install pipenv

# define the directory to work in
WORKDIR /app

# Copy poetry.lock* in case it dosn't exist in the repo
COPY Pipfile* ./

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

COPY . /app
ENV PYTHONPATH=/app

CMD ["pipenv", "run", "uvicorn", "manage_products.main:api", "--host", "0.0.0.0", "--port", "8003", "--reload"]