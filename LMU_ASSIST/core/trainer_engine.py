import numpy as np
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import statistics

@dataclass
class LapAnalysis:
    """Результат анализа круга"""
    lap_time: float
    sector_times: List[float]
    issues: List[str]
    strengths: List[str]
    improvement_potential: float
    recommendations: List[str]

class TrainerEngine:
    """Усовершенствованный движок для анализа и обучения"""
    
    def __init__(self, reference_data: Dict = None):
        self.reference_data = reference_data or {}
        self.driving_patterns = {}
        self.learning_history = []
        
        # Пороги для анализа
        self.thresholds = {
            'braking_efficiency': 0.85,
            'throttle_smoothness': 0.8,
            'steering_smoothness': 0.75,
            'consistency': 0.95,
            'sector_deviation': 2.0  # секунды
        }
    
    def analyze_lap(self, lap_data: Dict, reference_lap: Dict = None) -> LapAnalysis:
        """Полный анализ круга"""
        ref_lap = reference_lap or self.reference_data.get('best_lap', {})
        
        issues = []
        strengths = []
        recommendations = []
        
        # Анализ времени круга
        lap_time = lap_data.get('lap_time', 0)
        ref_time = ref_lap.get('lap_time', float('inf'))
        
        if ref_time != float('inf'):
            time_diff = lap_time - ref_time
            if time_diff > 2.0:
                issues.append(f"Время круга на {time_diff:.2f}с медленнее эталона")
            elif time_diff < 0.5:
                strengths.append("Отличное время круга!")
        
        # Анализ секторов
        sector_analysis = self._analyze_sectors(lap_data, ref_lap)
        issues.extend(sector_analysis['issues'])
        strengths.extend(sector_analysis['strengths'])
        recommendations.extend(sector_analysis['recommendations'])
        
        # Анализ техники вождения
        technique_analysis = self._analyze_driving_technique(lap_data)
        issues.extend(technique_analysis['issues'])
        strengths.extend(technique_analysis['strengths'])
        recommendations.extend(technique_analysis['recommendations'])
        
        # Расчет потенциала улучшения
        improvement_potential = self._calculate_improvement_potential(lap_data, ref_lap)
        
        return LapAnalysis(
            lap_time=lap_time,
            sector_times=lap_data.get('sector_times', []),
            issues=issues,
            strengths=strengths,
            improvement_potential=improvement_potential,
            recommendations=recommendations
        )
    
    def _analyze_sectors(self, lap_data: Dict, ref_lap: Dict) -> Dict:
        """Анализ времен секторов"""
        analysis = {'issues': [], 'strengths': [], 'recommendations': []}
        
        lap_sectors = lap_data.get('sector_times', [])
        ref_sectors = ref_lap.get('sector_times', [])
        
        if len(lap_sectors) == len(ref_sectors) and len(lap_sectors) > 0:
            for i, (sector_time, ref_time) in enumerate(zip(lap_sectors, ref_sectors)):
                diff = sector_time - ref_time
                sector_num = i + 1
                
                if diff > self.thresholds['sector_deviation']:
                    analysis['issues'].append(f"Сектор {sector_num}: потеря {diff:.2f}с")
                    analysis['recommendations'].append(
                        f"Изучи эталонную траекторию в секторе {sector_num}"
                    )
                elif diff < -0.5:
                    analysis['strengths'].append(f"Отличный сектор {sector_num}!")
        
        return analysis
    
    def _analyze_driving_technique(self, lap_data: Dict) -> Dict:
        """Анализ техники вождения"""
        analysis = {'issues': [], 'strengths': [], 'recommendations': []}
        
        # Анализ торможения
        brake_analysis = self._analyze_braking(lap_data)
        analysis['issues'].extend(brake_analysis['issues'])
        analysis['strengths'].extend(brake_analysis['strengths'])
        analysis['recommendations'].extend(brake_analysis['recommendations'])
        
        # Анализ ускорения
        throttle_analysis = self._analyze_throttle(lap_data)
        analysis['issues'].extend(throttle_analysis['issues'])
        analysis['strengths'].extend(throttle_analysis['strengths'])
        analysis['recommendations'].extend(throttle_analysis['recommendations'])
        
        # Анализ рулежки
        steering_analysis = self._analyze_steering(lap_data)
        analysis['issues'].extend(steering_analysis['issues'])
        analysis['strengths'].extend(steering_analysis['strengths'])
        analysis['recommendations'].extend(steering_analysis['recommendations'])
        
        return analysis
    
    def _analyze_braking(self, lap_data: Dict) -> Dict:
        """Анализ торможения"""
        analysis = {'issues': [], 'strengths': [], 'recommendations': []}
        
        brake_data = lap_data.get('brake_history', [])
        if not brake_data:
            return analysis
        
        # Анализ плавности торможения
        brake_smoothness = self._calculate_smoothness(brake_data)
        if brake_smoothness < self.thresholds['braking_efficiency']:
            analysis['issues'].append("Резкое торможение")
            analysis['recommendations'].append(
                "Попробуй более плавное и прогрессивное торможение"
            )
        else:
            analysis['strengths'].append("Плавное торможение")
        
        # Анализ эффективности торможения
        max_brake = max(brake_data) if brake_data else 0
        if max_brake < 0.8:
            analysis['issues'].append("Недостаточное использование тормозов")
            analysis['recommendations'].append(
                "Используй тормоза более агрессивно в зонах торможения"
            )
        
        return analysis
    
    def _analyze_throttle(self, lap_data: Dict) -> Dict:
        """Анализ работы с газом"""
        analysis = {'issues': [], 'strengths': [], 'recommendations': []}
        
        throttle_data = lap_data.get('throttle_history', [])
        if not throttle_data:
            return analysis
        
        # Анализ плавности газа
        throttle_smoothness = self._calculate_smoothness(throttle_data)
        if throttle_smoothness < self.thresholds['throttle_smoothness']:
            analysis['issues'].append("Резкая работа с газом")
            analysis['recommendations'].append(
                "Более плавно работай с педалью газа"
            )
        else:
            analysis['strengths'].append("Плавная работа с газом")
        
        # Анализ раннего ускорения
        early_throttle = self._analyze_early_throttle(lap_data)
        if early_throttle < 0.7:
            analysis['issues'].append("Поздно открываешь газ")
            analysis['recommendations'].append(
                "Пробуй открывать газ раньше на выходе из поворотов"
            )
        
        return analysis
    
    def _analyze_steering(self, lap_data: Dict) -> Dict:
        """Анализ рулежки"""
        analysis = {'issues': [], 'strengths': [], 'recommendations': []}
        
        steering_data = lap_data.get('steering_history', [])
        if not steering_data:
            return analysis
        
        # Анализ плавности рулежки
        steering_smoothness = self._calculate_smoothness(steering_data)
        if steering_smoothness < self.thresholds['steering_smoothness']:
            analysis['issues'].append("Резкая рулежка")
            analysis['recommendations'].append(
                "Сгладь движения рулем, особенно при входе в повороты"
            )
        else:
            analysis['strengths'].append("Плавная рулежка")
        
        return analysis
    
    def _calculate_smoothness(self, data: List[float]) -> float:
        """Расчет плавности данных"""
        if len(data) < 2:
            return 1.0
        
        # Рассчитываем стандартное отклонение производной
        derivatives = np.diff(data)
        smoothness = 1.0 - min(np.std(derivatives) / np.mean(np.abs(data)) if np.mean(np.abs(data)) > 0 else 0, 1.0)
        return max(smoothness, 0.0)
    
    def _analyze_early_throttle(self, lap_data: Dict) -> float:
        """Анализ раннего ускорения на выходе из поворотов"""
        # Упрощенная эвристика
        throttle_data = lap_data.get('throttle_history', [])
        steering_data = lap_data.get('steering_history', [])
        
        if len(throttle_data) != len(steering_data) or len(throttle_data) < 10:
            return 0.5
        
        # Ищем моменты выхода из поворотов (уменьшение угла поворота руля)
        early_throttle_score = 0.5
        
        for i in range(1, len(steering_data) - 1):
            if abs(steering_data[i]) > abs(steering_data[i + 1]):  # Выход из поворота
                if throttle_data[i] > 0.5:  # Раннее ускорение
                    early_throttle_score += 0.1
        
        return min(early_throttle_score, 1.0)
    
    def _calculate_improvement_potential(self, lap_data: Dict, ref_lap: Dict) -> float:
        """Расчет потенциала улучшения в секундах"""
        if not ref_lap:
            return 0.0
        
        lap_time = lap_data.get('lap_time', 0)
        ref_time = ref_lap.get('lap_time', 0)
        
        if ref_time == 0:
            return 0.0
        
        # Базовый потенциал на основе разницы времен
        time_potential = max(lap_time - ref_time, 0)
        
        # Дополнительный потенциал на основе техники
        technique_potential = 0
        
        # Потенциал от улучшения торможения
        brake_smoothness = self._calculate_smoothness(lap_data.get('brake_history', []))
        if brake_smoothness < self.thresholds['braking_efficiency']:
            technique_potential += 0.5
        
        # Потенциал от улучшения ускорения
        throttle_smoothness = self._calculate_smoothness(lap_data.get('throttle_history', []))
        if throttle_smoothness < self.thresholds['throttle_smoothness']:
            technique_potential += 0.3
        
        return round(time_potential + technique_potential, 2)
    
    def analyze_consistency(self, laps_data: List[Dict]) -> Dict:
        """Анализ стабильности времен кругов"""
        if len(laps_data) < 3:
            return {'consistency': 1.0, 'recommendations': ["Нужно больше кругов для анализа"]}
        
        lap_times = [lap.get('lap_time', 0) for lap in laps_data if lap.get('lap_time', 0) > 0]
        
        if not lap_times:
            return {'consistency': 1.0, 'recommendations': ["Нет данных о временах кругов"]}
        
        # Расчет коэффициента вариации
        mean_time = statistics.mean(lap_times)
        std_time = statistics.stdev(lap_times) if len(lap_times) > 1 else 0
        cv = std_time / mean_time if mean_time > 0 else 0
        
        consistency = max(1.0 - cv, 0.0)
        
        recommendations = []
        if consistency < self.thresholds['consistency']:
            recommendations.append("Работай над стабильностью времен кругов")
            recommendations.append("Сосредоточься на повторяемости траектории")
        else:
            recommendations.append("Отличная стабильность!")
        
        return {
            'consistency': round(consistency, 3),
            'std_deviation': round(std_time, 3),
            'mean_time': round(mean_time, 3),
            'recommendations': recommendations
        }
    
    def generate_training_plan(self, analysis_results: List[LapAnalysis]) -> Dict:
        """Генерация плана тренировок"""
        if not analysis_results:
            return {'plan': [], 'focus_areas': []}
        
        # Собираем статистику проблем
        issue_counts = {}
        for analysis in analysis_results:
            for issue in analysis.issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
        
        # Определяем основные проблемы
        main_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        focus_areas = [issue for issue, count in main_issues]
        
        training_plan = []
        
        # Генерируем план на основе проблем
        for issue, count in main_issues:
            if "торможение" in issue.lower():
                training_plan.append({
                    'area': 'Торможение',
                    'exercises': [
                        'Практика торможения в одну точку',
                        'Работа над плавностью нажатия педали',
                        'Поиск поздних точек торможения'
                    ],
                    'duration': '15-20 минут'
                })
            elif "газ" in issue.lower() or "ускорение" in issue.lower():
                training_plan.append({
                    'area': 'Ускорение',
                    'exercises': [
                        'Практика раннего ускорения',
                        'Работа над плавностью открытия газа',
                        'Поиск оптимальных точек ускорения'
                    ],
                    'duration': '15-20 минут'
                })
            elif "рулежка" in issue.lower() or "руль" in issue.lower():
                training_plan.append({
                    'area': 'Рулежка',
                    'exercises': [
                        'Практика плавных движений рулем',
                        'Работа над точностью траектории',
                        'Минимизация коррекций руля'
                    ],
                    'duration': '20-25 минут'
                })
        
        return {
            'plan': training_plan,
            'focus_areas': focus_areas,
            'recommended_session_time': '45-60 минут'
        }

    def save_analysis(self, analysis: LapAnalysis, filename: str):
        """Сохранение анализа в файл"""
        try:
            data = {
                'lap_time': analysis.lap_time,
                'sector_times': analysis.sector_times,
                'issues': analysis.issues,
                'strengths': analysis.strengths,
                'improvement_potential': analysis.improvement_potential,
                'recommendations': analysis.recommendations,
                'timestamp': time.time()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            print(f"Ошибка сохранения анализа: {e}")
