FROM python
COPY . ./api
RUN pip install fastapi uvicorn 
WORKDIR ./api
CMD ["uvicorn", "api_fake:app", "--host", "0.0.0.0", "--port", "8020"]