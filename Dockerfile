FROM python:3.12-slim-bookworm
EXPOSE 8000
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/src/venv/bin:$PATH"
WORKDIR /usr/src/app
RUN python -m venv /usr/src/venv
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app"]
COPY . .
