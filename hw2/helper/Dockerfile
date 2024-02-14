# Docker-команда FROM вказує базовий образ контейнера
# Наш базовий образ - це Linux з попередньо встановленим python-3.10
FROM python:3.11.5

# Встановимо робочу директорію всередині контейнера
WORKDIR /app

# Скопіюємо інші файли в робочу директорію контейнера
COPY helper/main.py /app/
COPY helper/notes.py /app/
COPY helper/classes.py /app/
COPY helper/sorter.py /app/
COPY requirements.txt /app/

# Встановимо залежності всередині контейнера
RUN pip3 install -r requirements.txt

# Позначимо порт, де працює застосунок всередині контейнера
# EXPOSE 8080

# Запустимо наш застосунок всередині контейнера
CMD ["python3", "main.py"]