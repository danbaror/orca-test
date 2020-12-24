FROM python:3.8
WORKDIR /app
COPY . /app
RUN pip install pipenv && pip install psycopg2
RUN pipenv lock --requirements > requirements.txt && pip install -r requirements.txt
# RUN pip install gunicorn
ENV DATABASE_URL postgresql://postgres:pg234x@localhost:5432/postgres
# CMD ["gunicorn", "--workers=1", "--bind=0.0.0.0:8000", "app:app"]
ENTRYPOINT ["./run_app.sh"] 
