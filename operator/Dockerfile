FROM python:3.9-slim
WORKDIR /app
RUN pip install kopf kubernetes
COPY operator.py .
CMD ["kopf", "run", "operator.py", "--namespace=drone-sim", "--verbose"]
