FROM ubuntu:20.04

# Оновлюємо Ubuntu та встановлюємо Ruby 3.0 та необхідні пакети
RUN apt-get update && apt-get install -y \
    ruby3.0 ruby3.0-dev build-essential

# Встановлюємо плагін для Elasticsearch
RUN gem install fluent-plugin-elasticsearch

# Встановлюємо Fluentd
RUN gem install fluentd

# Копіюємо конфігурацію Fluentd з папки fluentd/conf
COPY fluentd/conf/fluent.conf /fluentd/etc/fluent.conf

# Запускаємо Fluentd
CMD ["fluentd", "-c", "/fluentd/etc/fluent.conf"]

USER fluent
