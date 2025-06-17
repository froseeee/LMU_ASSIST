#!/usr/bin/env python3
"""Тест установки LMU Assistant"""

import sys
from pathlib import Path

def test_imports():
    """Тестирование импортов"""
    print("🔍 Тестирование импортов...")
    
    try:
        from core.config_manager import ConfigManager
        print("✅ ConfigManager импортирован")
        
        from core.telemetry_receiver import TelemetryReceiver
        print("✅ TelemetryReceiver импортирован")
        
        from core.telemetry_buffer import TelemetryBuffer
        print("✅ TelemetryBuffer импортирован")
        
        from core.setupexpert import SetupExpert
        print("✅ SetupExpert импортирован")
        
        from overlay.overlay_hud import OverlayHUD
        print("✅ OverlayHUD импортирован")
        
        return True
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False

def test_data_files():
    """Проверка файлов данных"""
    print("\n📂 Проверка файлов данных...")
    
    data_file = Path("data/lmu_data.json")
    if data_file.exists():
        print("✅ data/lmu_data.json найден")
        try:
            import json
            with open(data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"✅ JSON валиден, найдено {len(data.get('cars', {}))} автомобилей и {len(data.get('tracks', {}))} трасс")
            return True
        except json.JSONDecodeError as e:
            print(f"❌ Ошибка в JSON: {e}")
            return False
    else:
        print("❌ data/lmu_data.json не найден")
        return False

def test_directories():
    """Проверка директорий"""
    print("\n📁 Проверка директорий...")
    
    dirs = ["config", "logs", "assets", "data"]
    all_ok = True
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ Директория {dir_name}/ существует")
        else:
            print(f"❌ Директория {dir_name}/ не найдена")
            all_ok = False
    
    return all_ok

def test_config():
    """Тест системы конфигурации"""
    print("\n⚙️ Тестирование конфигурации...")
    
    try:
        from core.config_manager import ConfigManager
        config = ConfigManager()
        
        # Проверяем создание файлов конфигурации
        config_files = [
            "config/main.json",
            "config/telemetry.json", 
            "config/ui.json",
            "config/overlay.json"
        ]
        
        all_ok = True
        for config_file in config_files:
            if Path(config_file).exists():
                print(f"✅ {config_file} создан")
            else:
                print(f"❌ {config_file} не создан")
                all_ok = False
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Ошибка конфигурации: {e}")
        return False

def test_expert_system():
    """Тест экспертной системы"""
    print("\n🧠 Тестирование экспертной системы...")
    
    try:
        from core.setupexpert import SetupExpert
        
        data_file = Path("data/lmu_data.json")
        expert = SetupExpert(str(data_file) if data_file.exists() else None)
        
        # Тест получения списков
        cars = expert.get_available_cars()
        tracks = expert.get_available_tracks()
        
        print(f"✅ Найдено {len(cars)} автомобилей")
        print(f"✅ Найдено {len(tracks)} трасс")
        
        # Тест рекомендаций
        conditions = {"temperature": 25, "track": "le_mans"}
        telemetry = {"brake_avg": 0.8, "balance": "neutral"}
        
        recommendations = expert.recommend_setup(conditions, telemetry, "hypercar", "le_mans")
        
        if "adjustments" in recommendations:
            print("✅ Система рекомендаций работает")
            return True
        else:
            print("❌ Система рекомендаций не работает")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка экспертной системы: {e}")
        return False

def main():
    """Основная функция теста"""
    print("🧪 LMU Assistant - Тест установки")
    print("=" * 50)
    
    tests = [
        ("Импорты", test_imports),
        ("Директории", test_directories), 
        ("Файлы данных", test_data_files),
        ("Конфигурация", test_config),
        ("Экспертная система", test_expert_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📋 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    
    all_passed = True
    for test_name, result in results:
        status = "✅ ПРОШЕЛ" if result else "❌ ПРОВАЛЕН"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ! LMU Assistant готов к использованию!")
        print("\n🚀 Запустите приложение командой: python main.py")
    else:
        print("⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ! Проверьте установку.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
