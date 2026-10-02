import os
import random
import pandas as pd
from datetime import datetime, timedelta

# 1. Configuración de parámetros
NUM_REGISTROS = 120
OUTPUT_PATH = os.path.join("data", "processed", "caracterizacion_limpia.csv")

# 2. Listas de valores ficticios pero representativos
nombres_base = ["Maria", "Ana", "Carmen", "Luz", "Rosa", "Esperanza", "Diana", "Leonor", "Kelly", "Yadira", "Aura", "Gloria", "Sandra", "Patricia", "Yolanda"]
apellidos_base = ["Mina", "Lucumi", "Valencia", "Colorado", "Renteria", "Carabali", "Angulo", "Balanta", "Moreno", "Cifuentes", "Vargas", "Guerrero"]

# Listas de opciones
estados_civiles = ["Soltera(o)", "En unión libre", "Casada(o)", "Separada(o) / Divorciada(o)", "Viuda(o)"]
tenencias = ["Propia totalmente pagada", "Arrendada", "Familiar / Prestada", "En pago"]
estratos = ["Estrato 1 (Bajo-Bajo)", "Estrato 2 (Bajo)", "Estrato 3 (Medio-Bajo)"]
niveles_edu = ["Primaria incompleta", "Primaria completa", "Secundaria completa", "Educación técnica o tecnológica", "Educación universitaria"]
niveles_digital = ["Básico", "Intermedio", "Avanzado", "Nulo / Muy bajo"]
situaciones_lab = ["Independiente / Emprendedora", "Desempleada(o)", "Estudiante", "Empleado(a) informal"]
servicios_base = [
    "Acueducto (agua potable), Alcantarillado, Energía eléctrica, Gas natural, Acceso a Internet",
    "Acueducto (agua potable), Alcantarillado, Energía eléctrica, Gas natural",
    "Acueducto (agua potable), Energía eléctrica"
]
dispositivos_lista = ["Teléfono Inteligente", "Computadora (Portátil, Escritorio)", "Ambos", "Ninguno"]

records = []
start_date = datetime(2025, 7, 1)

for i in range(1, NUM_REGISTROS + 1):
    # Generación de fechas aleatorias recientes
    fecha_random = start_date + timedelta(days=random.randint(0, 180), minutes=random.randint(0, 1440))
    
    # Nombre
    nombre_full = f"{random.choice(nombres_base)} {random.choice(apellidos_base)} {random.choice(apellidos_base)}"
    email = f"{nombre_full.lower().replace(' ', '.')}@example.com"
    
    # Variables numéricas y categóricas ponderadas
    edad = random.choices(range(18, 70), weights=[1 if 18<=x<=25 else 3 if 26<=x<=45 else 2 if 46<=x<=60 else 1 for x in range(18, 70)])[0]
    
    if edad < 30:
        rango_edad = "Joven (18-29 años)"
    elif edad <= 50:
        rango_edad = "Adulta (30-50 años)"
    else:
        rango_edad = "Adulta Mayor (>50 años)"

    # Relaciones lógicas
    educacion = random.choices(niveles_edu, weights=[10, 20, 45, 20, 5])[0]
    dig_level = random.choices(niveles_digital, weights=[50, 30, 10, 10])[0]
    suficiencia = random.choices(["No, no son suficientes.", "Sí, son suficientes.", "Apenas cubren lo básico."], weights=[65, 15, 20])[0]
    lab_stat = random.choices(situaciones_lab, weights=[55, 25, 10, 10])[0]
    
    record = {
        "marca_temporal": fecha_random.strftime("%d/%m/%Y %H:%M:%S"),
        "consentimiento": "Sí, deseo participar.",
        "nombre": nombre_full,
        "email": email,
        "edad": edad,
        "genero": "Mujer",
        "estado_civil": random.choice(estados_civiles),
        "convivientes": str(random.randint(1, 6)),
        "tipo_vivienda": random.choices(["Casa (independiente)", "Vivienda compartida", "Apartamento"], weights=[70, 20, 10])[0],
        "tenencia_vivienda": random.choices(tenencias, weights=[35, 45, 15, 5])[0],
        "estrato": random.choices(estratos, weights=[65, 30, 5])[0],
        "zona_residencia": random.choices(["Urbana (Cabecera municipal de Zarzal)", "Rural / Corregimiento"], weights=[85, 15])[0],
        "etnia": random.choices(["Negra, mulata, afrocolombiana o afrodescendiente", "Mestiza"], weights=[90, 10])[0],
        "nivel_educativo": educacion,
        "capacitacion_12m": random.choice(["Si", "No"]),
        "tipo_capacitacion": random.choice(["Talleres presenciales", "Cursos virtuales", "Ninguna"]),
        "barreras_educacion": random.choice(["Falta de tiempo", "Dificultades económicas", "Falta de información"]),
        "nivel_digital": dig_level,
        "herramientas_digitales": random.choice(["Redes Sociales", "WhatsApp Business", "Correo electrónico"]),
        "areas_capacitacion_formal": random.choice(["Uso de tecnologías digitales", "Gestión financiera", "Marketing"]),
        "comodidad_plataformas_virtuales": random.choice(["Si, Siempre", "A veces", "No, se me dificulta"]),
        "situacion_laboral": lab_stat,
        "motivacion_trabajo": random.choice(["Obtener ingresos para mi hogar", "Cubrir gastos personales", "Independencia"]),
        "fuente_ingresos_hogar": random.choice(["Ventas del emprendimiento", "Trabajo informal / Ocasional", "Aportes familiares"]),
        "suficiencia_ingresos": suficiencia,
        "aporte_economico_hogar": random.choice(["Sí, aporto una parte complementaria", "Sí, aporto la mayor parte", "No aporto"]),
        "servicios_publicos": random.choices(servicios_base, weights=[60, 30, 10])[0],
        "acceso_salud": random.choices(["Sí", "No"], weights=[80, 20])[0],
        "apoyo_emocional": random.choices(["Sí", "No", "En ocasiones"], weights=[50, 30, 20])[0],
        "calidad_ambiental": random.choices(["Aceptable", "Buena", "Mala"], weights=[50, 30, 20])[0],
        "acceso_fuentes_naturales": random.choice(["Sí, fácilmente", "No, no tengo acceso"]),
        "percepcion_seguridad": random.choices(["Ni segura(o) ni insegura(o)", "Segura(o)", "Insegura(o)"], weights=[45, 35, 20])[0],
        "horas_trabajo_domestico": random.choices(["Más de 4 horas", "3 a 4 horas", "1 a 2 horas"], weights=[60, 30, 10])[0],
        "horas_trabajo_externo": random.choices(["Más de 4 horas", "2 a 4 horas", "Menos de 2 horas"], weights=[40, 40, 20])[0],
        "tiempo_descanso": random.choices(["Poco tiempo", "Sí, suficiente tiempo", "Casi nada"], weights=[60, 25, 15])[0],
        "frecuencia_ejercicio": random.choice(["Nunca", "1 a 2 veces por semana", "3 o más veces"]),
        "condicion_discapacidad": random.choices(["No", "Si"], weights=[90, 10])[0],
        "espacios_autocuidado": random.choice(["No, pero me gustaría", "Si", "Prefiero no responder"]),
        "barreras_autocuidado": random.choice(["Falta de recursos económicos", "Falta de tiempo", "Falta de apoyo"]),
        "frecuencia_info_desarrollo": random.choice(["Diariamente", "Semanalmente", "Rara vez"]),
        "fuente_aprendizaje_empresarial": random.choice(["Internet (videos, redes sociales)", "Talleres presenciales", "Familiares"]),
        "dispositivos_disponibles": random.choices(dispositivos_lista, weights=[70, 10, 15, 5])[0],
        "participa_organizacion": random.choices(["Sí", "No"], weights=[75, 25])[0],
        "tipo_organizacion": random.choice(["Asociación de emprendedoras", "Junta de Acción Comunal", "Colectivo cultural"]),
        "rango_edad": rango_edad
    }
    records.append(record)

# 3. Guardar en DataFrame y CSV
df_simulado = pd.DataFrame(records)
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
df_simulado.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

print(f"🎉 ¡Simulación exitosa! Se han generado {NUM_REGISTROS} registros sintéticos en '{OUTPUT_PATH}'.")