import os
import pandas as pd

# 1. Definir rutas claras dentro del proyecto
input_path = os.path.join("data", "caracterizacion_raw.csv")
output_path = os.path.join("data", "processed", "caracterizacion_limpia.csv")

# Verificar si el archivo existe
if not os.path.exists(input_path):
    print(f"❌ No se encontró el archivo en la ruta: '{input_path}'")
    print("Por favor, verifica que el CSV esté dentro de la carpeta 'data' con el nombre 'caracterizacion_raw.csv'.")
else:
    print(f"📂 Cargando archivo desde: {input_path}")
    df = pd.read_csv(input_path)

    # 2. Lista estandarizada de nombres cortos para las 44 columnas
    nuevos_nombres = [
        "marca_temporal",
        "consentimiento",
        "nombre",
        "email",
        "edad",
        "genero",
        "estado_civil",
        "convivientes",
        "tipo_vivienda",
        "tenencia_vivienda",
        "estrato",
        "zona_residencia",
        "etnia",
        "nivel_educativo",
        "capacitacion_12m",
        "tipo_capacitacion",
        "barreras_educacion",
        "nivel_digital",
        "herramientas_digitales",
        "areas_capacitacion_formal",
        "comodidad_plataformas_virtuales",
        "situacion_laboral",
        "motivacion_trabajo",
        "fuente_ingresos_hogar",
        "suficiencia_ingresos",
        "aporte_economico_hogar",
        "servicios_publicos",
        "acceso_salud",
        "apoyo_emocional",
        "calidad_ambiental",
        "acceso_fuentes_naturales",
        "percepcion_seguridad",
        "horas_trabajo_domestico",
        "horas_trabajo_externo",
        "tiempo_descanso",
        "frecuencia_ejercicio",
        "condicion_discapacidad",
        "espacios_autocuidado",
        "barreras_autocuidado",
        "frecuencia_info_desarrollo",
        "fuente_aprendizaje_empresarial",
        "dispositivos_disponibles",
        "participa_organizacion",
        "tipo_organizacion"
    ]

    # Asignar nombres si coincide la cantidad de columnas
    if len(df.columns) == len(nuevos_nombres):
        df.columns = nuevos_nombres
        print("✅ Nombres de las 44 columnas estandarizados con éxito.")
    else:
        print(f"⚠️ Advertencia: El dataset tiene {len(df.columns)} columnas y el script esperaba {len(nuevos_nombres)}.")

    # 3. Limpieza básica y columna derivada de edad
    df["edad"] = pd.to_numeric(df["edad"], errors="coerce")

    def definir_rango_edad(edad):
        if pd.isna(edad):
            return "No registra"
        elif edad < 30:
            return "Joven (18-29 años)"
        elif edad <= 50:
            return "Adulta (30-50 años)"
        else:
            return "Adulta Mayor (>50 años)"

    df["rango_edad"] = df["edad"].apply(definir_rango_edad)

    # 4. Guardar archivo limpio
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"🎉 ¡Limpieza completada con éxito! Archivo guardado en: '{output_path}'")
    print("\n--- Vista previa de las primeras 3 personas ---")
    print(df[["nombre", "edad", "rango_edad", "nivel_educativo", "situacion_laboral"]].head(3))