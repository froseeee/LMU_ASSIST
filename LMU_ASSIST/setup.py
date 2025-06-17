#!/usr/bin/env python3
"""
Setup script for LMU Assistant
Handles installation, dependency management, and environment setup
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Dict, Any

def get_system_info() -> Dict[str, str]:
    """Получение информации о системе"""
    return {
        'platform': platform.system(),
        'platform_release': platform.release(),
        'platform_version': platform.version(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'python_implementation': platform.python_implementation()
    }

def check_python_version() -> bool:
    """Проверка версии Python"""
    required_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]}+ required")
        print(f"   Current version: {current_version[0]}.{current_version[1]}")
        print(f"   Please upgrade Python: https://www.python.org/downloads/")
        return False
    
    print(f"✅ Python {current_version[0]}.{current_version[1]} OK")
    return True

def create_virtual_environment() -> bool:
    """Создание виртуального окружения"""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False

def get_pip_executable() -> str:
    """Получение пути к pip в виртуальном окружении"""
    system = platform.system()
    if system == "Windows":
        return str(Path("venv/Scripts/pip.exe"))
    else:
        return str(Path("venv/bin/pip"))

def install_dependencies() -> bool:
    """Установка зависимостей"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    pip_exe = get_pip_executable()
    
    try:
        print("📥 Installing dependencies...")
        subprocess.run([
            pip_exe, "install", "-r", "requirements.txt", "--upgrade"
        ], check=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def install_optional_dependencies() -> bool:
    """Установка опциональных зависимостей"""
    optional_packages = [
        "pyqtgraph>=0.12.0",  # Advanced plotting
        "pandas>=1.3.0",      # Data analysis
        "scikit-learn>=1.0.0", # Machine learning
        "psutil>=5.8.0"       # System monitoring
    ]
    
    pip_exe = get_pip_executable()
    installed_packages = []
    failed_packages = []
    
    for package in optional_packages:
        try:
            print(f"📥 Installing {package}...")
            subprocess.run([pip_exe, "install", package], check=True)
            installed_packages.append(package.split('>=')[0])
        except subprocess.CalledProcessError:
            failed_packages.append(package.split('>=')[0])
    
    if installed_packages:
        print(f"✅ Optional packages installed: {', '.join(installed_packages)}")
    
    if failed_packages:
        print(f"⚠️  Optional packages failed: {', '.join(failed_packages)}")
        print("   These packages provide enhanced features but are not required")
    
    return len(installed_packages) > 0

def create_directories() -> bool:
    """Создание необходимых директорий"""
    directories = ["config", "logs", "data", "assets", "models", "tests"]
    
    created = []
    failed = []
    
    for directory in directories:
        try:
            Path(directory).mkdir(exist_ok=True)
            created.append(directory)
        except Exception as e:
            failed.append(f"{directory} ({e})")
    
    if created:
        print(f"✅ Directories created: {', '.join(created)}")
    
    if failed:
        print(f"❌ Failed to create: {', '.join(failed)}")
        return False
    
    return True

def create_launch_scripts() -> bool:
    """Создание скриптов запуска"""
    system = platform.system()
    
    try:
        if system == "Windows":
            # Windows batch script
            batch_content = """@echo off
echo Starting LMU Assistant v2.0.1...
echo.

if not exist "venv" (
    echo Virtual environment not found!
    echo Please run setup.py first
    pause
    exit /b 1
)

call venv\\Scripts\\activate.bat
python main.py
pause
"""
            with open("run.bat", "w") as f:
                f.write(batch_content)
            
            print("✅ Created run.bat for Windows")
        
        else:
            # Unix shell script
            shell_content = """#!/bin/bash
echo "🏁 Starting LMU Assistant v2.0.1..."
echo

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.py first"
    exit 1
fi

source venv/bin/activate
python main.py
"""
            script_path = Path("run.sh")
            with open(script_path, "w") as f:
                f.write(shell_content)
            
            # Make executable
            os.chmod(script_path, 0o755)
            
            print("✅ Created run.sh for Unix/Linux")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create launch script: {e}")
        return False

def setup_data_files() -> bool:
    """Настройка файлов данных"""
    data_dir = Path("data")
    
    # Проверяем основной файл данных
    lmu_data_file = data_dir / "lmu_data.json"
    
    if lmu_data_file.exists():
        print("✅ LMU data file found")
        return True
    
    # Создаем минимальный файл данных если его нет
    try:
        minimal_data = {
            "cars": {
                "lmgt3_mclaren": {
                    "name": "McLaren 720S LMGT3 Evo",
                    "category": "LMGT3",
                    "power": 520,
                    "weight": 1300,
                    "drivetrain": "RWD",
                    "free_car": True
                }
            },
            "tracks": {
                "le_mans": {
                    "name": "Circuit de la Sarthe",
                    "length": 13.626,
                    "characteristics": ["very_fast", "long_straights"]
                }
            },
            "metadata": {
                "version": "2.0.1",
                "created_by": "setup.py",
                "note": "Minimal data file - update with full database"
            }
        }
        
        import json
        with open(lmu_data_file, 'w', encoding='utf-8') as f:
            json.dump(minimal_data, f, indent=2, ensure_ascii=False)
        
        print("✅ Created minimal LMU data file")
        print("   📝 Consider downloading the full database for complete features")
        return True
        
    except Exception as e:
        print(f"❌ Failed to create data file: {e}")
        return False

def run_post_install_tests() -> bool:
    """Запуск тестов после установки"""
    test_file = Path("test_installation.py")
    
    if not test_file.exists():
        print("⚠️  Installation test file not found")
        return True  # Не критично
    
    try:
        print("🧪 Running post-installation tests...")
        
        # Получаем путь к Python в виртуальном окружении
        system = platform.system()
        if system == "Windows":
            python_exe = str(Path("venv/Scripts/python.exe"))
        else:
            python_exe = str(Path("venv/bin/python"))
        
        result = subprocess.run([python_exe, "test_installation.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Installation tests passed")
            return True
        else:
            print("⚠️  Some installation tests failed")
            print("   Check test_installation.py output for details")
            return False
            
    except Exception as e:
        print(f"⚠️  Could not run installation tests: {e}")
        return False

def print_system_info():
    """Печать информации о системе"""
    print("\n🖥️  System Information:")
    info = get_system_info()
    
    for key, value in info.items():
        formatted_key = key.replace('_', ' ').title()
        print(f"   {formatted_key}: {value}")

def print_completion_message(success: bool):
    """Печать сообщения о завершении"""
    print("\n" + "="*60)
    
    if success:
        print("🎉 LMU Assistant Setup Completed Successfully!")
        print("\n📋 Next Steps:")
        print("   1. Activate virtual environment:")
        
        system = platform.system()
        if system == "Windows":
            print("      venv\\Scripts\\activate")
        else:
            print("      source venv/bin/activate")
        
        print("   2. Run the application:")
        print("      python main.py")
        print("   3. Or use the launch script:")
        
        if system == "Windows":
            print("      run.bat")
        else:
            print("      ./run.sh")
        
        print("\n🔧 Configuration:")
        print("   - Enable UDP telemetry in Le Mans Ultimate (port 20777)")
        print("   - Check README.md for detailed setup instructions")
        print("   - Visit the Setup Expert tab for car optimization")
        
    else:
        print("❌ LMU Assistant Setup Failed!")
        print("\n🔧 Troubleshooting:")
        print("   1. Check error messages above")
        print("   2. Ensure Python 3.8+ is installed")
        print("   3. Check internet connection for package downloads")
        print("   4. Run with administrator/sudo privileges if needed")
        print("   5. Check GitHub issues for known problems")
    
    print("="*60)

def main():
    """Основная функция установки"""
    print("🏁 LMU Assistant v2.0.1 Setup")
    print("="*40)
    
    # Печатаем информацию о системе
    print_system_info()
    
    success = True
    
    # Шаги установки
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Installing optional dependencies", install_optional_dependencies),
        ("Creating directories", create_directories),
        ("Setting up data files", setup_data_files),
        ("Creating launch scripts", create_launch_scripts),
        ("Running post-install tests", run_post_install_tests)
    ]
    
    print(f"\n📋 Installation Steps ({len(steps)} total):")
    
    for i, (step_name, step_func) in enumerate(steps, 1):
        print(f"\n[{i}/{len(steps)}] {step_name}...")
        
        try:
            step_success = step_func()
            if not step_success and step_name in ["Checking Python version", "Installing dependencies"]:
                # Критические шаги
                success = False
                break
            elif not step_success:
                # Некритические шаги - продолжаем
                print(f"   ⚠️  {step_name} completed with warnings")
                
        except Exception as e:
            print(f"   ❌ {step_name} failed: {e}")
            if step_name in ["Checking Python version", "Installing dependencies"]:
                success = False
                break
    
    # Печатаем результат
    print_completion_message(success)
    
    return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n💥 Unexpected error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
