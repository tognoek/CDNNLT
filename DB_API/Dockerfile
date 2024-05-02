FROM python
COPY . ./api
RUN pip install fastapi uvicorn mysql-connector-python pydantic
WORKDIR ./api
CMD ["uvicorn", "db_api:app", "--host", "0.0.0.0", "--port", "8000"]