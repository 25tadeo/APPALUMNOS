"""
Study Tracker Pro - Backend en Python Flask
App de estudio universitario con cuestionarios integrados
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
app.secret_key = 'study_tracker_secret_key'

# ========== BASE DE DATOS DE MATERIAS CON CUESTIONARIOS ==========

SUBJECTS_DATA = {
    'matematicas': {
        'name': 'Matemáticas',
        'description': 'Cálculo, Álgebra y Análisis Matemático',
        'emoji': '🔢',
        'quizzes': [
            {
                'id': 1,
                'title': 'Quiz 1: Derivadas e Integrales',
                'questions': [
                    {
                        'id': 1,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es la derivada de f(x) = 3x²?',
                        'options': ['6x', '3x', '2x', '9x'],
                        'correct': 0
                    },
                    {
                        'id': 2,
                        'type': 'true_false',
                        'text': 'La integral es la operación inversa de la derivada',
                        'correct': True
                    },
                    {
                        'id': 3,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es el resultado de ∫(2x)dx?',
                        'options': ['x² + C', '2x + C', 'x² - C', '2x²'],
                        'correct': 0
                    },
                    {
                        'id': 4,
                        'type': 'true_false',
                        'text': 'La constante de integración C es obligatoria en integrales indefinidas',
                        'correct': True
                    },
                    {
                        'id': 5,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es el límite de (x² + 2x) cuando x tiende a 0?',
                        'options': ['0', '2', '1', 'Indefinido'],
                        'correct': 0
                    }
                ]
            }
        ]
    },
    'fisica': {
        'name': 'Física',
        'description': 'Mecánica, Termodinámica y Ondas',
        'emoji': '⚛️',
        'quizzes': [
            {
                'id': 1,
                'title': 'Quiz 1: Cinemática y Dinámica',
                'questions': [
                    {
                        'id': 1,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es la fórmula de la velocidad promedio?',
                        'options': ['v = d/t', 'v = at', 'v = m/g', 'v = F/m'],
                        'correct': 0
                    },
                    {
                        'id': 2,
                        'type': 'true_false',
                        'text': 'La aceleración es la derivada de la velocidad respecto al tiempo',
                        'correct': True
                    },
                    {
                        'id': 3,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es la segunda ley de Newton?',
                        'options': ['F = ma', 'F = mv', 'F = mg', 'F = m/a'],
                        'correct': 0
                    },
                    {
                        'id': 4,
                        'type': 'true_false',
                        'text': 'La velocidad es una magnitud escalar',
                        'correct': False
                    },
                    {
                        'id': 5,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es la unidad de aceleración en el SI?',
                        'options': ['m/s²', 'm/s', 'km/h', 'rad/s'],
                        'correct': 0
                    }
                ]
            }
        ]
    },
    'programacion': {
        'name': 'Programación',
        'description': 'Python, Estructuras de Datos y Algoritmos',
        'emoji': '💻',
        'quizzes': [
            {
                'id': 1,
                'title': 'Quiz 1: Conceptos Básicos de Python',
                'questions': [
                    {
                        'id': 1,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es el tipo de dato de x = "hola" en Python?',
                        'options': ['string', 'integer', 'float', 'boolean'],
                        'correct': 0
                    },
                    {
                        'id': 2,
                        'type': 'true_false',
                        'text': 'Las listas en Python son mutables',
                        'correct': True
                    },
                    {
                        'id': 3,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es la forma correcta de declarar un diccionario vacío?',
                        'options': ['{}', '[]', '()', 'dict()'],
                        'correct': 0
                    },
                    {
                        'id': 4,
                        'type': 'true_false',
                        'text': 'Python es un lenguaje compilado',
                        'correct': False
                    },
                    {
                        'id': 5,
                        'type': 'multiple_choice',
                        'text': '¿Qué función ordena una lista en Python?',
                        'options': ['sorted()', 'order()', 'arrange()', 'sort_list()'],
                        'correct': 0
                    }
                ]
            }
        ]
    },
    'quimica': {
        'name': 'Química',
        'description': 'Química General, Orgánica e Inorgánica',
        'emoji': '🧪',
        'quizzes': [
            {
                'id': 1,
                'title': 'Quiz 1: Tabla Periódica y Enlaces',
                'questions': [
                    {
                        'id': 1,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es el símbolo del Oro?',
                        'options': ['Au', 'Ag', 'Ag', 'Cu'],
                        'correct': 0
                    },
                    {
                        'id': 2,
                        'type': 'true_false',
                        'text': 'El enlace iónico ocurre entre dos no-metales',
                        'correct': False
                    },
                    {
                        'id': 3,
                        'type': 'multiple_choice',
                        'text': '¿Cuántos electrones de valencia tiene el Carbono?',
                        'options': ['4', '3', '5', '6'],
                        'correct': 0
                    },
                    {
                        'id': 4,
                        'type': 'true_false',
                        'text': 'La electronegatividad aumenta de izquierda a derecha en la tabla periódica',
                        'correct': True
                    },
                    {
                        'id': 5,
                        'type': 'multiple_choice',
                        'text': '¿Cuál es el pH neutro?',
                        'options': ['7', '0', '14', '10'],
                        'correct': 0
                    }
                ]
            }
        ]
    },
    'historia': {
        'name': 'Historia',
        'description': 'Historia Universal y Contemporánea',
        'emoji': '📜',
        'quizzes': [
            {
                'id': 1,
                'title': 'Quiz 1: Revolución Francesa e Industrial',
                'questions': [
                    {
                        'id': 1,
                        'type': 'multiple_choice',
                        'text': '¿En qué año comenzó la Revolución Francesa?',
                        'options': ['1789', '1776', '1800', '1805'],
                        'correct': 0
                    },
                    {
                        'id': 2,
                        'type': 'true_false',
                        'text': 'La Revolución Industrial comenzó en Francia',
                        'correct': False
                    },
                    {
                        'id': 3,
                        'type': 'multiple_choice',
                        'text': '¿Cuál fue el lema de la Revolución Francesa?',
                        'options': ['Libertad, Igualdad, Fraternidad', 'Viva la República', 'Por Dios y el Rey', 'Igualdad para todos'],
                        'correct': 0
                    },
                    {
                        'id': 4,
                        'type': 'true_false',
                        'text': 'Napoleón Bonaparte fue el primer emperador de Francia durante la Revolución',
                        'correct': True
                    },
                    {
                        'id': 5,
                        'type': 'multiple_choice',
                        'text': '¿Qué país lideró la Revolución Industrial primero?',
                        'options': ['Inglaterra', 'Francia', 'Alemania', 'Estados Unidos'],
                        'correct': 0
                    }
                ]
            }
        ]
    }
}

# Almacenar resultados de cuestionarios
quiz_results = {}

# ========== RUTAS PRINCIPALES ==========

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/api/subjects')
def get_subjects():
    """Obtener lista de materias"""
    subjects = []
    for key, data in SUBJECTS_DATA.items():
        subjects.append({
            'id': key,
            'name': data['name'],
            'emoji': data['emoji'],
            'description': data['description'],
            'quizzes_count': len(data['quizzes'])
        })
    return jsonify(subjects)

@app.route('/api/subject/<subject_id>')
def get_subject(subject_id):
    """Obtener detalles de una materia"""
    if subject_id in SUBJECTS_DATA:
        data = SUBJECTS_DATA[subject_id]
        return jsonify({
            'id': subject_id,
            'name': data['name'],
            'emoji': data['emoji'],
            'description': data['description'],
            'quizzes': data['quizzes']
        })
    return jsonify({'error': 'Materia no encontrada'}), 404

@app.route('/api/quiz/<subject_id>/<int:quiz_id>')
def get_quiz(subject_id, quiz_id):
    """Obtener un cuestionario específico"""
    if subject_id in SUBJECTS_DATA:
        quizzes = SUBJECTS_DATA[subject_id]['quizzes']
        for quiz in quizzes:
            if quiz['id'] == quiz_id:
                return jsonify(quiz)
    return jsonify({'error': 'Cuestionario no encontrado'}), 404

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    """Procesar respuestas del cuestionario"""
    data = request.json
    subject_id = data.get('subject_id')
    quiz_id = data.get('quiz_id')
    answers = data.get('answers')
    
    if subject_id not in SUBJECTS_DATA:
        return jsonify({'error': 'Materia no encontrada'}), 404
    
    # Buscar el cuestionario
    quiz = None
    for q in SUBJECTS_DATA[subject_id]['quizzes']:
        if q['id'] == quiz_id:
            quiz = q
            break
    
    if not quiz:
        return jsonify({'error': 'Cuestionario no encontrado'}), 404
    
    # Calificar
    correct = 0
    total = len(quiz['questions'])
    results = []
    
    for question in quiz['questions']:
        q_id = question['id']
        user_answer = answers.get(str(q_id))
        
        # Determinar si es correcta
        is_correct = False
        if question['type'] == 'true_false':
            correct_answer = question['correct']
            is_correct = user_answer == str(correct_answer)
        else:
            is_correct = int(user_answer) == question['correct']
        
        if is_correct:
            correct += 1
        
        results.append({
            'question_id': q_id,
            'question': question['text'],
            'type': question['type'],
            'user_answer': user_answer,
            'correct_answer': str(question['correct']) if question['type'] == 'true_false' else question['options'][question['correct']],
            'is_correct': is_correct
        })
    
    # Calcular porcentaje
    percentage = (correct / total) * 100
    
    # Guardar resultado
    result_id = f"{subject_id}_{quiz_id}_{datetime.now().timestamp()}"
    quiz_results[result_id] = {
        'subject_id': subject_id,
        'subject_name': SUBJECTS_DATA[subject_id]['name'],
        'quiz_id': quiz_id,
        'quiz_title': quiz['title'],
        'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'correct': correct,
        'total': total,
        'percentage': percentage,
        'results': results
    }
    
    return jsonify({
        'correct': correct,
        'total': total,
        'percentage': round(percentage, 2),
        'results': results
    })

@app.route('/api/subject/<subject_id>/history')
def get_subject_history(subject_id):
    """Obtener historial de cuestionarios de una materia"""
    history = []
    for result in quiz_results.values():
        if result['subject_id'] == subject_id:
            history.append({
                'date': result['date'],
                'quiz': result['quiz_title'],
                'percentage': result['percentage'],
                'correct': result['correct'],
                'total': result['total']
            })
    
    return jsonify(history)

@app.route('/api/stats')
def get_stats():
    """Obtener estadísticas generales"""
    if not quiz_results:
        return jsonify({
            'total_quizzes': 0,
            'avg_percentage': 0,
            'best_percentage': 0,
            'total_correct': 0,
            'total_questions': 0
        })
    
    results_list = list(quiz_results.values())
    total_quizzes = len(results_list)
    total_correct = sum(r['correct'] for r in results_list)
    total_questions = sum(r['total'] for r in results_list)
    avg_percentage = sum(r['percentage'] for r in results_list) / total_quizzes
    best_percentage = max(r['percentage'] for r in results_list)
    
    return jsonify({
        'total_quizzes': total_quizzes,
        'avg_percentage': round(avg_percentage, 2),
        'best_percentage': best_percentage,
        'total_correct': total_correct,
        'total_questions': total_questions
    })

# ========== MANEJO DE ERRORES ==========

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Página no encontrada'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Error del servidor'}), 500

# ========== EJECUTAR APP ==========

if __name__ == '__main__':
    print("=" * 50)
    print("🎓 Study Tracker Pro - Backend Python Flask")
    print("=" * 50)
    print("✅ Servidor corriendo en: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)