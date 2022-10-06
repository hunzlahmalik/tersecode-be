FROM python:slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/
ENV APP_HOME=/backend

RUN mkdir $APP_HOME && \
  mkdir $APP_HOME/staticfiles && \
  mkdir $APP_HOME/mediafiles && \
  pip install --no-cache-dir --upgrade pip

WORKDIR $APP_HOME

COPY ./requirements.txt ./entrypoint.sh ./
RUN sed -i 's/\r$//g' /backend/entrypoint.sh && \
  chmod +x /backend/entrypoint.sh && \
  apt-get update && \
  apt-get install -y netcat gcc && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt && \
  rm -rf /root/.cache/pip/*


COPY . .

ENTRYPOINT ["/backend/entrypoint.sh"]
EXPOSE 8000