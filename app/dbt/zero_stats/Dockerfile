FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir dbt-postgres

COPY app/dbt/zero_stats /app
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["run"]
