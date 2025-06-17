#!/bin/bash
# Запуск LMU Assistant v2.0

echo "🏁 Запуск LMU Assistant v2.0..."

# Проверка виртуального окружения
if [ -d "venv" ]; then
    echo "📦 Активация виртуального окружения..."
    source venv/bin/activate
fi

# Проверка зависимостей
echo "🔍 Проверка зависимостей..."
pip install -r requirements.txt --quiet

# Создание необходимых директорий
mkdir -p config logs assets data

# Проверка файла данных
if [ ! -f "data/lmu_data.json" ]; then
    echo "⚠️  Внимание: Файл data/lmu_data.json не найден!"
    echo "Создайте файл с данными автомобилей и трасс"
fi

# Установка прав на выполнение
chmod +x run.sh

# Запуск приложения
echo "🚀 Запуск приложения..."
python3 main.py

echo "👋 LMU Assistant завершен"
