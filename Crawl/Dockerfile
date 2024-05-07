FROM python
COPY . ./crawl
RUN pip install requests uvicorn fastapi configparser beautifulsoup4
WORKDIR ./crawl
CMD ["uvicorn", "crawl:app",  "--host", "0.0.0.0", "--port", "7080"]