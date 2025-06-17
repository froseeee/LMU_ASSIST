from PyQt5 import QtWidgets, QtCore, QtGui
from core.trainer_engine import TrainerEngine, LapAnalysis
import json

class TrainerTab(QtWidgets.QWidget):
    """Улучшенная вкладка тренера с детальным анализом"""
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.trainer = TrainerEngine()
        self.current_analysis = None
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        
        # Левая панель - управление
        left_panel = self.create_control_panel()
        layout.addWidget(left_panel)
        
        # Центральная панель - анализ
        center_panel = self.create_analysis_panel()
        layout.addWidget(center_panel, 2)
        
        # Правая панель - рекомендации
        right_panel = self.create_recommendations_panel()
        layout.addWidget(right_panel)
    
    def create_control_panel(self):
        """Создание панели управления"""
        panel = QtWidgets.QGroupBox("🎯 Управление анализом")
        panel.setMaximumWidth(300)
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin: 5px;
                padding-top: 15px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(panel)
        
        # Загрузка данных круга
        load_label = QtWidgets.QLabel("Данные круга:")
        load_label.setStyleSheet("font-weight: bold; color: #cccccc;")
        layout.addWidget(load_label)
        
        load_buttons_layout = QtWidgets.QHBoxLayout()
        
        self.load_telemetry_btn = QtWidgets.QPushButton("📁 Загрузить телеметрию")
        self.load_reference_btn = QtWidgets.QPushButton("⭐ Загрузить эталон")
        
        button_style = """
            QPushButton {
                background-color: #4a4a4a;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 6px;
                color: #ffffff;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #0078d4;
            }
        """
        
        self.load_telemetry_btn.setStyleSheet(button_style)
        self.load_reference_btn.setStyleSheet(button_style)
        
        load_buttons_layout.addWidget(self.load_telemetry_btn)
        load_buttons_layout.addWidget(self.load_reference_btn)
        layout.addLayout(load_buttons_layout)
        
        # Текущие данные
        current_data_label = QtWidgets.QLabel("Текущие данные:")
        current_data_label.setStyleSheet("font-weight: bold; color: #cccccc; margin-top: 10px;")
        layout.addWidget(current_data_label)
        
        self.current_data_info = QtWidgets.QTextBrowser()
        self.current_data_info.setMaximumHeight(150)
        self.current_data_info.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
                padding: 5px;
            }
        """)
        self.current_data_info.setHtml("""
            <p style="color: #cccccc;">Нет загруженных данных</p>
            <p><small>Загрузите телеметрию для анализа</small></p>
        """)
        layout.addWidget(self.current_data_info)
        
        # Тип анализа
        analysis_label = QtWidgets.QLabel("Тип анализа:")
        analysis_label.setStyleSheet("font-weight: bold; color: #cccccc; margin-top: 10px;")
        layout.addWidget(analysis_label)
        
        self.analysis_type = QtWidgets.QComboBox()
        self.analysis_type.setStyleSheet("""
            QComboBox {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 5px;
                color: #ffffff;
            }
        """)
        
        analysis_types = [
            "Полный анализ круга",
            "Анализ техники торможения",
            "Анализ техники ускорения",
            "Анализ консистентности",
            "Сравнение с эталоном"
        ]
        
        for analysis_type in analysis_types:
            self.analysis_type.addItem(analysis_type)
        
        layout.addWidget(self.analysis_type)
        
        # Кнопки анализа
        analysis_buttons_layout = QtWidgets.QVBoxLayout()
        
        self.analyze_btn = QtWidgets.QPushButton("🔍 Анализировать")
        self.analyze_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                border: none;
                border-radius: 4px;
                padding: 10px;
                color: #ffffff;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
        """)
        
        self.generate_plan_btn = QtWidgets.QPushButton("📋 План тренировок")
        self.save_analysis_btn = QtWidgets.QPushButton("💾 Сохранить анализ")
        
        for btn in [self.generate_plan_btn, self.save_analysis_btn]:
            btn.setStyleSheet(button_style)
        
        analysis_buttons_layout.addWidget(self.analyze_btn)
        analysis_buttons_layout.addWidget(self.generate_plan_btn)
        analysis_buttons_layout.addWidget(self.save_analysis_btn)
        
        layout.addLayout(analysis_buttons_layout)
        
        # Подключаем сигналы
        self.load_telemetry_btn.clicked.connect(self.load_telemetry)
        self.load_reference_btn.clicked.connect(self.load_reference)
        self.analyze_btn.clicked.connect(self.run_analysis)
        self.generate_plan_btn.clicked.connect(self.generate_training_plan)
        self.save_analysis_btn.clicked.connect(self.save_analysis)
        
        layout.addStretch()
        return panel
    
    def create_analysis_panel(self):
        """Создание панели анализа"""
        panel = QtWidgets.QGroupBox("📊 Результаты анализа")
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin: 5px;
                padding-top: 15px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(panel)
        
        # Создаем вкладки для разных видов анализа
        self.analysis_tabs = QtWidgets.QTabWidget()
        self.analysis_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #555555;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #4a4a4a;
                color: #ffffff;
                padding: 8px 12px;
                margin: 1px;
                border-radius: 3px;
            }
            QTabBar::tab:selected {
                background-color: #0078d4;
            }
        """)
        
        # Вкладка основного анализа
        self.main_analysis = QtWidgets.QTextBrowser()
        self.main_analysis.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
                padding: 15px;
            }
        """)
        self.main_analysis.setHtml("""
            <h2 style="color: #0078d4;">🏁 Добро пожаловать в тренер!</h2>
            <p>Загрузите данные телеметрии для получения детального анализа вашего стиля вождения.</p>
            
            <h3 style="color: #ffa500;">Возможности анализа:</h3>
            <ul>
                <li><b>Анализ времени круга</b> - сравнение с эталоном по секторам</li>
                <li><b>Техника торможения</b> - плавность и эффективность</li>
                <li><b>Техника ускорения</b> - точки открытия газа</li>
                <li><b>Рулежка</b> - плавность и точность</li>
                <li><b>Консистентность</b> - стабильность времен</li>
            </ul>
            
            <h3 style="color: #ffa500;">Поддерживаемые форматы:</h3>
            <ul>
                <li>JSON файлы телеметрии</li>
                <li>CSV файлы с данными кругов</li>
                <li>Файлы симуляторов (LMU, ACC, F1)</li>
            </ul>
        """)
        self.analysis_tabs.addTab(self.main_analysis, "📈 Основной анализ")
        
        # Вкладка детального анализа
        self.detailed_analysis = QtWidgets.QTextBrowser()
        self.detailed_analysis.setStyleSheet(self.main_analysis.styleSheet())
        self.detailed_analysis.setHtml("<p>Детальный анализ появится после обработки данных.</p>")
        self.analysis_tabs.addTab(self.detailed_analysis, "🔍 Детальный анализ")
        
        # Вкладка сравнения
        self.comparison_analysis = QtWidgets.QTextBrowser()
        self.comparison_analysis.setStyleSheet(self.main_analysis.styleSheet())
        self.comparison_analysis.setHtml("<p>Сравнение с эталоном появится после загрузки эталонного круга.</p>")
        self.analysis_tabs.addTab(self.comparison_analysis, "⚖️ Сравнение")
        
        layout.addWidget(self.analysis_tabs)
        return panel
    
    def create_recommendations_panel(self):
        """Создание панели рекомендаций"""
        panel = QtWidgets.QGroupBox("💡 Рекомендации и план")
        panel.setMaximumWidth(350)
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #555555;
                border-radius: 5px;
                margin: 5px;
                padding-top: 15px;
                color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #0078d4;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(panel)
        
        # Быстрые рекомендации
        quick_recs_label = QtWidgets.QLabel("⚡ Быстрые советы:")
        quick_recs_label.setStyleSheet("font-weight: bold; color: #ffa500;")
        layout.addWidget(quick_recs_label)
        
        self.quick_recommendations = QtWidgets.QTextBrowser()
        self.quick_recommendations.setMaximumHeight(200)
        self.quick_recommendations.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
                padding: 10px;
            }
        """)
        self.quick_recommendations.setHtml("""
            <ul>
                <li>Загрузите данные для получения персональных советов</li>
                <li>Сравните с эталонным кругом</li>
                <li>Сосредоточьтесь на консистентности</li>
                <li>Анализируйте каждый сектор отдельно</li>
            </ul>
        """)
        layout.addWidget(self.quick_recommendations)
        
        # План тренировок
        training_plan_label = QtWidgets.QLabel("📋 План тренировок:")
        training_plan_label.setStyleSheet("font-weight: bold; color: #ffa500; margin-top: 10px;")
        layout.addWidget(training_plan_label)
        
        self.training_plan = QtWidgets.QTextBrowser()
        self.training_plan.setStyleSheet("""
            QTextBrowser {
                background-color: #2b2b2b;
                border: 1px solid #555555;
                border-radius: 4px;
                color: #ffffff;
                padding: 10px;
            }
        """)
        self.training_plan.setHtml("""
            <p>План тренировок будет сгенерирован на основе анализа ваших данных.</p>
            <p><small>Нажмите 'План тренировок' после анализа</small></p>
        """)
        layout.addWidget(self.training_plan)
        
        return panel
    
    def load_telemetry(self):
        """Загрузка файла телеметрии"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Загрузить телеметрию", "", 
            "JSON files (*.json);;CSV files (*.csv);;All files (*)"
        )
        
        if file_path:
            try:
                # Пробуем загрузить как JSON
                with open(file_path, 'r', encoding='utf-8') as f:
                    if file_path.endswith('.json'):
                        self.current_telemetry = json.load(f)
                    else:
                        # Простая загрузка CSV (можно расширить)
                        import csv
                        reader = csv.DictReader(f)
                        self.current_telemetry = list(reader)
                
                # Обновляем информацию
                self.update_current_data_info()
                
                QtWidgets.QMessageBox.information(self, "Успех", "Телеметрия загружена!")
                
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файл: {e}")
    
    def load_reference(self):
        """Загрузка эталонного круга"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Загрузить эталон", "",
            "JSON files (*.json);;CSV files (*.csv);;All files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    if file_path.endswith('.json'):
                        self.reference_lap = json.load(f)
                    else:
                        import csv
                        reader = csv.DictReader(f)
                        self.reference_lap = list(reader)[0]  # Берем первую строку
                
                QtWidgets.QMessageBox.information(self, "Успех", "Эталон загружен!")
                
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить эталон: {e}")
    
    def update_current_data_info(self):
        """Обновление информации о текущих данных"""
        if hasattr(self, 'current_telemetry') and self.current_telemetry:
            if isinstance(self.current_telemetry, dict):
                # JSON формат
                lap_time = self.current_telemetry.get('lap_time', 'N/A')
                sectors = self.current_telemetry.get('sector_times', [])
                
                info_html = f"""
                <h4 style="color: #0078d4;">Загруженные данные:</h4>
                <p><b>Время круга:</b> {lap_time}</p>
                <p><b>Секторы:</b> {len(sectors)}</p>
                """
                
                if 'track' in self.current_telemetry:
                    info_html += f"<p><b>Трасса:</b> {self.current_telemetry['track']}</p>"
                if 'car' in self.current_telemetry:
                    info_html += f"<p><b>Автомобиль:</b> {self.current_telemetry['car']}</p>"
                
            else:
                # CSV формат или список
                info_html = f"""
                <h4 style="color: #0078d4;">Загруженные данные:</h4>
                <p><b>Записей:</b> {len(self.current_telemetry)}</p>
                <p><b>Формат:</b> CSV/Список</p>
                """
            
            self.current_data_info.setHtml(info_html)
    
    def run_analysis(self):
        """Запуск анализа"""
        if not hasattr(self, 'current_telemetry'):
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Сначала загрузите данные телеметрии!")
            return
        
        try:
            # Преобразуем данные в нужный формат
            lap_data = self.prepare_lap_data()
            reference_lap = getattr(self, 'reference_lap', None)
            
            # Выполняем анализ
            self.current_analysis = self.trainer.analyze_lap(lap_data, reference_lap)
            
            # Отображаем результаты
            self.display_analysis_results()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Ошибка анализа", f"Произошла ошибка: {e}")
    
    def prepare_lap_data(self):
        """Подготовка данных для анализа"""
        if isinstance(self.current_telemetry, dict):
            return self.current_telemetry
        else:
            # Если это список записей CSV, агрегируем данные
            # Простая реализация - можно расширить
            return {
                'lap_time': 90.0,  # Примерное время
                'sector_times': [30.0, 30.0, 30.0],
                'brake_history': [float(r.get('brake', 0)) for r in self.current_telemetry[:100]],
                'throttle_history': [float(r.get('throttle', 0)) for r in self.current_telemetry[:100]],
                'steering_history': [float(r.get('steering', 0)) for r in self.current_telemetry[:100]]
            }
    
    def display_analysis_results(self):
        """Отображение результатов анализа"""
        if not self.current_analysis:
            return
        
        analysis = self.current_analysis
        
        # Основной анализ
        main_html = f"""
        <h2 style="color: #0078d4;">📊 Анализ круга</h2>
        
        <h3 style="color: #ffa500;">Общие результаты:</h3>
        <p><b>Время круга:</b> {analysis.lap_time:.3f} сек</p>
        <p><b>Потенциал улучшения:</b> {analysis.improvement_potential:.3f} сек</p>
        
        <h3 style="color: #ffa500;">Сильные стороны:</h3>
        """
        
        if analysis.strengths:
            main_html += "<ul>"
            for strength in analysis.strengths:
                main_html += f"<li style='color: #4ecdc4;'>✅ {strength}</li>"
            main_html += "</ul>"
        else:
            main_html += "<p>Не выявлено</p>"
        
        main_html += "<h3 style='color: #ffa500;'>Проблемные области:</h3>"
        
        if analysis.issues:
            main_html += "<ul>"
            for issue in analysis.issues:
                main_html += f"<li style='color: #ff6b6b;'>❌ {issue}</li>"
            main_html += "</ul>"
        else:
            main_html += "<p style='color: #4ecdc4;'>Проблем не выявлено!</p>"
        
        self.main_analysis.setHtml(main_html)
        
        # Детальный анализ
        detailed_html = f"""
        <h2 style="color: #0078d4;">🔍 Детальный анализ</h2>
        
        <h3 style="color: #ffa500;">Времена секторов:</h3>
        """
        
        if analysis.sector_times:
            detailed_html += "<table style='width: 100%; border-collapse: collapse;'>"
            detailed_html += "<tr style='background-color: #3c3c3c;'><th>Сектор</th><th>Время</th></tr>"
            for i, sector_time in enumerate(analysis.sector_times, 1):
                detailed_html += f"<tr><td>Сектор {i}</td><td>{sector_time:.3f} сек</td></tr>"
            detailed_html += "</table>"
        
        detailed_html += "<h3 style='color: #ffa500;'>Рекомендации:</h3><ul>"
        for recommendation in analysis.recommendations:
            detailed_html += f"<li>{recommendation}</li>"
        detailed_html += "</ul>"
        
        self.detailed_analysis.setHtml(detailed_html)
        
        # Обновляем быстрые рекомендации
        quick_html = "<h4 style='color: #0078d4;'>Приоритетные улучшения:</h4><ul>"
        for i, rec in enumerate(analysis.recommendations[:3], 1):
            quick_html += f"<li><b>{i}.</b> {rec}</li>"
        quick_html += "</ul>"
        
        self.quick_recommendations.setHtml(quick_html)
    
    def generate_training_plan(self):
        """Генерация плана тренировок"""
        if not self.current_analysis:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Сначала выполните анализ!")
            return
        
        # Генерируем план на основе анализа
        training_plan = self.trainer.generate_training_plan([self.current_analysis])
        
        plan_html = f"""
        <h3 style="color: #0078d4;">🎯 Персональный план тренировок</h3>
        
        <p><b>Рекомендуемое время сессии:</b> {training_plan.get('recommended_session_time', '45-60 минут')}</p>
        
        <h4 style="color: #ffa500;">Области фокуса:</h4>
        <ul>
        """
        
        for area in training_plan.get('focus_areas', []):
            plan_html += f"<li>{area}</li>"
        
        plan_html += "</ul><h4 style='color: #ffa500;'>Упражнения:</h4>"
        
        for exercise in training_plan.get('plan', []):
            plan_html += f"""
            <div style='margin-bottom: 15px; padding: 10px; background-color: #3c3c3c; border-radius: 5px;'>
                <h5 style='color: #4ecdc4; margin: 0;'>{exercise.get('area', 'Упражнение')}</h5>
                <p style='margin: 5px 0;'><b>Время:</b> {exercise.get('duration', 'N/A')}</p>
                <ul style='margin: 5px 0;'>
            """
            
            for ex in exercise.get('exercises', []):
                plan_html += f"<li>{ex}</li>"
            
            plan_html += "</ul></div>"
        
        self.training_plan.setHtml(plan_html)
    
    def save_analysis(self):
        """Сохранение анализа"""
        if not self.current_analysis:
            QtWidgets.QMessageBox.warning(self, "Ошибка", "Нет данных для сохранения!")
            return
        
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Сохранить анализ", "", "JSON files (*.json);;All files (*)"
        )
        
        if file_path:
            try:
                self.trainer.save_analysis(self.current_analysis, file_path)
                QtWidgets.QMessageBox.information(self, "Успех", "Анализ сохранен!")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить: {e}")
