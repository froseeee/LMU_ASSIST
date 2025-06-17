#!/usr/bin/env python3
"""
Тест установки LMU Assistant v2.0.1
Проверяет все критические компоненты перед запуском
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Цвета для вывода
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def run_comprehensive_test() -> Dict[str, Any]:
    """Запуск комплексного теста всех систем"""
    print_colored(f"\n🚀 LMU Assistant v2.0.1 - Installation Test", Colors.PURPLE + Colors.BOLD)
    print_colored(f"Testing all critical components...\n", Colors.WHITE)
    
    # Список всех тестов
    tests = [
        ("Python Version", test_python_version),
        ("Critical Imports", test_critical_imports),
        ("Required Dependencies", test_required_dependencies),
        ("Optional Dependencies", test_optional_dependencies),
        ("Core Modules", test_core_modules),
        ("UI Modules", test_ui_modules),
        ("Directories", test_directories),
        ("Data Files", test_data_files),
        ("Configuration System", test_configuration_system),
        ("Database System", test_database_system),
        ("Telemetry System", test_telemetry_system),
        ("ML System", test_ml_system)
    ]
    
    results = {}
    critical_failures = []
    warnings = []
    
    # Выполняем все тесты
    for test_name, test_func in tests:
        try:
            success, details = test_func()
            results[test_name] = {
                'success': success,
                'details': details,
                'critical': test_name in ['Python Version', 'Critical Imports', 'Required Dependencies', 'Core Modules']
            }
            
            print_test_result(test_name, success, details)
            
            # Собираем критические ошибки
            if not success and results[test_name]['critical']:
                critical_failures.append(test_name)
            elif not success:
                warnings.append(test_name)
                
        except Exception as e:
            error_details = f"Test execution failed: {e}"
            results[test_name] = {
                'success': False,
                'details': error_details,
                'critical': True
            }
            print_test_result(test_name, False, error_details)
            critical_failures.append(test_name)
    
    return {
        'results': results,
        'critical_failures': critical_failures,
        'warnings': warnings,
        'overall_success': len(critical_failures) == 0
    }

def generate_installation_report(test_results: Dict[str, Any]) -> str:
    """Генерация отчета об установке"""
    report = []
    report.append("LMU Assistant v2.0.1 - Installation Report")
    report.append("=" * 50)
    report.append(f"Test Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Python: {sys.version}")
    report.append(f"Platform: {sys.platform}")
    report.append("")
    
    results = test_results['results']
    
    # Успешные тесты
    successful_tests = [name for name, result in results.items() if result['success']]
    if successful_tests:
        report.append("✅ PASSED TESTS:")
        for test_name in successful_tests:
            details = results[test_name]['details']
            report.append(f"  - {test_name}: {details}")
        report.append("")
    
    # Предупреждения
    if test_results['warnings']:
        report.append("⚠️  WARNINGS:")
        for test_name in test_results['warnings']:
            details = results[test_name]['details']
            report.append(f"  - {test_name}: {details}")
        report.append("")
    
    # Критические ошибки
    if test_results['critical_failures']:
        report.append("❌ CRITICAL FAILURES:")
        for test_name in test_results['critical_failures']:
            details = results[test_name]['details']
            report.append(f"  - {test_name}: {details}")
        report.append("")
    
    # Рекомендации
    report.append("💡 RECOMMENDATIONS:")
    
    if test_results['critical_failures']:
        report.append("  🔧 REQUIRED ACTIONS:")
        for failure in test_results['critical_failures']:
            if failure == "Python Version":
                report.append("     - Upgrade Python to version 3.8 or higher")
            elif failure == "Required Dependencies":
                report.append("     - Install missing packages: pip install -r requirements.txt")
            elif failure == "Core Modules":
                report.append("     - Check file integrity and permissions")
            else:
                report.append(f"     - Fix {failure} issue before running the application")
        report.append("")
    
    if test_results['warnings']:
        report.append("  📋 OPTIONAL IMPROVEMENTS:")
        for warning in test_results['warnings']:
            if warning == "Optional Dependencies":
                report.append("     - Install optional packages for enhanced features")
            elif warning == "UI Modules":
                report.append("     - Install PyQt5 for full GUI functionality")
            elif warning == "ML System":
                report.append("     - Install scikit-learn for machine learning features")
            else:
                report.append(f"     - Consider fixing {warning} for better experience")
        report.append("")
    
    if test_results['overall_success']:
        report.append("🎉 READY TO RUN:")
        report.append("     - All critical components are working")
        report.append("     - You can start the application with: python main.py")
        report.append("     - Check the documentation for usage instructions")
    else:
        report.append("🚫 NOT READY:")
        report.append("     - Fix critical issues before running the application")
        report.append("     - Refer to the troubleshooting section in README.md")
    
    return "\n".join(report)

def create_detailed_log(test_results: Dict[str, Any]):
    """Создание детального лога тестирования"""
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"installation_test_{int(time.time())}.log"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("LMU Assistant Installation Test Log\n")
            f.write("=" * 40 + "\n")
            f.write(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Python Version: {sys.version}\n")
            f.write(f"Platform: {sys.platform}\n")
            f.write(f"Working Directory: {os.getcwd()}\n")
            f.write("\n")
            
            for test_name, result in test_results['results'].items():
                f.write(f"Test: {test_name}\n")
                f.write(f"Status: {'PASS' if result['success'] else 'FAIL'}\n")
                f.write(f"Critical: {'Yes' if result['critical'] else 'No'}\n")
                f.write(f"Details: {result['details']}\n")
                f.write("-" * 30 + "\n")
            
            f.write(f"\nOverall Result: {'SUCCESS' if test_results['overall_success'] else 'FAILURE'}\n")
            f.write(f"Critical Failures: {len(test_results['critical_failures'])}\n")
            f.write(f"Warnings: {len(test_results['warnings'])}\n")
        
        print_colored(f"\n📄 Detailed log saved: {log_file}", Colors.BLUE)
        
    except Exception as e:
        print_colored(f"⚠️  Could not create log file: {e}", Colors.YELLOW)

def print_final_summary(test_results: Dict[str, Any]):
    """Печать финального резюме"""
    print_header("INSTALLATION TEST SUMMARY")
    
    total_tests = len(test_results['results'])
    passed_tests = sum(1 for result in test_results['results'].values() if result['success'])
    critical_failures = len(test_results['critical_failures'])
    warnings = len(test_results['warnings'])
    
    print_colored(f"📊 Test Statistics:", Colors.CYAN + Colors.BOLD)
    print_colored(f"   Total Tests: {total_tests}", Colors.WHITE)
    print_colored(f"   Passed: {passed_tests}", Colors.GREEN)
    print_colored(f"   Critical Failures: {critical_failures}", Colors.RED if critical_failures > 0 else Colors.GREEN)
    print_colored(f"   Warnings: {warnings}", Colors.YELLOW if warnings > 0 else Colors.GREEN)
    
    print_colored(f"\n🎯 Overall Status:", Colors.CYAN + Colors.BOLD)
    
    if test_results['overall_success']:
        print_colored("   ✅ INSTALLATION SUCCESSFUL!", Colors.GREEN + Colors.BOLD)
        print_colored("   🚀 Ready to run: python main.py", Colors.GREEN)
        
        if warnings > 0:
            print_colored(f"\n   💡 {warnings} optional feature(s) unavailable", Colors.YELLOW)
            print_colored("   📋 Check warnings above for enhancement suggestions", Colors.YELLOW)
            
    else:
        print_colored("   ❌ INSTALLATION FAILED!", Colors.RED + Colors.BOLD)
        print_colored(f"   🔧 {critical_failures} critical issue(s) need fixing", Colors.RED)
        print_colored("   📖 Check the installation guide in README.md", Colors.RED)
    
    print_colored(f"\n📚 Next Steps:", Colors.CYAN + Colors.BOLD)
    
    if test_results['overall_success']:
        next_steps = [
            "1. Run 'python main.py' to start the application",
            "2. Configure Le Mans Ultimate UDP telemetry (port 20777)",
            "3. Check the Setup Expert tab for car optimization",
            "4. Read the documentation for advanced features"
        ]
    else:
        next_steps = [
            "1. Fix critical issues listed above",
            "2. Install missing dependencies with 'pip install -r requirements.txt'",
            "3. Re-run this test: 'python test_installation.py'",
            "4. Check GitHub issues for known problems"
        ]
    
    for step in next_steps:
        print_colored(f"   {step}", Colors.WHITE)

def save_installation_report(test_results: Dict[str, Any]):
    """Сохранение отчета об установке"""
    try:
        report_content = generate_installation_report(test_results)
        
        # Сохраняем в файл
        report_file = Path("installation_report.txt")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print_colored(f"\n📋 Installation report saved: {report_file}", Colors.BLUE)
        
        return str(report_file)
        
    except Exception as e:
        print_colored(f"⚠️  Could not save installation report: {e}", Colors.YELLOW)
        return None

def check_common_issues() -> List[str]:
    """Проверка типичных проблем"""
    issues = []
    
    # Проверка прав доступа
    try:
        test_file = Path("test_write_permissions.tmp")
        test_file.write_text("test")
        test_file.unlink()
    except Exception:
        issues.append("Insufficient write permissions in current directory")
    
    # Проверка места на диске
    try:
        import shutil
        free_space = shutil.disk_usage('.').free
        if free_space < 100 * 1024 * 1024:  # 100MB
            issues.append(f"Low disk space: {free_space // (1024*1024)}MB free")
    except Exception:
        issues.append("Could not check disk space")
    
    # Проверка кодировки
    try:
        test_string = "Тест кодировки UTF-8"
        test_string.encode('utf-8')
    except Exception:
        issues.append("UTF-8 encoding issues detected")
    
    return issues

def main():
    """Основная функция теста установки"""
    try:
        # Проверяем общие проблемы
        common_issues = check_common_issues()
        if common_issues:
            print_colored("⚠️  Detected potential issues:", Colors.YELLOW)
            for issue in common_issues:
                print_colored(f"   - {issue}", Colors.YELLOW)
            print()
        
        # Запускаем основной тест
        test_results = run_comprehensive_test()
        
        # Создаем детальный лог
        create_detailed_log(test_results)
        
        # Сохраняем отчет
        save_installation_report(test_results)
        
        # Печатаем финальное резюме
        print_final_summary(test_results)
        
        # Возвращаем код выхода
        return 0 if test_results['overall_success'] else 1
        
    except KeyboardInterrupt:
        print_colored("\n\n❌ Test interrupted by user", Colors.RED)
        return 130
        
    except Exception as e:
        print_colored(f"\n\n💥 Unexpected error during testing: {e}", Colors.RED)
        print_colored("Please report this issue on GitHub with the full error trace", Colors.RED)
        
        # Печатаем stack trace для отладки
        import traceback
        print_colored("\nError details:", Colors.RED)
        traceback.print_exc()
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    
    # Финальное сообщение
    print_colored(f"\n{'='*60}", Colors.CYAN)
    if exit_code == 0:
        print_colored("🎉 Installation test completed successfully!", Colors.GREEN + Colors.BOLD)
        print_colored("Ready to run LMU Assistant!", Colors.GREEN)
    else:
        print_colored("❌ Installation test failed!", Colors.RED + Colors.BOLD)
        print_colored("Please fix the issues above before running the application.", Colors.RED)
    print_colored(f"{'='*60}", Colors.CYAN)
    
    sys.exit(exit_code) print_colored(text: str, color: str = Colors.WHITE):
    """Цветной вывод"""
    print(f"{color}{text}{Colors.END}")

def print_header(title: str):
    """Печать заголовка секции"""
    print_colored(f"\n{'='*60}", Colors.CYAN)
    print_colored(f"🧪 {title}", Colors.CYAN + Colors.BOLD)
    print_colored(f"{'='*60}", Colors.CYAN)

def print_test_result(test_name: str, success: bool, details: str = ""):
    """Печать результата теста"""
    icon = "✅" if success else "❌"
    color = Colors.GREEN if success else Colors.RED
    status = "PASSED" if success else "FAILED"
    
    print_colored(f"{icon} {test_name}: {status}", color)
    if details:
        print_colored(f"   → {details}", Colors.WHITE)

def test_python_version() -> Tuple[bool, str]:
    """Проверка версии Python"""
    version = sys.version_info
    required = (3, 8)
    
    success = version >= required
    details = f"Python {version.major}.{version.minor}.{version.micro}"
    
    if not success:
        details += f" (требуется >= {required[0]}.{required[1]})"
    
    return success, details

def test_critical_imports() -> Tuple[bool, str]:
    """Тестирование критических импортов"""
    critical_modules = [
        ('json', 'JSON support'),
        ('sqlite3', 'SQLite database'),
        ('threading', 'Threading support'),
        ('pathlib', 'Path handling'),
        ('logging', 'Logging system')
    ]
    
    failed_imports = []
    
    for module_name, description in critical_modules:
        try:
            __import__(module_name)
        except ImportError:
            failed_imports.append(f"{module_name} ({description})")
    
    success = len(failed_imports) == 0
    details = f"All critical modules available" if success else f"Missing: {', '.join(failed_imports)}"
    
    return success, details

def test_required_dependencies() -> Tuple[bool, str]:
    """Тестирование обязательных зависимостей"""
    required_packages = [
        ('PyQt5', 'GUI framework'),
        ('numpy', 'Numerical computing'),
        ('matplotlib', 'Plotting library')
    ]
    
    missing_packages = []
    available_packages = []
    
    for package_name, description in required_packages:
        try:
            __import__(package_name)
            available_packages.append(package_name)
        except ImportError:
            missing_packages.append(f"{package_name} ({description})")
    
    success = len(missing_packages) == 0
    
    if success:
        details = f"All required packages available: {', '.join(available_packages)}"
    else:
        details = f"Missing packages: {', '.join(missing_packages)}"
    
    return success, details

def test_optional_dependencies() -> Tuple[bool, str]:
    """Тестирование опциональных зависимостей"""
    optional_packages = [
        ('pyqtgraph', 'Advanced plotting'),
        ('pandas', 'Data analysis'),
        ('sklearn', 'Machine learning'),
        ('psutil', 'System monitoring')
    ]
    
    available_optional = []
    missing_optional = []
    
    for package_name, description in optional_packages:
        try:
            __import__(package_name)
            available_optional.append(package_name)
        except ImportError:
            missing_optional.append(f"{package_name} ({description})")
    
    # Опциональные пакеты не критичны для успеха
    success = True
    
    details = f"Available: {len(available_optional)}/{len(optional_packages)}"
    if missing_optional:
        details += f" | Missing: {', '.join(missing_optional)}"
    
    return success, details

def test_core_modules() -> Tuple[bool, str]:
    """Тестирование основных модулей приложения"""
    core_modules = [
        'core.constants',
        'core.config_manager', 
        'core.database',
        'core.telemetry_receiver',
        'core.setupexpert'
    ]
    
    # Добавляем путь к модулям
    sys.path.insert(0, str(Path(__file__).parent))
    
    failed_modules = []
    imported_modules = []
    
    for module_name in core_modules:
        try:
            __import__(module_name)
            imported_modules.append(module_name)
        except ImportError as e:
            failed_modules.append(f"{module_name} ({str(e)})")
        except Exception as e:
            failed_modules.append(f"{module_name} (Error: {str(e)})")
    
    success = len(failed_modules) == 0
    
    if success:
        details = f"All core modules imported successfully ({len(imported_modules)})"
    else:
        details = f"Failed modules: {', '.join(failed_modules)}"
    
    return success, details

def test_ui_modules() -> Tuple[bool, str]:
    """Тестирование UI модулей"""
    ui_modules = [
        'ui.garage',
        'ui.telemetry_tab',
        'ui.progress_tab',
        'ui.trainer_tab',
        'ui.encyclopedia'
    ]
    
    failed_modules = []
    imported_modules = []
    
    for module_name in ui_modules:
        try:
            __import__(module_name)
            imported_modules.append(module_name)
        except ImportError as e:
            failed_modules.append(f"{module_name} ({str(e)})")
        except Exception as e:
            failed_modules.append(f"{module_name} (Error: {str(e)})")
    
    # UI модули не критичны если PyQt5 недоступен
    success = len(failed_modules) == 0 or 'PyQt5' not in str(failed_modules)
    
    if success:
        details = f"UI modules OK ({len(imported_modules)} imported)"
        if failed_modules:
            details += f" | Some modules need PyQt5"
    else:
        details = f"UI modules failed: {', '.join(failed_modules)}"
    
    return success, details

def test_directories() -> Tuple[bool, str]:
    """Проверка необходимых директорий"""
    required_dirs = ["config", "logs", "data"]
    optional_dirs = ["assets", "models", "tests"]
    
    missing_required = []
    missing_optional = []
    created_dirs = []
    
    # Проверяем и создаем обязательные директории
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(dir_name)
            except Exception as e:
                missing_required.append(f"{dir_name} (Error: {e})")
    
    # Проверяем опциональные директории
    for dir_name in optional_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(dir_name)
            except Exception:
                missing_optional.append(dir_name)
    
    success = len(missing_required) == 0
    
    details = f"Required directories OK"
    if created_dirs:
        details += f" | Created: {', '.join(created_dirs)}"
    if missing_required:
        details += f" | Missing: {', '.join(missing_required)}"
    
    return success, details

def test_data_files() -> Tuple[bool, str]:
    """Проверка файлов данных"""
    data_files = {
        "data/lmu_data.json": "Car and track database",
        "requirements.txt": "Python dependencies"
    }
    
    missing_files = []
    valid_files = []
    
    for file_path, description in data_files.items():
        path = Path(file_path)
        if path.exists():
            try:
                if file_path.endswith('.json'):
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    # Проверяем структуру данных LMU
                    if 'cars' in data and 'tracks' in data:
                        valid_files.append(f"{file_path} ({len(data.get('cars', {}))} cars, {len(data.get('tracks', {}))} tracks)")
                    else:
                        valid_files.append(f"{file_path} (structure OK)")
                else:
                    valid_files.append(f"{file_path} ({description})")
                    
            except Exception as e:
                missing_files.append(f"{file_path} (Invalid: {e})")
        else:
            missing_files.append(f"{file_path} ({description})")
    
    # Не критично если некоторые файлы отсутствуют
    success = len(valid_files) > 0
    
    details = f"Data files found: {len(valid_files)}"
    if missing_files:
        details += f" | Missing: {len(missing_files)}"
    
    return success, details

def test_configuration_system() -> Tuple[bool, str]:
    """Тест системы конфигурации"""
    try:
        from core.config_manager import ConfigManager
        from core.constants import AppConstants
        
        # Создаем тестовый менеджер конфигурации
        config_manager = ConfigManager("test_config")
        
        # Тестируем основные операции
        main_config = config_manager.get_main_config()
        
        # Проверяем наличие ключевых полей
        required_fields = ['app_name', 'version', 'language']
        missing_fields = [field for field in required_fields if field not in main_config]
        
        if missing_fields:
            return False, f"Missing config fields: {', '.join(missing_fields)}"
        
        # Тестируем сохранение/загрузку
        test_setting = "test_value"
        config_manager.set_setting('main', 'test_field', test_setting)
        retrieved_value = config_manager.get_setting('main', 'test_field')
        
        if retrieved_value != test_setting:
            return False, "Config save/load test failed"
        
        # Очищаем тестовые файлы
        import shutil
        test_config_dir = Path("test_config")
        if test_config_dir.exists():
            shutil.rmtree(test_config_dir)
        
        return True, "Configuration system working correctly"
        
    except Exception as e:
        return False, f"Configuration test failed: {e}"

def test_database_system() -> Tuple[bool, str]:
    """Тест системы базы данных"""
    try:
        from core.database import DatabaseManager
        
        # Создаем тестовую базу данных в памяти
        db = DatabaseManager(":memory:")
        
        # Тестируем создание сессии
        session_id = db.save_session(
            track="test_track",
            car="test_car", 
            session_type="practice",
            data={"test": "data"}
        )
        
        if not isinstance(session_id, int) or session_id <= 0:
            return False, "Session creation failed"
        
        # Тестируем получение сессий
        sessions = db.get_sessions()
        if len(sessions) != 1:
            return False, "Session retrieval failed"
        
        # Тестируем сохранение круга
        lap_id = db.save_lap(
            session_id=session_id,
            lap_number=1,
            lap_time=90.5,
            sector_times=[30.0, 30.0, 30.5]
        )
        
        if not isinstance(lap_id, int) or lap_id <= 0:
            return False, "Lap creation failed"
        
        db.close()
        return True, "Database system working correctly"
        
    except Exception as e:
        return False, f"Database test failed: {e}"

def test_telemetry_system() -> Tuple[bool, str]:
    """Тест системы телеметрии"""
    try:
        from core.telemetry_receiver import TelemetryReceiver, TelemetryConfig
        
        # Создаем тестовый приемник с нестандартным портом
        config = TelemetryConfig(port=20778)  # Другой порт для теста
        receiver = TelemetryReceiver(config)
        
        # Проверяем инициализацию
        if not receiver.sock:
            return False, "Socket initialization failed"
        
        # Проверяем валидацию данных
        test_data = {
            'rpm': 5000,
            'speed': 150,
            'gear': 3,
            'throttle': 0.8,
            'brake': 0.0
        }
        
        is_valid = receiver._validate_telemetry_values(test_data)
        if not is_valid:
            return False, "Telemetry validation failed"
        
        receiver.stop_listening()
        return True, "Telemetry system initialized correctly"
        
    except Exception as e:
        return False, f"Telemetry test failed: {e}"

def test_ml_system() -> Tuple[bool, str]:
    """Тест системы машинного обучения"""
    try:
        # Проверяем доступность ML библиотек
        try:
            import sklearn
            import numpy as np
            ml_available = True
        except ImportError:
            ml_available = False
        
        if not ml_available:
            return True, "ML libraries not available (optional)"
        
        # Тестируем базовые операции ML
        from core.ml_engine import MLSetupOptimizer
        
        optimizer = MLSetupOptimizer(model_path=":memory:")
        
        # Тестируем предсказание с fallback
        track_conditions = {"temperature": 25, "characteristics": ["fast"]}
        driver_style = {"brake_smoothness": 0.8, "consistency": 0.85}
        
        prediction = optimizer.predict_optimal_setup(
            track_conditions=track_conditions,
            driver_style=driver_style,
            car_model="test_car"
        )
        
        if not prediction or not hasattr(prediction, 'predicted_setup'):
            return False, "ML prediction failed"
        
        return True, f"ML system working (confidence: {prediction.confidence:.2f})"
        
    except Exception as e:
        return False, f"ML test failed: {e}"

def
