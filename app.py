import math
import streamlit as st
import pandas as pd

# 1. Configuración general de la página
st.set_page_config(
    page_title="Calculadora Estructural ASTM A500, Vigas WF y Tubos SCH",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Catálogo Completo (332 Perfiles):
# - 68 Tubos Cuadrados ASTM A500
# - 78 Tubos Rectangulares ASTM A500
# - 156 Vigas H Alas Anchas (WF) Estándar Americano
# - 30 Tubos Redondos Schedule (SCH 40 STD / SCH 80 XS) Sin Costura
CATALOGO_CUADRADOS = [
    {"selector": "20 x 20 | 0.9 mm", "tipo": "Tubo Cuadrado", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_a_mm": 20.0, "lado_b_mm": 20.0, "espesor_mm": 0.9, "espesor_alma_mm": 0.9, "peso_kg_m": 0.49, "peso_6m_ficha": 2.96, "nota": ""},
    {"selector": "20 x 20 | 1.5 mm", "tipo": "Tubo Cuadrado", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_a_mm": 20.0, "lado_b_mm": 20.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 0.86, "peso_6m_ficha": 5.14, "nota": ""},
    {"selector": "20 x 20 | 2 mm", "tipo": "Tubo Cuadrado", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_a_mm": 20.0, "lado_b_mm": 20.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 1.04, "peso_6m_ficha": 6.24, "nota": ""},
    {"selector": "25 x 25 | 1.5 mm", "tipo": "Tubo Cuadrado", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_a_mm": 25.0, "lado_b_mm": 25.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 1.06, "peso_6m_ficha": 6.37, "nota": ""},
    {"selector": "25 x 25 | 2 mm", "tipo": "Tubo Cuadrado", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_a_mm": 25.0, "lado_b_mm": 25.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 1.46, "peso_6m_ficha": 8.76, "nota": ""},
    {"selector": "25 x 25 | 2.5 mm", "tipo": "Tubo Cuadrado", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_a_mm": 25.0, "lado_b_mm": 25.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 1.67, "peso_6m_ficha": 10.02, "nota": ""},
    {"selector": "25 x 25 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_a_mm": 25.0, "lado_b_mm": 25.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 1.93, "peso_6m_ficha": 11.58, "nota": ""},
    {"selector": "30 x 30 | 1.2 mm", "tipo": "Tubo Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30.0, "lado_b_mm": 30.0, "espesor_mm": 1.2, "espesor_alma_mm": 1.2, "peso_kg_m": 1.04, "peso_6m_ficha": 6.24, "nota": ""},
    {"selector": "30 x 30 | 1.5 mm", "tipo": "Tubo Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30.0, "lado_b_mm": 30.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 1.30, "peso_6m_ficha": 7.80, "nota": ""},
    {"selector": "30 x 30 | 1.8 mm", "tipo": "Tubo Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30.0, "lado_b_mm": 30.0, "espesor_mm": 1.8, "espesor_alma_mm": 1.8, "peso_kg_m": 1.68, "peso_6m_ficha": 10.08, "nota": ""},
    {"selector": "30 x 30 | 2 mm", "tipo": "Tubo Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30.0, "lado_b_mm": 30.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 1.86, "peso_6m_ficha": 11.16, "nota": ""},
    {"selector": "30 x 30 | 2.5 mm", "tipo": "Tubo Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30.0, "lado_b_mm": 30.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 2.17, "peso_6m_ficha": 13.02, "nota": ""},
    {"selector": "40 x 40 | 1.5 mm", "tipo": "Tubo Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40.0, "lado_b_mm": 40.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 1.77, "peso_6m_ficha": 10.62, "nota": ""},
    {"selector": "40 x 40 | 1.8 mm", "tipo": "Tubo Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40.0, "lado_b_mm": 40.0, "espesor_mm": 1.8, "espesor_alma_mm": 1.8, "peso_kg_m": 2.03, "peso_6m_ficha": 12.18, "nota": ""},
    {"selector": "40 x 40 | 2 mm", "tipo": "Tubo Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40.0, "lado_b_mm": 40.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 2.24, "peso_6m_ficha": 13.46, "nota": ""},
    {"selector": "40 x 40 | 2.5 mm", "tipo": "Tubo Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40.0, "lado_b_mm": 40.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 2.99, "peso_6m_ficha": 17.94, "nota": ""},
    {"selector": "40 x 40 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40.0, "lado_b_mm": 40.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 3.54, "peso_6m_ficha": 21.24, "nota": ""},
    {"selector": "40 x 40 | 4.5 mm", "tipo": "Tubo Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40.0, "lado_b_mm": 40.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 4.52, "peso_6m_ficha": 27.12, "nota": ""},
    {"selector": "50 x 50 | 1.2 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 1.2, "espesor_alma_mm": 1.2, "peso_kg_m": 1.87, "peso_6m_ficha": 11.24, "nota": ""},
    {"selector": "50 x 50 | 1.5 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 2.25, "peso_6m_ficha": 13.50, "nota": ""},
    {"selector": "50 x 50 | 1.8 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 1.8, "espesor_alma_mm": 1.8, "peso_kg_m": 2.70, "peso_6m_ficha": 16.20, "nota": ""},
    {"selector": "50 x 50 | 2 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 3.12, "peso_6m_ficha": 18.73, "nota": ""},
    {"selector": "50 x 50 | 2.5 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 3.87, "peso_6m_ficha": 23.23, "nota": ""},
    {"selector": "50 x 50 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 4.49, "peso_6m_ficha": 26.94, "nota": ""},
    {"selector": "50 x 50 | 4 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 6.57, "peso_6m_ficha": 39.41, "nota": "Revisar: valor 4 mm (6.57 kg/m) mayor que 4.5 mm (6.02 kg/m)"},
    {"selector": "50 x 50 | 4.5 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 6.02, "peso_6m_ficha": 36.12, "nota": ""},
    {"selector": "50 x 50 | 6 mm", "tipo": "Tubo Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50.0, "lado_b_mm": 50.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 8.54, "peso_6m_ficha": 51.21, "nota": ""},
    {"selector": "60 x 60 | 2 mm", "tipo": "Tubo Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60.0, "lado_b_mm": 60.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 3.56, "peso_6m_ficha": 21.36, "nota": ""},
    {"selector": "60 x 60 | 2.5 mm", "tipo": "Tubo Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60.0, "lado_b_mm": 60.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 4.39, "peso_6m_ficha": 26.34, "nota": ""},
    {"selector": "60 x 60 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60.0, "lado_b_mm": 60.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 5.19, "peso_6m_ficha": 31.14, "nota": ""},
    {"selector": "60 x 60 | 4 mm", "tipo": "Tubo Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60.0, "lado_b_mm": 60.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 7.14, "peso_6m_ficha": 42.86, "nota": ""},
    {"selector": "60 x 60 | 4.5 mm", "tipo": "Tubo Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60.0, "lado_b_mm": 60.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 7.43, "peso_6m_ficha": 44.58, "nota": ""},
    {"selector": "75 x 75 | 1.5 mm", "tipo": "Tubo Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75.0, "lado_b_mm": 75.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 3.41, "peso_6m_ficha": 20.43, "nota": ""},
    {"selector": "75 x 75 | 2 mm", "tipo": "Tubo Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75.0, "lado_b_mm": 75.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 4.50, "peso_6m_ficha": 27.00, "nota": ""},
    {"selector": "75 x 75 | 2.5 mm", "tipo": "Tubo Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75.0, "lado_b_mm": 75.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 5.56, "peso_6m_ficha": 33.36, "nota": ""},
    {"selector": "75 x 75 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75.0, "lado_b_mm": 75.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 6.81, "peso_6m_ficha": 40.86, "nota": ""},
    {"selector": "75 x 75 | 4 mm", "tipo": "Tubo Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75.0, "lado_b_mm": 75.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 8.59, "peso_6m_ficha": 51.54, "nota": ""},
    {"selector": "75 x 75 | 4.5 mm", "tipo": "Tubo Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75.0, "lado_b_mm": 75.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 9.55, "peso_6m_ficha": 57.30, "nota": ""},
    {"selector": "75 x 75 | 6 mm", "tipo": "Tubo Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75.0, "lado_b_mm": 75.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 13.11, "peso_6m_ficha": 78.66, "nota": ""},
    {"selector": "100 x 100 | 2 mm", "tipo": "Tubo Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100.0, "lado_b_mm": 100.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 6.17, "peso_6m_ficha": 36.99, "nota": ""},
    {"selector": "100 x 100 | 2.5 mm", "tipo": "Tubo Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100.0, "lado_b_mm": 100.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 7.68, "peso_6m_ficha": 46.05, "nota": ""},
    {"selector": "100 x 100 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100.0, "lado_b_mm": 100.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 9.20, "peso_6m_ficha": 55.21, "nota": ""},
    {"selector": "100 x 100 | 4 mm", "tipo": "Tubo Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100.0, "lado_b_mm": 100.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 12.17, "peso_6m_ficha": 73.03, "nota": ""},
    {"selector": "100 x 100 | 4.5 mm", "tipo": "Tubo Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100.0, "lado_b_mm": 100.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 13.59, "peso_6m_ficha": 81.56, "nota": ""},
    {"selector": "100 x 100 | 6 mm", "tipo": "Tubo Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100.0, "lado_b_mm": 100.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 16.98, "peso_6m_ficha": 101.88, "nota": ""},
    {"selector": "100 x 100 | 9.5 mm", "tipo": "Tubo Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100.0, "lado_b_mm": 100.0, "espesor_mm": 9.5, "espesor_alma_mm": 9.5, "peso_kg_m": 25.70, "peso_6m_ficha": 154.20, "nota": ""},
    {"selector": "125 x 125 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125.0, "lado_b_mm": 125.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 11.31, "peso_6m_ficha": 67.86, "nota": ""},
    {"selector": "125 x 125 | 4 mm", "tipo": "Tubo Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125.0, "lado_b_mm": 125.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 14.87, "peso_6m_ficha": 89.22, "nota": ""},
    {"selector": "125 x 125 | 4.5 mm", "tipo": "Tubo Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125.0, "lado_b_mm": 125.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 17.17, "peso_6m_ficha": 103.02, "nota": ""},
    {"selector": "125 x 125 | 4.7 mm", "tipo": "Tubo Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125.0, "lado_b_mm": 125.0, "espesor_mm": 4.7, "espesor_alma_mm": 4.7, "peso_kg_m": 17.81, "peso_6m_ficha": 106.86, "nota": ""},
    {"selector": "125 x 125 | 6 mm", "tipo": "Tubo Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125.0, "lado_b_mm": 125.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 21.69, "peso_6m_ficha": 130.14, "nota": ""},
    {"selector": "125 x 125 | 6.35 mm", "tipo": "Tubo Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125.0, "lado_b_mm": 125.0, "espesor_mm": 6.35, "espesor_alma_mm": 6.35, "peso_kg_m": 23.24, "peso_6m_ficha": 139.44, "nota": ""},
    {"selector": "150 x 150 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_a_mm": 150.0, "lado_b_mm": 150.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 13.67, "peso_6m_ficha": 82.02, "nota": ""},
    {"selector": "150 x 150 | 4 mm", "tipo": "Tubo Cuadrado", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_a_mm": 150.0, "lado_b_mm": 150.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 18.01, "peso_6m_ficha": 108.06, "nota": ""},
    {"selector": "150 x 150 | 4.5 mm", "tipo": "Tubo Cuadrado", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_a_mm": 150.0, "lado_b_mm": 150.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 20.80, "peso_6m_ficha": 124.80, "nota": ""},
    {"selector": "150 x 150 | 6 mm", "tipo": "Tubo Cuadrado", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_a_mm": 150.0, "lado_b_mm": 150.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 27.39, "peso_6m_ficha": 164.32, "nota": ""},
    {"selector": "200 x 200 | 3 mm", "tipo": "Tubo Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200.0, "lado_b_mm": 200.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 18.63, "peso_6m_ficha": 111.76, "nota": ""},
    {"selector": "200 x 200 | 4 mm", "tipo": "Tubo Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200.0, "lado_b_mm": 200.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 24.29, "peso_6m_ficha": 145.74, "nota": ""},
    {"selector": "200 x 200 | 4.5 mm", "tipo": "Tubo Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200.0, "lado_b_mm": 200.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 27.77, "peso_6m_ficha": 166.64, "nota": ""},
    {"selector": "200 x 200 | 4.7 mm", "tipo": "Tubo Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200.0, "lado_b_mm": 200.0, "espesor_mm": 4.7, "espesor_alma_mm": 4.7, "peso_kg_m": 29.21, "peso_6m_ficha": 175.26, "nota": ""},
    {"selector": "200 x 200 | 6 mm", "tipo": "Tubo Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200.0, "lado_b_mm": 200.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 35.82, "peso_6m_ficha": 214.92, "nota": ""},
    {"selector": "200 x 200 | 8 mm", "tipo": "Tubo Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200.0, "lado_b_mm": 200.0, "espesor_mm": 8.0, "espesor_alma_mm": 8.0, "peso_kg_m": 48.68, "peso_6m_ficha": 292.10, "nota": ""},
    {"selector": "200 x 200 | 9 mm", "tipo": "Tubo Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200.0, "lado_b_mm": 200.0, "espesor_mm": 9.0, "espesor_alma_mm": 9.0, "peso_kg_m": 52.34, "peso_6m_ficha": 314.04, "nota": ""},
    {"selector": "200 x 200 | 9.5 mm", "tipo": "Tubo Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200.0, "lado_b_mm": 200.0, "espesor_mm": 9.5, "espesor_alma_mm": 9.5, "peso_kg_m": 56.08, "peso_6m_ficha": 336.48, "nota": ""},
    {"selector": "250 x 250 | 4.7 mm", "tipo": "Tubo Cuadrado", "perfil": "250 x 250", "equiv_pulg": '10" x 10"', "lado_a_mm": 250.0, "lado_b_mm": 250.0, "espesor_mm": 4.7, "espesor_alma_mm": 4.7, "peso_kg_m": 36.86, "peso_6m_ficha": 221.14, "nota": ""},
    {"selector": "250 x 250 | 6 mm", "tipo": "Tubo Cuadrado", "perfil": "250 x 250", "equiv_pulg": '10" x 10"', "lado_a_mm": 250.0, "lado_b_mm": 250.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 45.24, "peso_6m_ficha": 271.44, "nota": ""},
    {"selector": "300 x 300 | 6 mm", "tipo": "Tubo Cuadrado", "perfil": "300 x 300", "equiv_pulg": '12" x 12"', "lado_a_mm": 300.0, "lado_b_mm": 300.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 54.66, "peso_6m_ficha": 327.96, "nota": ""},
    {"selector": "300 x 300 | 8 mm", "tipo": "Tubo Cuadrado", "perfil": "300 x 300", "equiv_pulg": '12" x 12"', "lado_a_mm": 300.0, "lado_b_mm": 300.0, "espesor_mm": 8.0, "espesor_alma_mm": 8.0, "peso_kg_m": 73.82, "peso_6m_ficha": 442.90, "nota": ""},
]

CATALOGO_RECTANGULARES = [
    {"selector": "20 x 40 | 1.5 mm", "tipo": "Tubo Rectangular", "perfil": "20 x 40", "equiv_pulg": '3/4" x 1 1/2"', "lado_a_mm": 20.0, "lado_b_mm": 40.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 1.35, "peso_6m_ficha": 8.12, "nota": ""},
    {"selector": "20 x 40 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "20 x 40", "equiv_pulg": '3/4" x 1 1/2"', "lado_a_mm": 20.0, "lado_b_mm": 40.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 1.70, "peso_6m_ficha": 10.20, "nota": ""},
    {"selector": "20 x 50 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "20 x 50", "equiv_pulg": '3/4" x 2"', "lado_a_mm": 20.0, "lado_b_mm": 50.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 2.10, "peso_6m_ficha": 12.60, "nota": ""},
    {"selector": "25 x 50 | 1.2 mm", "tipo": "Tubo Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25.0, "lado_b_mm": 50.0, "espesor_mm": 1.2, "espesor_alma_mm": 1.2, "peso_kg_m": 1.34, "peso_6m_ficha": 8.04, "nota": ""},
    {"selector": "25 x 50 | 1.5 mm", "tipo": "Tubo Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25.0, "lado_b_mm": 50.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 1.65, "peso_6m_ficha": 9.90, "nota": ""},
    {"selector": "25 x 50 | 1.8 mm", "tipo": "Tubo Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25.0, "lado_b_mm": 50.0, "espesor_mm": 1.8, "espesor_alma_mm": 1.8, "peso_kg_m": 2.07, "peso_6m_ficha": 12.42, "nota": ""},
    {"selector": "25 x 50 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25.0, "lado_b_mm": 50.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 2.26, "peso_6m_ficha": 13.57, "nota": ""},
    {"selector": "25 x 50 | 2.5 mm", "tipo": "Tubo Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25.0, "lado_b_mm": 50.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 2.98, "peso_6m_ficha": 17.87, "nota": ""},
    {"selector": "25 x 50 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25.0, "lado_b_mm": 50.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 3.35, "peso_6m_ficha": 20.09, "nota": ""},
    {"selector": "40 x 50 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 50", "equiv_pulg": "—", "lado_a_mm": 40.0, "lado_b_mm": 50.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 2.62, "peso_6m_ficha": 15.72, "nota": ""},
    {"selector": "40 x 60 | 1.2 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40.0, "lado_b_mm": 60.0, "espesor_mm": 1.2, "espesor_alma_mm": 1.2, "peso_kg_m": 1.82, "peso_6m_ficha": 10.92, "nota": ""},
    {"selector": "40 x 60 | 1.5 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40.0, "lado_b_mm": 60.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 2.26, "peso_6m_ficha": 13.56, "nota": ""},
    {"selector": "40 x 60 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40.0, "lado_b_mm": 60.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 3.03, "peso_6m_ficha": 18.20, "nota": ""},
    {"selector": "40 x 60 | 2.5 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40.0, "lado_b_mm": 60.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 3.60, "peso_6m_ficha": 21.60, "nota": ""},
    {"selector": "40 x 60 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40.0, "lado_b_mm": 60.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 4.25, "peso_6m_ficha": 25.50, "nota": ""},
    {"selector": "40 x 80 | 1.5 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40.0, "lado_b_mm": 80.0, "espesor_mm": 1.5, "espesor_alma_mm": 1.5, "peso_kg_m": 2.71, "peso_6m_ficha": 16.26, "nota": ""},
    {"selector": "40 x 80 | 1.8 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40.0, "lado_b_mm": 80.0, "espesor_mm": 1.8, "espesor_alma_mm": 1.8, "peso_kg_m": 3.29, "peso_6m_ficha": 19.76, "nota": ""},
    {"selector": "40 x 80 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40.0, "lado_b_mm": 80.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 3.66, "peso_6m_ficha": 21.96, "nota": ""},
    {"selector": "40 x 80 | 2.5 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40.0, "lado_b_mm": 80.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 4.39, "peso_6m_ficha": 26.34, "nota": ""},
    {"selector": "40 x 80 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40.0, "lado_b_mm": 80.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 5.19, "peso_6m_ficha": 31.14, "nota": ""},
    {"selector": "40 x 80 | 4 mm", "tipo": "Tubo Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40.0, "lado_b_mm": 80.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 6.92, "peso_6m_ficha": 41.52, "nota": ""},
    {"selector": "50 x 70 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 70", "equiv_pulg": "—", "lado_a_mm": 50.0, "lado_b_mm": 70.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 3.58, "peso_6m_ficha": 21.48, "nota": ""},
    {"selector": "50 x 70 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 70", "equiv_pulg": "—", "lado_a_mm": 50.0, "lado_b_mm": 70.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 5.37, "peso_6m_ficha": 32.22, "nota": ""},
    {"selector": "50 x 75 | 1.8 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50.0, "lado_b_mm": 75.0, "espesor_mm": 1.8, "espesor_alma_mm": 1.8, "peso_kg_m": 3.25, "peso_6m_ficha": 19.52, "nota": ""},
    {"selector": "50 x 75 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50.0, "lado_b_mm": 75.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 3.95, "peso_6m_ficha": 23.68, "nota": ""},
    {"selector": "50 x 75 | 2.5 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50.0, "lado_b_mm": 75.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 4.88, "peso_6m_ficha": 29.28, "nota": ""},
    {"selector": "50 x 75 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50.0, "lado_b_mm": 75.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 5.42, "peso_6m_ficha": 32.54, "nota": ""},
    {"selector": "50 x 75 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50.0, "lado_b_mm": 75.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 7.98, "peso_6m_ficha": 47.88, "nota": ""},
    {"selector": "50 x 75 | 4.7 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50.0, "lado_b_mm": 75.0, "espesor_mm": 4.7, "espesor_alma_mm": 4.7, "peso_kg_m": 8.33, "peso_6m_ficha": 50.00, "nota": ""},
    {"selector": "50 x 75 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50.0, "lado_b_mm": 75.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 10.85, "peso_6m_ficha": 65.08, "nota": ""},
    {"selector": "50 x 100 | 1.8 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50.0, "lado_b_mm": 100.0, "espesor_mm": 1.8, "espesor_alma_mm": 1.8, "peso_kg_m": 3.96, "peso_6m_ficha": 23.76, "nota": ""},
    {"selector": "50 x 100 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50.0, "lado_b_mm": 100.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 4.50, "peso_6m_ficha": 27.00, "nota": ""},
    {"selector": "50 x 100 | 2.5 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50.0, "lado_b_mm": 100.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 5.56, "peso_6m_ficha": 33.36, "nota": ""},
    {"selector": "50 x 100 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50.0, "lado_b_mm": 100.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 6.85, "peso_6m_ficha": 41.07, "nota": ""},
    {"selector": "50 x 100 | 4 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50.0, "lado_b_mm": 100.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 8.59, "peso_6m_ficha": 51.54, "nota": ""},
    {"selector": "50 x 100 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50.0, "lado_b_mm": 100.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 9.90, "peso_6m_ficha": 59.40, "nota": ""},
    {"selector": "50 x 100 | 4.7 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50.0, "lado_b_mm": 100.0, "espesor_mm": 4.7, "espesor_alma_mm": 4.7, "peso_kg_m": 10.22, "peso_6m_ficha": 61.33, "nota": ""},
    {"selector": "50 x 100 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50.0, "lado_b_mm": 100.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 13.20, "peso_6m_ficha": 79.20, "nota": ""},
    {"selector": "50 x 125 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 125", "equiv_pulg": '2" x 5"', "lado_a_mm": 50.0, "lado_b_mm": 125.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 5.44, "peso_6m_ficha": 32.64, "nota": ""},
    {"selector": "50 x 125 | 2.5 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 125", "equiv_pulg": '2" x 5"', "lado_a_mm": 50.0, "lado_b_mm": 125.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 6.80, "peso_6m_ficha": 40.80, "nota": ""},
    {"selector": "50 x 125 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 125", "equiv_pulg": '2" x 5"', "lado_a_mm": 50.0, "lado_b_mm": 125.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 8.16, "peso_6m_ficha": 48.96, "nota": ""},
    {"selector": "50 x 150 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50.0, "lado_b_mm": 150.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 6.18, "peso_6m_ficha": 37.10, "nota": ""},
    {"selector": "50 x 150 | 2.5 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50.0, "lado_b_mm": 150.0, "espesor_mm": 2.5, "espesor_alma_mm": 2.5, "peso_kg_m": 7.70, "peso_6m_ficha": 46.19, "nota": ""},
    {"selector": "50 x 150 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50.0, "lado_b_mm": 150.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 9.17, "peso_6m_ficha": 55.04, "nota": ""},
    {"selector": "50 x 150 | 4 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50.0, "lado_b_mm": 150.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 11.73, "peso_6m_ficha": 70.38, "nota": ""},
    {"selector": "50 x 150 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50.0, "lado_b_mm": 150.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 13.76, "peso_6m_ficha": 82.56, "nota": ""},
    {"selector": "50 x 150 | 4.7 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50.0, "lado_b_mm": 150.0, "espesor_mm": 4.7, "espesor_alma_mm": 4.7, "peso_kg_m": 14.37, "peso_6m_ficha": 86.23, "nota": ""},
    {"selector": "50 x 150 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50.0, "lado_b_mm": 150.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 18.26, "peso_6m_ficha": 109.56, "nota": ""},
    {"selector": "50 x 200 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 200", "equiv_pulg": '2" x 8"', "lado_a_mm": 50.0, "lado_b_mm": 200.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 11.75, "peso_6m_ficha": 70.50, "nota": ""},
    {"selector": "50 x 200 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "50 x 200", "equiv_pulg": '2" x 8"', "lado_a_mm": 50.0, "lado_b_mm": 200.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 17.45, "peso_6m_ficha": 104.70, "nota": ""},
    {"selector": "75 x 100 | 2 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75.0, "lado_b_mm": 100.0, "espesor_mm": 2.0, "espesor_alma_mm": 2.0, "peso_kg_m": 5.44, "peso_6m_ficha": 32.64, "nota": ""},
    {"selector": "75 x 100 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75.0, "lado_b_mm": 100.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 8.16, "peso_6m_ficha": 48.96, "nota": ""},
    {"selector": "75 x 100 | 4 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75.0, "lado_b_mm": 100.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 10.88, "peso_6m_ficha": 65.28, "nota": ""},
    {"selector": "75 x 100 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75.0, "lado_b_mm": 100.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 12.07, "peso_6m_ficha": 72.42, "nota": ""},
    {"selector": "75 x 100 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75.0, "lado_b_mm": 100.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 15.87, "peso_6m_ficha": 95.22, "nota": ""},
    {"selector": "75 x 125 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 125", "equiv_pulg": '3" x 5"', "lado_a_mm": 75.0, "lado_b_mm": 125.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 17.96, "peso_6m_ficha": 107.75, "nota": ""},
    {"selector": "75 x 150 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 150", "equiv_pulg": '3" x 6"', "lado_a_mm": 75.0, "lado_b_mm": 150.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 10.55, "peso_6m_ficha": 63.30, "nota": ""},
    {"selector": "75 x 200 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 200", "equiv_pulg": '3" x 8"', "lado_a_mm": 75.0, "lado_b_mm": 200.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 12.94, "peso_6m_ficha": 77.64, "nota": ""},
    {"selector": "75 x 200 | 4.7 mm", "tipo": "Tubo Rectangular", "perfil": "75 x 200", "equiv_pulg": '3" x 8"', "lado_a_mm": 75.0, "lado_b_mm": 200.0, "espesor_mm": 4.7, "espesor_alma_mm": 4.7, "peso_kg_m": 20.27, "peso_6m_ficha": 121.64, "nota": ""},
    {"selector": "100 x 150 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100.0, "lado_b_mm": 150.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 11.56, "peso_6m_ficha": 69.34, "nota": ""},
    {"selector": "100 x 150 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100.0, "lado_b_mm": 150.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 17.17, "peso_6m_ficha": 103.02, "nota": ""},
    {"selector": "100 x 150 | 4.7 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100.0, "lado_b_mm": 150.0, "espesor_mm": 4.7, "espesor_alma_mm": 4.7, "peso_kg_m": 17.00, "peso_6m_ficha": 102.00, "nota": "Revisar: en catálogo 4.7 mm (17.00 kg/m) es menor que 4.5 mm (17.17 kg/m)"},
    {"selector": "100 x 150 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100.0, "lado_b_mm": 150.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 21.70, "peso_6m_ficha": 130.20, "nota": ""},
    {"selector": '100 x 150 | 5/16" (7.94 mm)', "tipo": "Tubo Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100.0, "lado_b_mm": 150.0, "espesor_mm": 7.94, "espesor_alma_mm": 7.94, "peso_kg_m": 28.39, "peso_6m_ficha": 170.34, "nota": ""},
    {"selector": "100 x 200 | 3 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100.0, "lado_b_mm": 200.0, "espesor_mm": 3.0, "espesor_alma_mm": 3.0, "peso_kg_m": 13.91, "peso_6m_ficha": 83.48, "nota": ""},
    {"selector": "100 x 200 | 4 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100.0, "lado_b_mm": 200.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 18.45, "peso_6m_ficha": 110.72, "nota": ""},
    {"selector": "100 x 200 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100.0, "lado_b_mm": 200.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 20.70, "peso_6m_ficha": 124.22, "nota": ""},
    {"selector": "100 x 200 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100.0, "lado_b_mm": 200.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 26.40, "peso_6m_ficha": 158.40, "nota": ""},
    {"selector": "100 x 200 | 8 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100.0, "lado_b_mm": 200.0, "espesor_mm": 8.0, "espesor_alma_mm": 8.0, "peso_kg_m": 34.38, "peso_6m_ficha": 206.28, "nota": ""},
    {"selector": "100 x 200 | 9.3 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100.0, "lado_b_mm": 200.0, "espesor_mm": 9.3, "espesor_alma_mm": 9.3, "peso_kg_m": 40.92, "peso_6m_ficha": 245.52, "nota": ""},
    {"selector": "100 x 250 | 4 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 250", "equiv_pulg": '4" x 10"', "lado_a_mm": 100.0, "lado_b_mm": 250.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 21.60, "peso_6m_ficha": 129.57, "nota": ""},
    {"selector": "100 x 250 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 250", "equiv_pulg": '4" x 10"', "lado_a_mm": 100.0, "lado_b_mm": 250.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 24.24, "peso_6m_ficha": 145.43, "nota": ""},
    {"selector": "100 x 250 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "100 x 250", "equiv_pulg": '4" x 10"', "lado_a_mm": 100.0, "lado_b_mm": 250.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 31.10, "peso_6m_ficha": 186.60, "nota": ""},
    {"selector": "150 x 200 | 4 mm", "tipo": "Tubo Rectangular", "perfil": "150 x 200", "equiv_pulg": '6" x 8"', "lado_a_mm": 150.0, "lado_b_mm": 200.0, "espesor_mm": 4.0, "espesor_alma_mm": 4.0, "peso_kg_m": 21.15, "peso_6m_ficha": 126.90, "nota": ""},
    {"selector": "150 x 200 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "150 x 200", "equiv_pulg": '6" x 8"', "lado_a_mm": 150.0, "lado_b_mm": 200.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 23.68, "peso_6m_ficha": 142.08, "nota": ""},
    {"selector": "150 x 200 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "150 x 200", "equiv_pulg": '6" x 8"', "lado_a_mm": 150.0, "lado_b_mm": 200.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 31.10, "peso_6m_ficha": 186.60, "nota": ""},
    {"selector": "150 x 250 | 6 mm", "tipo": "Tubo Rectangular", "perfil": "150 x 250", "equiv_pulg": '6" x 10"', "lado_a_mm": 150.0, "lado_b_mm": 250.0, "espesor_mm": 6.0, "espesor_alma_mm": 6.0, "peso_kg_m": 35.80, "peso_6m_ficha": 214.80, "nota": ""},
    {"selector": "150 x 300 | 4.5 mm", "tipo": "Tubo Rectangular", "perfil": "150 x 300", "equiv_pulg": '6" x 12"', "lado_a_mm": 150.0, "lado_b_mm": 300.0, "espesor_mm": 4.5, "espesor_alma_mm": 4.5, "peso_kg_m": 30.75, "peso_6m_ficha": 184.50, "nota": ""},
]

DATOS_RAW_WF = [
    ('4"', 13.00, 4.16, 4.06, 8.76, 7.11), ('6"', 9.00, 5.90, 3.94, 5.46, 4.32), ('6"', 12.00, 6.03, 4.00, 7.11, 5.84),
    ('6"', 16.00, 6.28, 4.03, 10.29, 6.60), ('6"', 15.00, 5.99, 5.99, 6.60, 5.84), ('6"', 20.00, 6.20, 6.02, 9.27, 6.60),
    ('6"', 25.00, 6.38, 6.08, 11.56, 8.13), ('8"', 10.00, 7.89, 3.94, 5.21, 4.32), ('8"', 13.00, 7.99, 4.00, 6.48, 5.84),
    ('8"', 15.00, 8.11, 4.02, 8.00, 6.22), ('8"', 18.00, 8.14, 5.25, 8.38, 5.84), ('8"', 21.00, 8.28, 5.27, 10.16, 6.35),
    ('8"', 24.00, 7.93, 6.50, 10.16, 6.22), ('8"', 28.00, 8.06, 6.54, 11.81, 7.24), ('8"', 31.00, 8.00, 8.00, 11.05, 7.24),
    ('8"', 35.00, 8.12, 8.02, 12.57, 7.87), ('8"', 40.00, 8.25, 8.07, 14.22, 9.14), ('8"', 48.00, 8.50, 8.11, 17.40, 10.16),
    ('8"', 58.00, 8.75, 8.22, 20.57, 12.95), ('8"', 67.00, 9.00, 8.28, 23.75, 14.48), ('10"', 12.00, 9.87, 3.96, 5.33, 4.83),
    ('10"', 15.00, 9.99, 4.00, 6.86, 5.84), ('10"', 17.00, 10.11, 4.01, 8.38, 6.10), ('10"', 19.00, 10.24, 4.02, 10.03, 6.35),
    ('10"', 22.00, 10.17, 5.75, 9.14, 6.10), ('10"', 26.00, 10.33, 5.77, 11.18, 6.60), ('10"', 30.00, 10.47, 5.81, 12.95, 7.62),
    ('10"', 33.00, 9.73, 7.96, 11.05, 7.37), ('10"', 39.00, 9.92, 7.99, 13.46, 8.00), ('10"', 45.00, 10.10, 8.02, 15.75, 8.89),
    ('10"', 49.00, 9.98, 10.00, 14.22, 8.64), ('10"', 54.00, 10.09, 10.03, 15.62, 9.40), ('10"', 60.00, 10.22, 10.08, 17.27, 10.67),
    ('10"', 68.00, 10.40, 10.13, 19.56, 11.94), ('10"', 77.00, 10.40, 10.19, 22.10, 13.46), ('10"', 88.00, 10.84, 10.27, 25.15, 15.37),
    ('10"', 100.00, 11.10, 10.34, 28.45, 17.27), ('12"', 14.00, 11.91, 3.97, 5.72, 5.08), ('12"', 16.00, 11.99, 3.99, 6.73, 5.59),
    ('12"', 19.00, 12.16, 4.01, 8.89, 5.97), ('12"', 22.00, 12.31, 4.03, 10.80, 6.60), ('12"', 26.00, 12.22, 6.49, 9.65, 5.84),
    ('12"', 30.00, 12.34, 6.52, 11.18, 6.60), ('12"', 35.00, 12.50, 6.56, 13.21, 7.62), ('12"', 40.00, 11.94, 8.01, 13.08, 7.49),
    ('12"', 45.00, 12.06, 8.05, 14.61, 8.51), ('12"', 50.00, 12.19, 8.08, 16.26, 9.40), ('12"', 53.00, 12.06, 10.00, 14.61, 8.76),
    ('12"', 58.00, 12.19, 10.01, 16.26, 9.14), ('12"', 65.00, 12.12, 12.00, 15.37, 9.91), ('12"', 72.00, 12.25, 12.04, 17.02, 10.92),
    ('12"', 79.00, 12.38, 12.08, 18.67, 11.94), ('12"', 87.00, 12.53, 12.13, 20.57, 13.08), ('12"', 96.00, 12.71, 12.16, 22.86, 13.97),
    ('12"', 106.00, 12.89, 12.22, 25.15, 15.49), ('12"', 120.00, 13.12, 12.32, 28.07, 18.03), ('12"', 136.00, 13.41, 12.40, 31.75, 20.07),
    ('12"', 152.00, 13.71, 12.48, 35.56, 22.10), ('14"', 22.00, 13.74, 5.00, 8.51, 5.84), ('14"', 26.00, 13.91, 5.03, 10.67, 6.48),
    ('14"', 30.00, 13.84, 6.73, 9.78, 6.86), ('14"', 34.00, 13.98, 6.75, 11.56, 7.24), ('14"', 38.00, 14.10, 6.77, 13.08, 7.87),
    ('14"', 43.00, 13.66, 8.00, 13.46, 7.75), ('14"', 48.00, 13.79, 8.03, 15.11, 8.64), ('14"', 53.00, 13.92, 8.06, 16.76, 9.40),
    ('14"', 61.00, 13.89, 10.00, 16.38, 9.53), ('14"', 68.00, 14.04, 10.04, 18.29, 10.54), ('14"', 74.00, 14.17, 10.07, 19.94, 11.43),
    ('14"', 82.00, 14.31, 10.13, 21.72, 12.95), ('14"', 90.00, 14.02, 14.52, 21.72, 11.18), ('14"', 99.00, 14.16, 14.57, 19.81, 12.32),
    ('14"', 109.00, 14.32, 14.61, 21.84, 13.34), ('14"', 120.00, 14.48, 14.67, 23.88, 14.99), ('14"', 132.00, 14.66, 14.73, 26.16, 16.38),
    ('14"', 145.00, 14.78, 15.50, 27.69, 17.27), ('14"', 159.00, 14.98, 15.57, 30.23, 18.92), ('14"', 176.00, 15.22, 15.65, 33.27, 21.08),
    ('14"', 193.00, 15.48, 15.71, 36.58, 22.61), ('16"', 26.00, 15.69, 5.50, 8.76, 6.35), ('16"', 31.00, 15.88, 5.53, 11.18, 6.99),
    ('16"', 36.00, 15.86, 6.99, 10.92, 7.49), ('16"', 40.00, 16.01, 7.00, 12.83, 7.75), ('16"', 45.00, 16.13, 7.04, 14.35, 8.76),
    ('16"', 50.00, 16.26, 7.07, 16.00, 9.65), ('16"', 57.00, 16.43, 7.12, 18.16, 10.92), ('16"', 67.00, 16.33, 10.24, 16.89, 10.03),
    ('16"', 77.00, 16.52, 10.30, 19.30, 11.56), ('16"', 89.00, 16.75, 10.37, 22.23, 13.34), ('16"', 100.00, 16.97, 10.43, 25.02, 14.86),
    ('18"', 35.00, 17.70, 6.00, 10.80, 7.62), ('18"', 40.00, 17.90, 6.02, 13.34, 8.00), ('18"', 46.00, 18.06, 6.06, 15.37, 9.14),
    ('18"', 50.00, 17.99, 7.50, 14.48, 9.02), ('18"', 55.00, 18.11, 7.53, 16.00, 9.91), ('18"', 60.00, 18.24, 7.56, 17.65, 10.54),
    ('18"', 65.00, 18.35, 7.59, 19.05, 11.43), ('18"', 71.00, 18.47, 7.64, 20.57, 12.57), ('18"', 76.00, 18.21, 11.04, 17.27, 10.80),
    ('18"', 86.00, 18.39, 11.09, 19.56, 12.19), ('18"', 97.00, 18.59, 11.15, 22.10, 13.59), ('18"', 106.00, 18.73, 11.20, 23.88, 14.99),
    ('18"', 130.00, 19.25, 11.16, 30.48, 17.02), ('18"', 158.00, 19.72, 11.30, 36.58, 20.57), ('21"', 44.00, 20.66, 6.50, 11.43, 8.89),
    ('21"', 50.00, 20.83, 6.53, 13.59, 9.65), ('21"', 55.00, 20.80, 8.22, 13.26, 9.53), ('21"', 57.00, 21.06, 6.56, 16.51, 10.29),
    ('21"', 62.00, 20.99, 8.24, 15.62, 10.16), ('21"', 68.00, 21.13, 8.27, 17.40, 10.92), ('21"', 73.00, 21.24, 8.30, 18.80, 11.56),
    ('21"', 83.00, 21.43, 8.36, 21.21, 13.08), ('21"', 93.00, 21.62, 8.42, 23.62, 14.73), ('21"', 101.00, 21.36, 12.29, 20.32, 12.70),
    ('21"', 111.00, 21.51, 12.34, 22.23, 13.97), ('21"', 122.00, 21.68, 12.39, 24.38, 15.24), ('21"', 132.00, 21.83, 12.44, 26.29, 16.51),
    ('21"', 147.00, 22.06, 12.51, 29.21, 18.29), ('21"', 166.00, 22.48, 12.42, 34.54, 19.05), ('21"', 201.00, 23.03, 12.58, 41.40, 23.11),
    ('24"', 55.00, 23.57, 7.01, 12.83, 10.03), ('24"', 62.00, 23.74, 7.04, 14.99, 10.92), ('24"', 68.00, 23.73, 8.97, 14.86, 10.54),
    ('24"', 76.00, 23.92, 8.99, 17.27, 11.18), ('24"', 84.00, 24.10, 9.02, 19.56, 11.94), ('24"', 94.00, 24.31, 9.07, 22.23, 13.08),
    ('24"', 104.00, 24.06, 12.75, 19.05, 12.70), ('24"', 117.00, 24.26, 12.80, 21.59, 13.97), ('24"', 131.00, 24.48, 12.86, 24.38, 15.37),
    ('24"', 146.00, 24.74, 12.90, 27.69, 16.51), ('24"', 162.00, 25.00, 12.96, 30.99, 17.91), ('24"', 176.00, 25.24, 12.89, 34.04, 19.05),
    ('24"', 192.00, 25.47, 12.95, 37.08, 20.57), ('24"', 250.00, 26.34, 13.19, 48.01, 26.42), ('27"', 84.00, 26.71, 9.96, 16.26, 11.68),
    ('27"', 94.00, 26.92, 9.99, 18.92, 12.45), ('27"', 102.00, 27.09, 10.02, 21.08, 13.08), ('27"', 114.00, 27.29, 10.07, 23.62, 14.48),
    ('27"', 129.00, 27.63, 10.01, 27.94, 15.49), ('27"', 161.00, 27.59, 14.02, 27.43, 16.76), ('27"', 235.00, 28.66, 14.19, 40.89, 23.11),
    ('27"', 307.00, 29.61, 14.45, 53.09, 29.46), ('30"', 90.00, 29.53, 10.40, 15.49, 11.94), ('30"', 99.00, 29.65, 10.45, 17.02, 13.21),
    ('30"', 108.00, 29.83, 10.48, 19.30, 13.84), ('30"', 116.00, 30.01, 10.50, 21.59, 14.35), ('30"', 124.00, 30.17, 10.52, 23.62, 14.86),
    ('30"', 132.00, 30.31, 10.55, 25.40, 15.62), ('30"', 148.00, 30.67, 10.48, 29.97, 16.51), ('33"', 118.00, 32.86, 11.48, 18.80, 13.97),
    ('33"', 152.00, 33.49, 11.57, 26.80, 16.13), ('33"', 169.00, 33.82, 11.50, 30.99, 17.02), ('36"', 150.00, 35.85, 11.98, 23.88, 15.88),
    ('36"', 160.00, 36.01, 12.00, 25.91, 16.51), ('36"', 194.00, 36.49, 12.12, 32.00, 19.43), ('36"', 232.00, 37.12, 12.12, 39.88, 22.10),
]

DATOS_RAW_SCH = [
    ('1/2"', 0.84, 21.3, 0.11, 2.77, 1.27, 'STD', '40', 700),
    ('1/2"', 0.84, 21.3, 0.15, 3.73, 1.62, 'XS', '80', 850),
    ('3/4"', 1.05, 26.7, 0.11, 2.87, 1.69, 'STD', '40', 700),
    ('3/4"', 1.05, 26.7, 0.15, 3.91, 2.20, 'XS', '80', 850),
    ('1"', 1.32, 33.4, 0.13, 3.38, 2.50, 'STD', '40', 700),
    ('1"', 1.32, 33.4, 0.18, 4.55, 3.24, 'XS', '80', 850),
    ('1 1/4"', 1.66, 42.2, 0.14, 3.56, 3.39, 'STD', '40', 1300),
    ('1 1/4"', 1.66, 42.2, 0.19, 4.85, 4.47, 'XS', '80', 1900),
    ('1 1/2"', 1.90, 48.3, 0.15, 3.68, 4.05, 'STD', '40', 1300),
    ('1 1/2"', 1.90, 48.3, 0.20, 5.08, 5.41, 'XS', '80', 1900),
    ('2"', 2.38, 60.3, 0.15, 3.91, 5.44, 'STD', '40', 2500),
    ('2"', 2.38, 60.3, 0.22, 5.54, 7.48, 'XS', '80', 2500),
    ('2 1/2"', 2.88, 73.0, 0.20, 5.16, 8.63, 'STD', '40', 2500),
    ('2 1/2"', 2.88, 73.0, 0.28, 7.01, 11.41, 'XS', '80', 2500),
    ('3"', 3.50, 88.9, 0.22, 5.49, 11.29, 'STD', '40', 2500),
    ('3"', 3.50, 88.9, 0.30, 7.62, 15.27, 'XS', '80', 2500),
    ('4"', 4.50, 114.3, 0.24, 6.02, 16.07, 'STD', '40', 2210),
    ('4"', 4.50, 114.3, 0.34, 8.56, 22.32, 'XS', '80', 2800),
    ('5"', 5.56, 141.3, 0.26, 6.55, 21.77, 'STD', '40', 1950),
    ('5"', 5.56, 141.3, 0.38, 9.52, 30.94, 'XS', '80', 2800),
    ('6"', 6.63, 168.3, 0.28, 7.11, 28.26, 'STD', '40', 1780),
    ('6"', 6.63, 168.3, 0.43, 10.97, 42.56, 'XS', '80', 2740),
    ('8"', 8.63, 219.1, 0.32, 8.18, 42.55, 'STD', '40', 1570),
    ('8"', 8.63, 219.1, 0.50, 12.70, 64.64, 'XS', '80', 2430),
    ('10"', 10.75, 273.0, 0.37, 9.27, 60.29, 'STD', '40', 1430),
    ('10"', 10.75, 273.0, 0.59, 15.09, 95.97, 'XS', '80', 2320),
    ('12"', 12.75, 323.8, 0.41, 10.31, 79.70, 'STD', '40', 1340),
    ('12"', 12.75, 323.8, 0.69, 17.48, 132.04, 'XS', '80', 2270),
    ('14"', 14.00, 355.6, 0.44, 11.13, 94.55, 'STD', '40', 1310),
    ('14"', 14.00, 355.6, 0.75, 19.05, 158.10, 'XS', '80', 2250),
]

for item in CATALOGO_CUADRADOS + CATALOGO_RECTANGULARES:
    item["peso_6m_calc"] = round(item["peso_kg_m"] * 6.0, 2)
    item["area_m2_m"] = round(2.0 * (item["lado_a_mm"] + item["lado_b_mm"]) / 1000.0, 4)
    item["area_6m_m2"] = round(item["area_m2_m"] * 6.0, 4)

CATALOGO_VIGAS_WF = []
for nom_in, lb_ft, d_in, b_in, tf_mm, tw_mm in DATOS_RAW_WF:
    peso_kg_m = round(lb_ft * 1.48816394, 2)
    d_mm = round(d_in * 25.4, 2)
    b_mm = round(b_in * 25.4, 2)
    area_m2_m = round((2.0 * d_mm + 4.0 * b_mm - 2.0 * tw_mm) / 1000.0, 4)
    selector = f"WF {nom_in} x {int(lb_ft)} lb/pie"
    CATALOGO_VIGAS_WF.append({
        "selector": selector,
        "tipo": "Viga H (WF)",
        "perfil": f"WF {nom_in} x {int(lb_ft)}",
        "equiv_pulg": f'd={d_in}" | b={b_in}" ({int(lb_ft)} lb/pie)',
        "d_pulg": d_in,
        "b_pulg": b_in,
        "peso_lb_pie": lb_ft,
        "lado_a_mm": d_mm,
        "lado_b_mm": b_mm,
        "espesor_mm": tf_mm,
        "espesor_alma_mm": tw_mm,
        "peso_kg_m": peso_kg_m,
        "peso_6m_calc": round(peso_kg_m * 6.0, 2),
        "peso_6m_ficha": round(peso_kg_m * 9.144, 2),
        "area_m2_m": area_m2_m,
        "area_6m_m2": round(area_m2_m * 6.0, 4),
        "nota": f"Espesor Ala (f)={tf_mm} mm | Alma (w)={tw_mm} mm"
    })

CATALOGO_TUBOS_SCH = []
for nom_pulg, od_pulg, od_mm, t_pulg, t_mm, peso_kg_m, peso_tipo, sch_no, presion_psi in DATOS_RAW_SCH:
    area_m2_m = round(math.pi * od_mm / 1000.0, 4)
    extremos = "Planos (< 2\")" if od_pulg < 2.0 else "Biselados (≥ 2\")"
    selector = f'SCH {sch_no} ({peso_tipo}) Ø {nom_pulg} ({od_mm} x {t_mm} mm)'
    CATALOGO_TUBOS_SCH.append({
        "selector": selector,
        "tipo": "Tubo Schedule (SCH)",
        "perfil": f'Ø {nom_pulg} SCH {sch_no}',
        "equiv_pulg": f'Ø {nom_pulg} (OD={od_pulg}" | t={t_pulg}")',
        "nom_pulg": nom_pulg,
        "od_pulg": od_pulg,
        "t_pulg": t_pulg,
        "lado_a_mm": od_mm,
        "lado_b_mm": od_mm,
        "espesor_mm": t_mm,
        "espesor_alma_mm": t_mm,
        "peso_tipo": peso_tipo,
        "sch_no": sch_no,
        "presion_psi": presion_psi,
        "extremos": extremos,
        "peso_kg_m": peso_kg_m,
        "peso_6m_calc": round(peso_kg_m * 6.0, 2),
        "peso_6m_ficha": round(peso_kg_m * 6.0, 2),
        "area_m2_m": area_m2_m,
        "area_6m_m2": round(area_m2_m * 6.0, 4),
        "nota": f"Tipo {peso_tipo} (SCH {sch_no}) | Prueba Grado B: {presion_psi} psi | Extremos: {extremos}"
    })

CATALOGO_TOTAL = CATALOGO_CUADRADOS + CATALOGO_RECTANGULARES + CATALOGO_VIGAS_WF + CATALOGO_TUBOS_SCH
MAPA_PERFILES = {item["selector"]: item for item in CATALOGO_TOTAL}

LISTAS_POR_TIPO = {
    "Tubo Cuadrado": [item["selector"] for item in CATALOGO_CUADRADOS],
    "Tubo Rectangular": [item["selector"] for item in CATALOGO_RECTANGULARES],
    "Viga H (WF)": [item["selector"] for item in CATALOGO_VIGAS_WF],
    "Tubo Schedule (SCH)": [item["selector"] for item in CATALOGO_TUBOS_SCH],
}


# 3. Funciones auxiliares para la Grilla y Croquis de Columnas Individuales ("VISTA SUPERIOR")
def obtener_letras_ejes(n_letras, invertir=True):
    letras = [chr(65 + i) for i in range(max(1, min(26, int(n_letras))))]
    return list(reversed(letras)) if invertir else letras


def obtener_numeros_ejes(n_filas):
    # De arriba hacia abajo: ej. [2, 1] como en el plano CAD adjunto
    return list(range(max(1, int(n_filas)), 0, -1))


def sincronizar_nodos_croquis():
    cfg = st.session_state.config
    letras = obtener_letras_ejes(cfg["grid_num_ejes_letras"], cfg["grid_invertir_letras"])
    numeros = obtener_numeros_ejes(cfg["grid_num_ejes_numeros"])
    nodos_actuales = st.session_state.get("nodos_columnas", {})
    nuevos_nodos = {}

    for num in numeros:
        for letra in letras:
            coord = f"{letra}-{num}"
            if coord in nodos_actuales:
                nuevos_nodos[coord] = nodos_actuales[coord]
            else:
                # Por defecto: Fila superior (ej. Eje 2) Tubo Rectangular 5.20m; Fila inferior (ej. Eje 1) Viga H WF 4.00m
                if num == max(numeros) and len(numeros) > 1:
                    nuevos_nodos[coord] = {
                        "activo": True,
                        "tipo": "Tubo Rectangular",
                        "perfil": "50 x 100 | 2.5 mm",
                        "altura_m": 5.20
                    }
                else:
                    nuevos_nodos[coord] = {
                        "activo": True,
                        "tipo": "Viga H (WF)",
                        "perfil": 'WF 8" x 24 lb/pie',
                        "altura_m": 4.00
                    }
    st.session_state.nodos_columnas = nuevos_nodos
    return letras, numeros


def generar_svg_croquis_columnas(letras_ejes, numeros_ejes, mapa_nodos, ancho_portico_m):
    """
    Dibuja un croquis técnico SVG estilo AutoCAD ("VISTA SUPERIOR") con ejes alfabéticos
    superiores, ejes numéricos laterales, placas base y sección transversal real (I, [], O).
    """
    n_cols = len(letras_ejes)
    n_rows = len(numeros_ejes)

    dx = max(118, min(155, int(980 / max(1, n_cols))))
    dy = 165 if n_rows <= 2 else 135
    margin_left = 90
    margin_right = 55
    margin_top = 80
    margin_bottom = 75

    width = margin_left + max(0, n_cols - 1) * dx + margin_right + 40
    height = margin_top + max(0, n_rows - 1) * dy + margin_bottom + 35

    svg = [
        '<div style="overflow-x:auto; background:#ffffff; border:1px solid #d0d7de; border-radius:8px; padding:12px;">',
        f'<svg viewBox="0 0 {width} {height}" width="100%" style="min-width:{min(width, 760)}px; max-height:580px; font-family: monospace, sans-serif;">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#ffffff"/>'
    ]

    # Líneas verticales de ejes (Letras)
    for i, letra in enumerate(letras_ejes):
        x = margin_left + i * dx
        y_circle = 30
        y_start = 46
        y_end = height - 45
        svg.append(f'<line x1="{x}" y1="{y_start}" x2="{x}" y2="{y_end}" stroke="#6e7781" stroke-width="1.2" stroke-dasharray="12,4,2,4"/>')
        svg.append(f'<circle cx="{x}" cy="{y_circle}" r="15" fill="#ffffff" stroke="#1f2328" stroke-width="1.5"/>')
        svg.append(f'<text x="{x}" y="{y_circle+5}" text-anchor="middle" font-size="14" font-weight="bold" fill="#1f2328">{letra}</text>')

    # Líneas horizontales de ejes (Números)
    for j, num in enumerate(numeros_ejes):
        y = margin_top + j * dy
        x_circle = 30
        x_start = 46
        x_end = width - 25
        svg.append(f'<line x1="{x_start}" y1="{y}" x2="{x_end}" y2="{y}" stroke="#6e7781" stroke-width="1.2" stroke-dasharray="12,4,2,4"/>')
        svg.append(f'<circle cx="{x_circle}" cy="{y}" r="15" fill="#ffffff" stroke="#1f2328" stroke-width="1.5"/>')
        svg.append(f'<text x="{x_circle}" y="{y+5}" text-anchor="middle" font-size="14" font-weight="bold" fill="#1f2328">{num}</text>')

    # Nodos de columna en cada intersección
    for j, num in enumerate(numeros_ejes):
        y = margin_top + j * dy
        for i, letra in enumerate(letras_ejes):
            x = margin_left + i * dx
            coord = f"{letra}-{num}"
            nodo = mapa_nodos.get(coord, {"activo": False})

            if not nodo.get("activo", False):
                svg.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#eaeef2" stroke="#8c959f" stroke-width="1"/>')
                svg.append(f'<text x="{x}" y="{y+22}" text-anchor="middle" font-size="10" fill="#8c959f">{coord} (Sin col.)</text>')
                continue

            tipo = nodo["tipo"]
            partes_p = nodo["perfil"].split("|")
            perfil_corto = partes_p[0].strip()
            espesor_corto = partes_p[1].strip() if len(partes_p) > 1 else ""
            altura = nodo["altura_m"]

            if tipo == "Viga H (WF)":
                color_borde = "#0969da"
                color_fondo = "#ddf4ff"
            elif tipo == "Tubo Rectangular":
                color_borde = "#1a7f37"
                color_fondo = "#dafbe1"
            elif tipo == "Tubo Cuadrado":
                color_borde = "#8250df"
                color_fondo = "#fbefff"
            else:
                color_borde = "#bc4c00"
                color_fondo = "#fff1e5"

            # Placa base exterior cuadrada
            svg.append(f'<rect x="{x-15}" y="{y-15}" width="30" height="30" fill="#ffffff" stroke="#1f2328" stroke-width="1.5"/>')

            # Símbolo interno según geometría del perfil (como en el plano VISTA SUPERIOR)
            if tipo == "Viga H (WF)":
                svg.append(f'<line x1="{x-8}" y1="{y-9}" x2="{x+8}" y2="{y-9}" stroke="{color_borde}" stroke-width="2.6"/>')
                svg.append(f'<line x1="{x-8}" y1="{y+9}" x2="{x+8}" y2="{y+9}" stroke="{color_borde}" stroke-width="2.6"/>')
                svg.append(f'<line x1="{x}" y1="{y-9}" x2="{x}" y2="{y+9}" stroke="{color_borde}" stroke-width="2.4"/>')
            elif tipo == "Tubo Rectangular":
                svg.append(f'<rect x="{x-5.5}" y="{y-9.5}" width="11" height="19" fill="{color_fondo}" stroke="{color_borde}" stroke-width="2.0"/>')
            elif tipo == "Tubo Cuadrado":
                svg.append(f'<rect x="{x-8}" y="{y-8}" width="16" height="16" fill="{color_fondo}" stroke="{color_borde}" stroke-width="2.0"/>')
            else:
                svg.append(f'<circle cx="{x}" cy="{y}" r="8.5" fill="{color_fondo}" stroke="{color_borde}" stroke-width="2.0"/>')

            # Etiqueta técnica debajo del nodo
            svg.append(f'<rect x="{x-48}" y="{y+18}" width="96" height="36" rx="4" fill="{color_fondo}" stroke="{color_borde}" stroke-width="1"/>')
            svg.append(f'<text x="{x}" y="{y+30}" text-anchor="middle" font-size="10.5" font-weight="bold" fill="#1f2328">{coord} | H={altura:.2f}m</text>')
            texto_p = f"{perfil_corto} ({espesor_corto})" if espesor_corto else perfil_corto
            svg.append(f'<text x="{x}" y="{y+43}" text-anchor="middle" font-size="9.2" fill="{color_borde}">{texto_p[:19]}</text>')

    svg.append(
        f'<text x="{width/2}" y="{height-12}" text-anchor="middle" font-size="13.5" font-weight="bold" fill="#1f2328" text-decoration="underline">'
        f'VISTA SUPERIOR — CROQUIS DE UBICACIÓN Y ALTURA DE COLUMNAS (LUZ = {ancho_portico_m:.2f} m)</text>'
    )
    svg.append('</svg></div>')
    return "\n".join(svg)


# 4. Inicialización de Estado (Session State)
if "paso" not in st.session_state:
    st.session_state.paso = 1

if "config" not in st.session_state:
    st.session_state.config = {
        "proyecto": "Estructura de Techo Metálico y Pórticos",
        "largo_tubos_m": 6.00,
        "modo_largo_wf": "30 pies (9.14 m) - Estándar",
        "largo_wf_m": 9.14,
        "modo_largo_sch": "6.00 m (SRL Comercial Estándar)",
        "largo_sch_m": 6.00,
        "ancho_corte_mm": 0.0,
        "num_tijerales": 8,
        "modo_columnas": "individual_croquis",  # 'niveladas', 'desnivel_lados', 'individual_croquis'
        "mismo_perfil_columnas_desnivel": True,
        "ancho_portico_m": 10.00,
        "optimizar_sobrantes_mismo_perfil": True,
        "grid_num_ejes_letras": 8,
        "grid_num_ejes_numeros": 2,
        "grid_invertir_letras": True
    }

if "partidas" not in st.session_state:
    st.session_state.partidas = {
        "columnas_unico": {
            "activo": False, "nombre": "Columnas Principales (Niveladas)", "es_tijeral": False,
            "tipo": "Viga H (WF)", "perfil": 'WF 8" x 24 lb/pie', "cantidad": 16, "longitud_m": 4.50
        },
        "columnas_mayor": {
            "activo": False, "nombre": "Columnas - Lado Mayor (Altura Mayor)", "es_tijeral": False,
            "tipo": "Tubo Rectangular", "perfil": "50 x 100 | 2.5 mm", "cantidad": 8, "longitud_m": 5.20
        },
        "columnas_menor": {
            "activo": False, "nombre": "Columnas - Lado Menor (Altura Menor)", "es_tijeral": False,
            "tipo": "Viga H (WF)", "perfil": 'WF 8" x 24 lb/pie', "cantidad": 8, "longitud_m": 4.00
        },
        "vigas_portico": {
            "activo": False, "nombre": "Vigas Principales / Soleras", "es_tijeral": False,
            "tipo": "Viga H (WF)", "perfil": 'WF 10" x 26 lb/pie', "cantidad": 4, "longitud_m": 9.00
        },
        "correas": {
            "activo": True, "nombre": "Correas de Cobertura", "es_tijeral": False,
            "tipo": "Tubo Rectangular", "perfil": "40 x 80 | 2 mm", "cantidad": 14, "longitud_m": 9.00
        },
        "brida_sup": {
            "activo": True, "nombre": "Tijeral - Brida Superior", "es_tijeral": True,
            "tipo": "Tubo Rectangular", "perfil": "50 x 100 | 2.5 mm", "cantidad": 1, "longitud_m": 10.07
        },
        "brida_inf": {
            "activo": True, "nombre": "Tijeral - Brida Inferior", "es_tijeral": True,
            "tipo": "Tubo Rectangular", "perfil": "50 x 100 | 2.5 mm", "cantidad": 1, "longitud_m": 10.00
        },
    }

if "nodos_columnas" not in st.session_state:
    sincronizar_nodos_croquis()

if "lista_montantes" not in st.session_state:
    st.session_state.lista_montantes = [
        {
            "id": 1, "activo": True, "nombre": "Tijeral - Montante M1 (Mayor)",
            "tipo": "Tubo Rectangular", "perfil": "50 x 100 | 2.5 mm", "cantidad": 2, "longitud_m": 1.15
        },
        {
            "id": 2, "activo": True, "nombre": "Tijeral - Montante M2 (Medio)",
            "tipo": "Tubo Rectangular", "perfil": "50 x 100 | 2.5 mm", "cantidad": 2, "longitud_m": 0.85
        },
        {
            "id": 3, "activo": True, "nombre": "Tijeral - Montante M3 (Menor)",
            "tipo": "Tubo Rectangular", "perfil": "50 x 100 | 2.5 mm", "cantidad": 2, "longitud_m": 0.55
        },
        {
            "id": 4, "activo": True, "nombre": "Tijeral - Diagonales Internas",
            "tipo": "Tubo Cuadrado", "perfil": "40 x 40 | 2 mm", "cantidad": 6, "longitud_m": 1.45
        }
    ]

if "next_montante_id" not in st.session_state:
    st.session_state.next_montante_id = 5


def ir_a_paso(nuevo_paso):
    st.session_state.paso = nuevo_paso


def obtener_largo_comercial_por_tipo(tipo_geometria):
    if tipo_geometria == "Viga H (WF)":
        return st.session_state.config["largo_wf_m"]
    elif tipo_geometria == "Tubo Schedule (SCH)":
        return st.session_state.config["largo_sch_m"]
    return st.session_state.config["largo_tubos_m"]


def calcular_geometria_techo(h_mayor, h_menor, ancho_portico):
    delta_h = abs(h_mayor - h_menor)
    if ancho_portico > 0:
        pendiente_pct = (delta_h / ancho_portico) * 100.0
        angulo_deg = math.degrees(math.atan(delta_h / ancho_portico))
        long_inclinada = math.hypot(ancho_portico, delta_h)
    else:
        pendiente_pct = 0.0
        angulo_deg = 0.0
        long_inclinada = 0.0
    return {
        "delta_h": delta_h,
        "pendiente_pct": pendiente_pct,
        "angulo_deg": angulo_deg,
        "long_inclinada": long_inclinada
    }


def obtener_partidas_columnas_activas():
    """
    Devuelve la lista de partidas de columnas según el modo elegido:
    - 'niveladas'
    - 'desnivel_lados'
    - 'individual_croquis' (agrupando automáticamente las columnas individuales que comparten perfil y altura)
    """
    cfg = st.session_state.config
    modo = cfg["modo_columnas"]
    lista_cols = []

    if modo == "niveladas":
        it = st.session_state.partidas["columnas_unico"]
        if it["activo"]:
            lista_cols.append({
                "nombre": it["nombre"],
                "tipo": it["tipo"],
                "perfil": it["perfil"],
                "cantidad_total": it["cantidad"],
                "longitud_m": it["longitud_m"],
                "largo_barra_m": obtener_largo_comercial_por_tipo(it["tipo"])
            })
    elif modo == "desnivel_lados":
        for k in ["columnas_mayor", "columnas_menor"]:
            it = st.session_state.partidas[k]
            if it["activo"]:
                lista_cols.append({
                    "nombre": it["nombre"],
                    "tipo": it["tipo"],
                    "perfil": it["perfil"],
                    "cantidad_total": it["cantidad"],
                    "longitud_m": it["longitud_m"],
                    "largo_barra_m": obtener_largo_comercial_por_tipo(it["tipo"])
                })
    elif modo == "individual_croquis":
        letras, numeros = sincronizar_nodos_croquis()
        nodos_activos = []
        for num in numeros:
            for letra in letras:
                coord = f"{letra}-{num}"
                nd = st.session_state.nodos_columnas.get(coord, {})
                if nd.get("activo", False):
                    nodos_activos.append({
                        "coord": coord,
                        "tipo": nd["tipo"],
                        "perfil": nd["perfil"],
                        "altura_m": round(float(nd["altura_m"]), 2)
                    })
        if nodos_activos:
            df_n = pd.DataFrame(nodos_activos)
            agrupado = df_n.groupby(["tipo", "perfil", "altura_m"], sort=False, as_index=False).agg(
                cantidad=("coord", "count"),
                ubicaciones=("coord", lambda x: ", ".join(x))
            )
            for _, row in agrupado.iterrows():
                lista_cols.append({
                    "nombre": f"Columnas [{row['ubicaciones']}]",
                    "tipo": row["tipo"],
                    "perfil": row["perfil"],
                    "cantidad_total": int(row["cantidad"]),
                    "longitud_m": float(row["altura_m"]),
                    "largo_barra_m": obtener_largo_comercial_por_tipo(row["tipo"])
                })
    return lista_cols


def mostrar_ficha_resumen_perfil(tipo_perfil, info_p, largo_barra_aplica, metraje_subtotal, nota_extra=""):
    if tipo_perfil == "Viga H (WF)":
        st.caption(
            f"📌 **Ficha Viga H (WF):** `{info_p['equiv_pulg']}` ({info_p['lado_a_mm']:.1f} × {info_p['lado_b_mm']:.1f} mm) | "
            f"{info_p['nota']} | Peso: `{info_p['peso_kg_m']:.2f} kg/m` | "
            f"Área ext.: `{info_p['area_m2_m']:.3f} m²/m` | Barra comercial: `{largo_barra_aplica:.2f} m`"
            f"{nota_extra} | Metraje neto: **{metraje_subtotal:.2f} m**"
        )
    elif tipo_perfil == "Tubo Schedule (SCH)":
        st.caption(
            f"📌 **Ficha Tubo SCH Sin Costura:** `{info_p['equiv_pulg']}` (OD={info_p['lado_a_mm']:.1f} mm, e={info_p['espesor_mm']:.2f} mm) | "
            f"{info_p['nota']} | Peso: `{info_p['peso_kg_m']:.2f} kg/m` | "
            f"Área ext.: `{info_p['area_m2_m']:.4f} m²/m` | Barra comercial: `{largo_barra_aplica:.2f} m`"
            f"{nota_extra} | Metraje neto: **{metraje_subtotal:.2f} m**"
        )
    else:
        st.caption(
            f"📌 **Ficha ASTM A500:** Equiv. `{info_p['equiv_pulg']}` | "
            f"Peso teórico: `{info_p['peso_kg_m']:.2f} kg/m` (`{info_p['peso_6m_ficha']:.2f} kg/barra 6m`) | "
            f"Área ext.: `{info_p['area_m2_m']:.2f} m²/m` | Barra comercial: `{largo_barra_aplica:.2f} m`"
            f"{nota_extra} | Metraje neto: **{metraje_subtotal:.2f} m**"
        )
        if info_p["nota"]:
            st.warning(f"⚠️ {info_p['nota']}")


# 5. Motor de Optimización Global por Perfil (Aprovechamiento de sobrantes entre elementos del mismo perfil)
def ejecutar_metrado_y_optimizacion_global(lista_items_activos, aprovechar_sobrantes=True):
    kerf_m = st.session_state.config["ancho_corte_mm"] / 1000.0

    resumen_individual = []
    for item in lista_items_activos:
        p_info = MAPA_PERFILES[item["perfil"]]
        cant = item["cantidad_total"]
        long_m = item["longitud_m"]
        largo_b = item["largo_barra_m"]
        peso_u = p_info["peso_kg_m"]
        area_u = p_info["area_m2_m"]

        metraje_req = cant * long_m
        tramos_comp_unit = int(long_m // largo_b) if largo_b > 0 else 0
        tramo_res = round(long_m % largo_b, 6) if largo_b > 0 else 0.0
        if abs(tramo_res - largo_b) < 1e-6:
            tramo_res = 0.0
            tramos_comp_unit += 1

        if tramo_res == 0:
            pzas_por_barra_aislado = 0
            barras_cortes_aislado = 0
        else:
            denom = tramo_res + kerf_m
            pzas_por_barra_aislado = int(math.floor((largo_b + kerf_m + 1e-9) / denom)) if denom > 0 else 0
            barras_cortes_aislado = math.ceil(cant / pzas_por_barra_aislado) if pzas_por_barra_aislado > 0 else 0

        barras_comp = tramos_comp_unit * cant
        total_barras_aislado = barras_comp + barras_cortes_aislado
        empalmes = cant * max(0, math.ceil(long_m / largo_b) - 1) if largo_b > 0 else 0
        piezas_totales = cant * (tramos_comp_unit + (1 if tramo_res > 0 else 0))

        resumen_individual.append({
            "Elemento / Ubicación": item["nombre"],
            "Tipo": p_info["tipo"],
            "Perfil": item["perfil"],
            "Equiv. / Dim.": p_info["equiv_pulg"],
            "Largo Barra (m)": round(largo_b, 2),
            "Peso unit. (kg/m)": peso_u,
            "Cant. Elementos": cant,
            "Longitud Final c/u (m)": long_m,
            "Metraje Requerido (m)": round(metraje_req, 2),
            "Tramos Completos/Elem": tramos_comp_unit,
            "Barras Completas": barras_comp,
            "Tramo por Cortar (m)": round(tramo_res, 2),
            "Piezas por Cortar": cant if tramo_res > 0 else 0,
            "Empalmes": empalmes,
            "Piezas Totales": piezas_totales,
            "Peso Requerido (kg)": round(metraje_req * peso_u, 2),
            "Área Requerida (m²)": round(metraje_req * area_u, 2),
            "Barras (Cálculo aislado)": total_barras_aislado,
        })

    df_elementos = pd.DataFrame(resumen_individual)

    perfiles_unicos = []
    for item in lista_items_activos:
        if item["perfil"] not in perfiles_unicos:
            perfiles_unicos.append(item["perfil"])

    consolidado_perfiles = []
    planes_por_perfil = {}
    todos_los_planes_dfs = []

    for perf_sel in perfiles_unicos:
        p_info = MAPA_PERFILES[perf_sel]
        items_perf = [it for it in lista_items_activos if it["perfil"] == perf_sel]
        largo_b = items_perf[0]["largo_barra_m"]
        peso_u = p_info["peso_kg_m"]
        area_u = p_info["area_m2_m"]

        elementos_involucrados = [it["nombre"] for it in items_perf]
        metraje_req_total = sum(it["cantidad_total"] * it["longitud_m"] for it in items_perf)
        empalmes_perfil = sum(
            it["cantidad_total"] * max(0, math.ceil(it["longitud_m"] / largo_b) - 1)
            for it in items_perf
        )
        barras_aisladas_suma = sum(
            row["Barras (Cálculo aislado)"]
            for row in resumen_individual if row["Perfil"] == perf_sel
        )

        filas_plan_perfil = []
        contador_barras = 0
        barras_completas_perfil = 0
        grupos_piezas = []

        for it in items_perf:
            cant = it["cantidad_total"]
            long_m = it["longitud_m"]
            tramos_comp_unit = int(long_m // largo_b) if largo_b > 0 else 0
            tramo_res = round(long_m % largo_b, 6) if largo_b > 0 else 0.0
            if abs(tramo_res - largo_b) < 1e-6:
                tramo_res = 0.0
                tramos_comp_unit += 1

            n_comp = tramos_comp_unit * cant
            if n_comp > 0:
                inicio_b = contador_barras + 1
                fin_b = contador_barras + n_comp
                contador_barras = fin_b
                barras_completas_perfil += n_comp
                filas_plan_perfil.append({
                    "Perfil": perf_sel,
                    "Largo Barra (m)": round(largo_b, 2),
                    "N.° barra(s)": f"{inicio_b} a {fin_b}" if n_comp > 1 else f"{inicio_b}",
                    "Tipo de uso": "Barras completas",
                    "Elementos que abastece": it["nombre"],
                    "Piezas en barra": n_comp,
                    "Detalle de cortes en la barra": f"{n_comp} barra(s) entera(s) de {largo_b:.2f} m sin corte",
                    "Metraje útil (m)": round(n_comp * largo_b, 2),
                    "Pérdida corte (m)": 0.0,
                    "Sobrante (m)": 0.0,
                    "Aprovechamiento (%)": 100.0
                })

            if tramo_res > 0:
                lista_pzas_elem = [
                    {
                        "largo": tramo_res,
                        "elemento": it["nombre"],
                        "etiqueta": f"{it['nombre']} ({tramo_res:.2f} m)"
                    }
                    for _ in range(cant)
                ]
                grupos_piezas.append(lista_pzas_elem)

        barras_cortadas = []
        if aprovechar_sobrantes:
            todas_las_piezas = [p for grp in grupos_piezas for p in grp]
            piezas_ordenadas = sorted(todas_las_piezas, key=lambda x: x["largo"], reverse=True)
            for pza in piezas_ordenadas:
                mejor_idx = -1
                menor_sobrante = float("inf")
                for idx, b in enumerate(barras_cortadas):
                    usado_actual = sum(x["largo"] for x in b["piezas"])
                    cortes_min = len(b["piezas"])
                    necesario = usado_actual + pza["largo"] + cortes_min * kerf_m
                    if necesario <= largo_b + 1e-7:
                        restante = largo_b - necesario
                        if restante < menor_sobrante:
                            menor_sobrante = restante
                            mejor_idx = idx
                if mejor_idx != -1:
                    barras_cortadas[mejor_idx]["piezas"].append(pza)
                else:
                    barras_cortadas.append({"piezas": [pza]})
        else:
            for grp in grupos_piezas:
                barras_elem = []
                for pza in grp:
                    colocado = False
                    for b in barras_elem:
                        usado_actual = sum(x["largo"] for x in b["piezas"])
                        cortes_min = len(b["piezas"])
                        if usado_actual + pza["largo"] + cortes_min * kerf_m <= largo_b + 1e-7:
                            b["piezas"].append(pza)
                            colocado = True
                            break
                    if not colocado:
                        barras_elem.append({"piezas": [pza]})
                barras_cortadas.extend(barras_elem)

        perdida_total_perfil = 0.0
        sobrante_total_perfil = 0.0
        barras_combinadas_count = 0

        for b in barras_cortadas:
            contador_barras += 1
            pzas_b = b["piezas"]
            n_pzas = len(pzas_b)
            metraje_util_b = sum(x["largo"] for x in pzas_b)

            if (largo_b - metraje_util_b - n_pzas * kerf_m) >= -1e-7:
                perdida_b = n_pzas * kerf_m
            else:
                perdida_b = max(0, n_pzas - 1) * kerf_m

            sobrante_b = max(0.0, largo_b - metraje_util_b - perdida_b)
            perdida_total_perfil += perdida_b
            sobrante_total_perfil += sobrante_b

            conteo_etiquetas = {}
            elems_en_barra = []
            for x in pzas_b:
                conteo_etiquetas[x["etiqueta"]] = conteo_etiquetas.get(x["etiqueta"], 0) + 1
                if x["elemento"] not in elems_en_barra:
                    elems_en_barra.append(x["elemento"])

            if len(elems_en_barra) > 1:
                barras_combinadas_count += 1
                tipo_uso_str = "🔥 Corte Combinado (Aprovecha sobrante)"
            else:
                tipo_uso_str = "Corte Simple"

            detalle_str = " + ".join([f"{cnt}× {etiq}" for etiq, cnt in conteo_etiquetas.items()])
            aprov_pct = (metraje_util_b / largo_b) * 100.0 if largo_b > 0 else 0.0

            filas_plan_perfil.append({
                "Perfil": perf_sel,
                "Largo Barra (m)": round(largo_b, 2),
                "N.° barra(s)": f"{contador_barras}",
                "Tipo de uso": tipo_uso_str,
                "Elementos que abastece": " + ".join(elems_en_barra),
                "Piezas en barra": n_pzas,
                "Detalle de cortes en la barra": f"Cortar: {detalle_str}",
                "Metraje útil (m)": round(metraje_util_b, 2),
                "Pérdida corte (m)": round(perdida_b, 4),
                "Sobrante (m)": round(sobrante_b, 2),
                "Aprovechamiento (%)": round(aprov_pct, 1)
            })

        total_barras_optimizado = barras_completas_perfil + len(barras_cortadas)
        metraje_comprado_perfil = total_barras_optimizado * largo_b
        ahorro_barras = max(0, barras_aisladas_suma - total_barras_optimizado)

        df_plan_perf = pd.DataFrame(filas_plan_perfil)
        todos_los_planes_dfs.append(df_plan_perf)

        consolidado_perfiles.append({
            "Tipo": p_info["tipo"],
            "Perfil": perf_sel,
            "Equiv. / Dim.": p_info["equiv_pulg"],
            "Elementos que comparten este perfil": ", ".join(elementos_involucrados),
            "Largo Barra (m)": round(largo_b, 2),
            "Peso unit. (kg/m)": peso_u,
            "Metraje Requerido (m)": round(metraje_req_total, 2),
            "Barras (Sin compartir)": barras_aisladas_suma,
            "Barras a Comprar": total_barras_optimizado,
            "Barras Ahorradas": ahorro_barras,
            "Metraje Comprado (m)": round(metraje_comprado_perfil, 2),
            "Pérdida Corte (m)": round(perdida_total_perfil, 3),
            "Sobrante Final (m)": round(sobrante_total_perfil, 2),
            "Peso Requerido (kg)": round(metraje_req_total * peso_u, 2),
            "Peso Compra (kg)": round(metraje_comprado_perfil * peso_u, 2),
            "Área Requerida (m²)": round(metraje_req_total * area_u, 2),
            "Área Compra (m²)": round(metraje_comprado_perfil * area_u, 2),
            "Empalmes": empalmes_perfil
        })

        planes_por_perfil[perf_sel] = {
            "df_plan": df_plan_perf,
            "total_barras": total_barras_optimizado,
            "barras_sin_compartir": barras_aisladas_suma,
            "ahorro_barras": ahorro_barras,
            "barras_combinadas": barras_combinadas_count,
            "elementos": elementos_involucrados,
            "largo_barra": largo_b,
            "sobrante_total": sobrante_total_perfil
        }

    df_consolidado = pd.DataFrame(consolidado_perfiles)
    df_todos_planes = pd.concat(todos_los_planes_dfs, ignore_index=True) if todos_los_planes_dfs else pd.DataFrame()
    return df_elementos, df_consolidado, planes_por_perfil, df_todos_planes


# 6. Apartado de Columnas con 3 Modos (Niveladas, Con Desnivel por Lados y Columnas Individuales con Croquis en Planta)
def renderizar_apartado_columnas():
    cfg = st.session_state.config
    p_unico = st.session_state.partidas["columnas_unico"]
    p_mayor = st.session_state.partidas["columnas_mayor"]
    p_menor = st.session_state.partidas["columnas_menor"]

    with st.container(border=True):
        st.markdown("#### 🏛️ Apartado de Columnas Principales, Croquis de Ubicación y Pendiente")
        st.caption(
            "Elige cómo deseas configurar las columnas: todas iguales, por lados (Mayor/Menor) "
            "o con **libertad total columna por columna mediante un Croquis en Planta (Vista Superior)**."
        )

        mapa_modos = {
            "niveladas": "1. Niveladas — Todas las columnas con el mismo perfil y altura",
            "desnivel_lados": "2. Con desnivel por lados — Lado Mayor y Lado Menor (Inclinación uniforme)",
            "individual_croquis": "3. 🎯 Columnas Individuales con Croquis en Planta (Libertad total en perfil y altura por eje)"
        }
        claves_modo = list(mapa_modos.keys())
        idx_modo = claves_modo.index(cfg["modo_columnas"]) if cfg["modo_columnas"] in claves_modo else 2

        modo_elegido = st.radio(
            "Modo de configuración de columnas:",
            options=claves_modo,
            format_func=lambda k: mapa_modos[k],
            index=idx_modo,
            key="radio_modo_columnas"
        )
        cfg["modo_columnas"] = modo_elegido

        opciones_tipo = ["Tubo Cuadrado", "Tubo Rectangular", "Viga H (WF)", "Tubo Schedule (SCH)"]

        # ----------------------------------------------------------------------
        # MODO 1: NIVELADAS (TODAS IGUALES)
        # ----------------------------------------------------------------------
        if modo_elegido == "niveladas":
            p_unico["activo"] = True
            p_mayor["activo"] = False
            p_menor["activo"] = False

            c1, c2, c3, c4 = st.columns([1.4, 2.3, 1.1, 1.2])
            with c1:
                idx_t = opciones_tipo.index(p_unico["tipo"]) if p_unico["tipo"] in opciones_tipo else 0
                p_unico["tipo"] = st.selectbox("Familia de Perfil", options=opciones_tipo, index=idx_t, key="tipo_col_u")
            with c2:
                lista_p = LISTAS_POR_TIPO[p_unico["tipo"]]
                idx_p = lista_p.index(p_unico["perfil"]) if p_unico["perfil"] in lista_p else 0
                p_unico["perfil"] = st.selectbox("Perfil / Designación", options=lista_p, index=idx_p, key="perf_col_u")
            with c3:
                p_unico["cantidad"] = st.number_input("Cantidad total", min_value=1, value=int(p_unico["cantidad"]), step=1, key="cant_col_u")
            with c4:
                p_unico["longitud_m"] = st.number_input("Altura final c/u (m)", min_value=0.10, value=float(p_unico["longitud_m"]), step=0.25, format="%.2f", key="long_col_u")

            info_u = MAPA_PERFILES[p_unico["perfil"]]
            largo_b_u = obtener_largo_comercial_por_tipo(p_unico["tipo"])
            mostrar_ficha_resumen_perfil(p_unico["tipo"], info_u, largo_b_u, p_unico["cantidad"] * p_unico["longitud_m"])

        # ----------------------------------------------------------------------
        # MODO 2: CON DESNIVEL POR LADOS (LADO MAYOR Y LADO MENOR)
        # ----------------------------------------------------------------------
        elif modo_elegido == "desnivel_lados":
            p_unico["activo"] = False
            p_mayor["activo"] = True
            p_menor["activo"] = True

            st.markdown("##### 🔼 1. Columnas de Lado Mayor (Altura Mayor)")
            cm1, cm2, cm3, cm4 = st.columns([1.4, 2.3, 1.1, 1.2])
            with cm1:
                idx_tm = opciones_tipo.index(p_mayor["tipo"]) if p_mayor["tipo"] in opciones_tipo else 0
                p_mayor["tipo"] = st.selectbox("Familia (Lado Mayor)", options=opciones_tipo, index=idx_tm, key="tipo_col_may")
            with cm2:
                lista_pm = LISTAS_POR_TIPO[p_mayor["tipo"]]
                idx_pm = lista_pm.index(p_mayor["perfil"]) if p_mayor["perfil"] in lista_pm else 0
                p_mayor["perfil"] = st.selectbox("Perfil (Lado Mayor)", options=lista_pm, index=idx_pm, key="perf_col_may")
            with cm3:
                p_mayor["cantidad"] = st.number_input("Cant. Lado Mayor", min_value=1, value=int(p_mayor["cantidad"]), step=1, key="cant_col_may")
            with cm4:
                p_mayor["longitud_m"] = st.number_input("Altura Mayor c/u (m)", min_value=0.10, value=float(p_mayor["longitud_m"]), step=0.20, format="%.2f", key="long_col_may")

            info_may = MAPA_PERFILES[p_mayor["perfil"]]
            largo_b_may = obtener_largo_comercial_por_tipo(p_mayor["tipo"])
            mostrar_ficha_resumen_perfil(p_mayor["tipo"], info_may, largo_b_may, p_mayor["cantidad"] * p_mayor["longitud_m"])

            st.divider()
            st.markdown("##### 🔽 2. Columnas de Lado Menor (Altura Menor)")
            cfg["mismo_perfil_columnas_desnivel"] = st.checkbox(
                "Usar la misma familia y perfil que las Columnas de Lado Mayor",
                value=cfg["mismo_perfil_columnas_desnivel"],
                key="chk_mismo_perf_desnivel"
            )

            cn1, cn2, cn3, cn4 = st.columns([1.4, 2.3, 1.1, 1.2])
            if cfg["mismo_perfil_columnas_desnivel"]:
                p_menor["tipo"] = p_mayor["tipo"]
                p_menor["perfil"] = p_mayor["perfil"]
                with cn1:
                    st.text_input("Familia (Lado Menor)", value=p_menor["tipo"], disabled=True, key="tipo_col_men_dis")
                with cn2:
                    st.text_input("Perfil (Lado Menor)", value=p_menor["perfil"], disabled=True, key="perf_col_men_dis")
            else:
                with cn1:
                    idx_tn = opciones_tipo.index(p_menor["tipo"]) if p_menor["tipo"] in opciones_tipo else 0
                    p_menor["tipo"] = st.selectbox("Familia (Lado Menor)", options=opciones_tipo, index=idx_tn, key="tipo_col_men")
                with cn2:
                    lista_pn = LISTAS_POR_TIPO[p_menor["tipo"]]
                    idx_pn = lista_pn.index(p_menor["perfil"]) if p_menor["perfil"] in lista_pn else 0
                    p_menor["perfil"] = st.selectbox("Perfil (Lado Menor)", options=lista_pn, index=idx_pn, key="perf_col_men")

            with cn3:
                p_menor["cantidad"] = st.number_input("Cant. Lado Menor", min_value=1, value=int(p_menor["cantidad"]), step=1, key="cant_col_men")
            with cn4:
                p_menor["longitud_m"] = st.number_input("Altura Menor c/u (m)", min_value=0.10, value=float(p_menor["longitud_m"]), step=0.20, format="%.2f", key="long_col_men")

            info_men = MAPA_PERFILES[p_menor["perfil"]]
            largo_b_men = obtener_largo_comercial_por_tipo(p_menor["tipo"])
            mostrar_ficha_resumen_perfil(p_menor["tipo"], info_men, largo_b_men, p_menor["cantidad"] * p_menor["longitud_m"])

            st.divider()
            st.markdown("##### 📐 3. Cálculo Automático de Pendiente y Ángulo de Inclinación")
            col_luz, col_info_pend = st.columns([1.5, 3.5])
            with col_luz:
                cfg["ancho_portico_m"] = st.number_input(
                    "Ancho del Pórtico / Luz horizontal (m)",
                    min_value=0.50,
                    value=float(cfg["ancho_portico_m"]),
                    step=0.50,
                    format="%.2f"
                )
            geo = calcular_geometria_techo(p_mayor["longitud_m"], p_menor["longitud_m"], cfg["ancho_portico_m"])
            with col_info_pend:
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Desnivel (Δh)", f"{geo['delta_h']:.2f} m")
                m2.metric("Pendiente (%)", f"{geo['pendiente_pct']:.2f} %")
                m3.metric("Ángulo (θ)", f"{geo['angulo_deg']:.2f}°")
                m4.metric("Largo Inclinado", f"{geo['long_inclinada']:.2f} m")

        # ----------------------------------------------------------------------
        # MODO 3: COLUMNAS INDIVIDUALES CON CROQUIS EN PLANTA ("VISTA SUPERIOR")
        # ----------------------------------------------------------------------
        elif modo_elegido == "individual_croquis":
            p_unico["activo"] = False
            p_mayor["activo"] = False
            p_menor["activo"] = False

            st.markdown("##### 🗺️ Configuración de Ejes y Cantidades del Croquis (Vista Superior)")
            g1, g2, g3, g4 = st.columns([1.3, 1.3, 1.6, 1.3])
            with g1:
                cfg["grid_num_ejes_letras"] = st.number_input(
                    "Cant. Ejes Transversales (Letras)",
                    min_value=1,
                    max_value=26,
                    value=int(cfg["grid_num_ejes_letras"]),
                    step=1,
                    help="Número de ejes verticales (ej. 8 para H, G, F, E, D, C, B, A como en tu plano)."
                )
            with g2:
                cfg["grid_num_ejes_numeros"] = st.number_input(
                    "Cant. Ejes Longitudinales (Filas)",
                    min_value=1,
                    max_value=6,
                    value=int(cfg["grid_num_ejes_numeros"]),
                    step=1,
                    help="Número de filas horizontales (ej. 2 para los ejes 2 y 1 de tu plano)."
                )
            with g3:
                orden_str = st.selectbox(
                    "Orden de Letras en Croquis",
                    options=["H → A (Izquierda a Derecha, como plano CAD)", "A → H (Izquierda a Derecha)"],
                    index=0 if cfg["grid_invertir_letras"] else 1
                )
                cfg["grid_invertir_letras"] = orden_str.startswith("H")
            with g4:
                cfg["ancho_portico_m"] = st.number_input(
                    "Luz entre Filas / Ancho Pórtico (m)",
                    min_value=0.50,
                    value=float(cfg["ancho_portico_m"]),
                    step=0.50,
                    format="%.2f"
                )

            letras_ejes, numeros_ejes = sincronizar_nodos_croquis()

            # Herramienta de asignación rápida por fila/eje (para no editar una por una si comparten base)
            with st.expander("⚡ Asignación Rápida por Eje / Fila (Opcional — Aplica un perfil o altura a todo un eje y luego personaliza)", expanded=False):
                b1, b2, b3, b4, b5 = st.columns([1.3, 1.4, 2.0, 1.1, 1.0])
                opciones_destino = [f"Todo el Eje {num}" for num in numeros_ejes] + [f"Todo el Eje {let}" for let in letras_ejes] + ["Todas las columnas"]
                with b1:
                    destino_batch = st.selectbox("Aplicar a:", options=opciones_destino, key="batch_dest")
                with b2:
                    tipo_batch = st.selectbox("Familia:", options=opciones_tipo, key="batch_tipo")
                with b3:
                    perf_batch = st.selectbox("Perfil:", options=LISTAS_POR_TIPO[tipo_batch], key="batch_perf")
                with b4:
                    alt_batch = st.number_input("Altura (m):", min_value=0.10, value=5.00, step=0.20, format="%.2f", key="batch_alt")
                with b5:
                    st.write("")
                    if st.button("Aplicar ahora", type="primary", use_container_width=True, key="btn_batch_apply"):
                        for num in numeros_ejes:
                            for let in letras_ejes:
                                c_key = f"{let}-{num}"
                                aplicar = (
                                    destino_batch == "Todas las columnas"
                                    or destino_batch == f"Todo el Eje {num}"
                                    or destino_batch == f"Todo el Eje {let}"
                                )
                                if aplicar and c_key in st.session_state.nodos_columnas:
                                    st.session_state.nodos_columnas[c_key]["tipo"] = tipo_batch
                                    st.session_state.nodos_columnas[c_key]["perfil"] = perf_batch
                                    st.session_state.nodos_columnas[c_key]["altura_m"] = float(alt_batch)
                                    # Sincronizar widgets individuales si existen en session_state
                                    st.session_state[f"nd_tipo_{c_key}"] = tipo_batch
                                    st.session_state[f"nd_perf_{c_key}"] = perf_batch
                                    st.session_state[f"nd_alt_{c_key}"] = float(alt_batch)
                        st.rerun()

            # Mostrar Croquis Técnico Interactivo en Planta ("VISTA SUPERIOR")
            st.markdown("##### 📐 Croquis en Planta — Vista Superior (Actualización en Tiempo Real)")
            svg_croquis = generar_svg_croquis_columnas(
                letras_ejes,
                numeros_ejes,
                st.session_state.nodos_columnas,
                cfg["ancho_portico_m"]
            )
            st.markdown(svg_croquis, unsafe_allow_html=True)
            st.caption(
                "Leyenda del croquis: **Símbolo `I`** = Viga H (WF) | **Símbolo `▭`** = Tubo Rectangular | "
                "**Símbolo `□`** = Tubo Cuadrado | **Símbolo `○`** = Tubo Schedule (SCH)."
            )

            # Panel de Selección Individual Columna por Columna organizado por pestañas de Eje Longitudinal
            st.markdown("##### 🎯 Selección Individual de Perfil y Altura para cada Columna")
            tabs_filas = st.tabs([f"📍 Eje Longitudinal {num} ({len(letras_ejes)} posiciones)" for num in numeros_ejes])

            for idx_f, num in enumerate(numeros_ejes):
                with tabs_filas[idx_f]:
                    for letra in letras_ejes:
                        coord = f"{letra}-{num}"
                        nodo = st.session_state.nodos_columnas[coord]
                        ic1, ic2, ic3, ic4 = st.columns([1.1, 1.6, 2.3, 1.2])
                        with ic1:
                            nodo["activo"] = st.checkbox(
                                f"Col. **{coord}**",
                                value=nodo["activo"],
                                key=f"nd_act_{coord}"
                            )
                        with ic2:
                            idx_nt = opciones_tipo.index(nodo["tipo"]) if nodo["tipo"] in opciones_tipo else 0
                            nodo["tipo"] = st.selectbox(
                                f"Familia ({coord})",
                                options=opciones_tipo,
                                index=idx_nt,
                                key=f"nd_tipo_{coord}",
                                disabled=not nodo["activo"],
                                label_visibility="collapsed"
                            )
                        with ic3:
                            lista_np = LISTAS_POR_TIPO[nodo["tipo"]]
                            idx_np = lista_np.index(nodo["perfil"]) if nodo["perfil"] in lista_np else 0
                            nodo["perfil"] = st.selectbox(
                                f"Perfil ({coord})",
                                options=lista_np,
                                index=idx_np,
                                key=f"nd_perf_{coord}",
                                disabled=not nodo["activo"],
                                label_visibility="collapsed"
                            )
                        with ic4:
                            nodo["altura_m"] = st.number_input(
                                f"Altura m ({coord})",
                                min_value=0.10,
                                value=float(nodo["altura_m"]),
                                step=0.10,
                                format="%.2f",
                                key=f"nd_alt_{coord}",
                                disabled=not nodo["activo"],
                                label_visibility="collapsed"
                            )

            # Tabla resumen de cantidades por ubicación y pendientes por cada eje transversal
            partidas_ind = obtener_partidas_columnas_activas()
            if partidas_ind:
                col_res1, col_res2 = st.columns([2.5, 2.5])
                with col_res1:
                    st.markdown("###### 📋 Conteo Agrupado por Perfil y Altura")
                    df_conteo_ind = pd.DataFrame([
                        {
                            "Ubicaciones en Croquis": p["nombre"].replace("Columnas ", ""),
                            "Familia": p["tipo"],
                            "Perfil": p["perfil"],
                            "Altura c/u (m)": p["longitud_m"],
                            "Cantidad": p["cantidad_total"],
                            "Metraje Neto (m)": round(p["cantidad_total"] * p["longitud_m"], 2)
                        }
                        for p in partidas_ind
                    ])
                    st.dataframe(df_conteo_ind, use_container_width=True, hide_index=True)

                with col_res2:
                    if len(numeros_ejes) >= 2:
                        st.markdown("###### 📐 Pendiente y Ángulo por cada Pórtico (Ejes Letra)")
                        eje_sup = numeros_ejes[0]
                        eje_inf = numeros_ejes[-1]
                        filas_pend = []
                        for letra in letras_ejes:
                            n_sup = st.session_state.nodos_columnas.get(f"{letra}-{eje_sup}", {})
                            n_inf = st.session_state.nodos_columnas.get(f"{letra}-{eje_inf}", {})
                            if n_sup.get("activo") and n_inf.get("activo"):
                                g_p = calcular_geometria_techo(n_sup["altura_m"], n_inf["altura_m"], cfg["ancho_portico_m"])
                                filas_pend.append({
                                    "Pórtico": f"Eje {letra} ({letra}-{eje_sup} a {letra}-{eje_inf})",
                                    f"H ({letra}-{eje_sup})": f"{n_sup['altura_m']:.2f} m",
                                    f"H ({letra}-{eje_inf})": f"{n_inf['altura_m']:.2f} m",
                                    "Δh (m)": round(g_p["delta_h"], 2),
                                    "Pendiente (%)": f"{g_p['pendiente_pct']:.2f}%",
                                    "Ángulo (°)": f"{g_p['angulo_deg']:.2f}°",
                                    "L. Inclinada (m)": round(g_p["long_inclinada"], 2)
                                })
                        if filas_pend:
                            st.dataframe(pd.DataFrame(filas_pend), use_container_width=True, hide_index=True)


# 7. Bloque interactivo para elementos estándar (Vigas, Correas, Bridas)
def renderizar_bloque_elemento(clave, titulo, descripcion, es_tijeral=False, num_tijerales=1):
    datos = st.session_state.partidas[clave]
    with st.container(border=True):
        col_check, col_tit = st.columns([1, 5])
        with col_check:
            datos["activo"] = st.checkbox("Incluir", value=datos["activo"], key=f"chk_{clave}")
        with col_tit:
            st.markdown(f"#### {titulo}")
            st.caption(descripcion)

        if datos["activo"]:
            c1, c2, c3, c4 = st.columns([1.4, 2.3, 1.1, 1.2])
            with c1:
                opciones_tipo = ["Tubo Cuadrado", "Tubo Rectangular", "Viga H (WF)", "Tubo Schedule (SCH)"]
                idx_tipo = opciones_tipo.index(datos["tipo"]) if datos["tipo"] in opciones_tipo else 0
                datos["tipo"] = st.selectbox(
                    "Familia de Perfil",
                    options=opciones_tipo,
                    index=idx_tipo,
                    key=f"tipo_{clave}"
                )

            with c2:
                lista_perfiles = LISTAS_POR_TIPO[datos["tipo"]]
                idx_perf = lista_perfiles.index(datos["perfil"]) if datos["perfil"] in lista_perfiles else 0
                datos["perfil"] = st.selectbox(
                    "Perfil / Designación",
                    options=lista_perfiles,
                    index=idx_perf,
                    key=f"perf_{clave}"
                )

            with c3:
                etiqueta_cant = "Cant. por 1 tijeral" if es_tijeral else "Cantidad total"
                datos["cantidad"] = st.number_input(
                    etiqueta_cant,
                    min_value=1,
                    value=int(datos["cantidad"]),
                    step=1,
                    key=f"cant_{clave}"
                )

            with c4:
                datos["longitud_m"] = st.number_input(
                    "Longitud final c/u (m)",
                    min_value=0.10,
                    value=float(datos["longitud_m"]),
                    step=0.25,
                    format="%.2f",
                    key=f"long_{clave}"
                )

            info_p = MAPA_PERFILES[datos["perfil"]]
            largo_barra_aplica = obtener_largo_comercial_por_tipo(datos["tipo"])
            cant_real = datos["cantidad"] * num_tijerales if es_tijeral else datos["cantidad"]
            metraje_subtotal = cant_real * datos["longitud_m"]

            nota_extra = f" | Total en {num_tijerales} tijerales: **{cant_real} pzas**" if es_tijeral else ""
            mostrar_ficha_resumen_perfil(datos["tipo"], info_p, largo_barra_aplica, metraje_subtotal, nota_extra)


# 8. Gestor dinámico de Montantes y Diagonales en el Paso 3
def renderizar_gestor_montantes_dinamicos(num_tijerales):
    st.markdown("#### ⏸️ Tijeral — Montantes y Diagonales (Medidas Específicas)")
    st.caption(
        "Añade tantos tipos o alturas de montantes como tenga tu tijeral. "
        "**Recuerda:** si usas el mismo perfil que en las bridas o columnas, el sistema aprovechará automáticamente los sobrantes de barra."
    )

    opciones_tipo = ["Tubo Cuadrado", "Tubo Rectangular", "Viga H (WF)", "Tubo Schedule (SCH)"]
    id_a_eliminar = None

    for m_item in st.session_state.lista_montantes:
        mid = m_item["id"]
        with st.container(border=True):
            top_c1, top_c2, top_c3 = st.columns([1, 4, 1])
            with top_c1:
                m_item["activo"] = st.checkbox("Incluir", value=m_item["activo"], key=f"chk_mont_{mid}")
            with top_c2:
                m_item["nombre"] = st.text_input(
                    "Identificador del Montante o Diagonal",
                    value=m_item["nombre"],
                    key=f"nom_mont_{mid}",
                    label_visibility="collapsed"
                )
            with top_c3:
                if len(st.session_state.lista_montantes) > 1:
                    if st.button("🗑️ Quitar", key=f"del_mont_{mid}", use_container_width=True):
                        id_a_eliminar = mid

            if m_item["activo"]:
                mc1, mc2, mc3, mc4 = st.columns([1.4, 2.3, 1.1, 1.2])
                with mc1:
                    idx_t = opciones_tipo.index(m_item["tipo"]) if m_item["tipo"] in opciones_tipo else 0
                    m_item["tipo"] = st.selectbox(
                        "Familia de Perfil",
                        options=opciones_tipo,
                        index=idx_t,
                        key=f"tipo_mont_{mid}"
                    )
                with mc2:
                    lista_p = LISTAS_POR_TIPO[m_item["tipo"]]
                    idx_p = lista_p.index(m_item["perfil"]) if m_item["perfil"] in lista_p else 0
                    m_item["perfil"] = st.selectbox(
                        "Perfil / Designación",
                        options=lista_p,
                        index=idx_p,
                        key=f"perf_mont_{mid}"
                    )
                with mc3:
                    m_item["cantidad"] = st.number_input(
                        "Cant. por 1 tijeral",
                        min_value=1,
                        value=int(m_item["cantidad"]),
                        step=1,
                        key=f"cant_mont_{mid}"
                    )
                with mc4:
                    m_item["longitud_m"] = st.number_input(
                        "Longitud final c/u (m)",
                        min_value=0.05,
                        value=float(m_item["longitud_m"]),
                        step=0.10,
                        format="%.2f",
                        key=f"long_mont_{mid}"
                    )

                info_m = MAPA_PERFILES[m_item["perfil"]]
                largo_b_m = obtener_largo_comercial_por_tipo(m_item["tipo"])
                cant_total_m = m_item["cantidad"] * num_tijerales
                metraje_sub = cant_total_m * m_item["longitud_m"]
                mostrar_ficha_resumen_perfil(
                    m_item["tipo"],
                    info_m,
                    largo_b_m,
                    metraje_sub,
                    f" | Total en {num_tijerales} tijerales: **{cant_total_m} pzas**"
                )

    if id_a_eliminar is not None:
        st.session_state.lista_montantes = [
            m for m in st.session_state.lista_montantes if m["id"] != id_a_eliminar
        ]
        st.rerun()

    if st.button("➕ Añadir otro tipo / medida de Montante o Diagonal", type="secondary", use_container_width=True):
        ultimo = st.session_state.lista_montantes[-1] if st.session_state.lista_montantes else {
            "tipo": "Tubo Cuadrado", "perfil": "40 x 40 | 2 mm", "longitud_m": 1.00
        }
        nuevo_id = st.session_state.next_montante_id
        st.session_state.next_montante_id += 1
        st.session_state.lista_montantes.append({
            "id": nuevo_id,
            "activo": True,
            "nombre": f"Tijeral - Montante M{len(st.session_state.lista_montantes) + 1}",
            "tipo": ultimo["tipo"],
            "perfil": ultimo["perfil"],
            "cantidad": 2,
            "longitud_m": max(0.20, round(ultimo["longitud_m"] - 0.20, 2))
        })
        st.rerun()


# 9. Barra Lateral: Navegación por pasos y resumen normativo
with st.sidebar:
    st.header("🧭 Pasos del Asistente")
    paso_actual = st.session_state.paso

    if st.button("1️⃣ Parámetros Generales", use_container_width=True, type="primary" if paso_actual == 1 else "secondary"):
        ir_a_paso(1)
        st.rerun()
    if st.button("2️⃣ Columnas (Croquis), Pendiente y Correas", use_container_width=True, type="primary" if paso_actual == 2 else "secondary"):
        ir_a_paso(2)
        st.rerun()
    if st.button("3️⃣ Tijeral (Bridas y Montantes)", use_container_width=True, type="primary" if paso_actual == 3 else "secondary"):
        ir_a_paso(3)
        st.rerun()
    if st.button("4️⃣ Panorama Completo", use_container_width=True, type="primary" if paso_actual == 4 else "secondary"):
        ir_a_paso(4)
        st.rerun()

    st.divider()
    st.markdown("##### 📋 Normas Integradas (332 Perfiles)")
    st.caption(
        "**1. Tubos Estructurales (Cuadrados y Rect.):**\n"
        "• ASTM A500 / AISI A500 Grado A (LAC - ERW)\n\n"
        "**2. Vigas H Alas Anchas (WF):**\n"
        "• ASTM A36 / A572 Gr. 50 / A992 (20, 30 y 40 pies)\n\n"
        "**3. Tubos Schedule (SCH 40 / SCH 80) Sin Costura:**\n"
        "• Trinorma: ASTM A53 / A106 / API 5L PSL 1 Gr. B"
    )


# 10. Encabezado y Barra de Progreso
st.title("🏗️ Calculadora Estructural: ASTM A500, Vigas H (WF) y Tubos Schedule (SCH)")

titulos_pasos = {
    1: "Paso 1 de 4: Configuración General y Longitudes Comerciales",
    2: "Paso 2 de 4: Columnas (con Croquis en Planta Individual), Pendiente, Vigas y Correas",
    3: "Paso 3 de 4: Diseño del Tijeral (Brida Superior, Brida Inferior y Múltiples Montantes)",
    4: "Paso 4 de 4: Panorama Completo con Croquis y Aprovechamiento Global de Sobrantes"
}
st.progress(st.session_state.paso / 4.0, text=titulos_pasos[st.session_state.paso])
st.divider()


# ==============================================================================
# PASO 1: CONFIGURACIÓN GENERAL
# ==============================================================================
if st.session_state.paso == 1:
    st.subheader("1️⃣ Configuración General de Barras y Corte")
    st.markdown("Define las longitudes comerciales para cada familia de perfiles y el espesor del corte.")

    with st.container(border=True):
        st.session_state.config["proyecto"] = st.text_input(
            "Nombre del Proyecto / Obra",
            value=st.session_state.config["proyecto"]
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.config["largo_tubos_m"] = st.number_input(
                "Largo comercial Tubos ASTM A500 (m)",
                min_value=1.00,
                value=float(st.session_state.config["largo_tubos_m"]),
                step=0.50,
                format="%.2f"
            )

            st.session_state.config["ancho_corte_mm"] = st.number_input(
                "Ancho de corte / disco (mm)",
                min_value=0.0,
                value=float(st.session_state.config["ancho_corte_mm"]),
                step=0.5,
                format="%.1f"
            )

        with col2:
            opciones_wf = [
                "20 pies (6.10 m)",
                "30 pies (9.14 m) - Estándar",
                "40 pies (12.19 m) - Estándar",
                "Personalizado"
            ]
            idx_wf = opciones_wf.index(st.session_state.config["modo_largo_wf"]) if st.session_state.config["modo_largo_wf"] in opciones_wf else 1
            modo_wf = st.selectbox(
                "Presentación Comercial Vigas H (WF)",
                options=opciones_wf,
                index=idx_wf
            )
            st.session_state.config["modo_largo_wf"] = modo_wf

            if modo_wf == "20 pies (6.10 m)":
                st.session_state.config["largo_wf_m"] = 6.10
            elif modo_wf == "30 pies (9.14 m) - Estándar":
                st.session_state.config["largo_wf_m"] = 9.14
            elif modo_wf == "40 pies (12.19 m) - Estándar":
                st.session_state.config["largo_wf_m"] = 12.19
            else:
                st.session_state.config["largo_wf_m"] = st.number_input(
                    "Largo personalizado Vigas WF (m)",
                    min_value=1.00,
                    value=float(st.session_state.config["largo_wf_m"]),
                    step=0.50,
                    format="%.2f"
                )

            st.session_state.config["num_tijerales"] = st.number_input(
                "Cantidad de Tijerales iguales en el techo",
                min_value=1,
                value=int(st.session_state.config["num_tijerales"]),
                step=1
            )

        with col3:
            opciones_sch = [
                "6.00 m (SRL Comercial Estándar)",
                "6.40 m (SRL Promedio 21 pies)",
                "10.70 m (DRL Mínimo)",
                "12.00 m (DRL Comercial)",
                "Personalizado"
            ]
            idx_sch = opciones_sch.index(st.session_state.config["modo_largo_sch"]) if st.session_state.config["modo_largo_sch"] in opciones_sch else 0
            modo_sch = st.selectbox(
                "Presentación Tubos Schedule (SCH)",
                options=opciones_sch,
                index=idx_sch
            )
            st.session_state.config["modo_largo_sch"] = modo_sch

            if modo_sch == "6.00 m (SRL Comercial Estándar)":
                st.session_state.config["largo_sch_m"] = 6.00
            elif modo_sch == "6.40 m (SRL Promedio 21 pies)":
                st.session_state.config["largo_sch_m"] = 6.40
            elif modo_sch == "10.70 m (DRL Mínimo)":
                st.session_state.config["largo_sch_m"] = 10.70
            elif modo_sch == "12.00 m (DRL Comercial)":
                st.session_state.config["largo_sch_m"] = 12.00
            else:
                st.session_state.config["largo_sch_m"] = st.number_input(
                    "Largo personalizado Tubos SCH (m)",
                    min_value=1.00,
                    value=float(st.session_state.config["largo_sch_m"]),
                    step=0.50,
                    format="%.2f"
                )

            st.session_state.config["optimizar_sobrantes_mismo_perfil"] = st.checkbox(
                "♻️ Aprovechar sobrantes entre elementos del mismo perfil",
                value=st.session_state.config["optimizar_sobrantes_mismo_perfil"]
            )

    st.write("")
    col_nav1, col_nav2 = st.columns([4, 1])
    with col_nav2:
        if st.button("Siguiente ➡️", type="primary", use_container_width=True):
            ir_a_paso(2)
            st.rerun()


# ==============================================================================
# PASO 2: COLUMNAS (CROQUIS EN PLANTA / DESNIVEL), VIGAS Y CORREAS
# ==============================================================================
elif st.session_state.paso == 2:
    st.subheader("2️⃣ Selección de Columnas (con Croquis en Planta), Pendiente, Vigas y Correas")

    renderizar_apartado_columnas()

    renderizar_bloque_elemento(
        "vigas_portico",
        "🌉 Vigas Principales / Soleras (Opcional)",
        "Activa esta partida si tu estructura incluye vigas maestras o soleras de pórtico.",
        es_tijeral=False
    )

    renderizar_bloque_elemento(
        "correas",
        "📏 Correas de Cobertura",
        "Perfiles longitudinales de apoyo para la cobertura del techo.",
        es_tijeral=False
    )

    st.write("")
    col_ant, col_esp, col_sig = st.columns([1, 3, 1])
    with col_ant:
        if st.button("⬅️ Anterior", use_container_width=True):
            ir_a_paso(1)
            st.rerun()
    with col_sig:
        if st.button("Siguiente ➡️", type="primary", use_container_width=True):
            ir_a_paso(3)
            st.rerun()


# ==============================================================================
# PASO 3: TIJERAL (BRIDA SUPERIOR, BRIDA INFERIOR Y MÚLTIPLES MONTANTES)
# ==============================================================================
elif st.session_state.paso == 3:
    cfg = st.session_state.config
    st.subheader("3️⃣ Selección de Perfiles para el Tijeral (Bridas y Montantes Específicos)")

    # Obtener referencia de pendiente desde el modo de columnas activo
    geo_ref = None
    if cfg["modo_columnas"] == "desnivel_lados" and st.session_state.partidas["columnas_mayor"]["activo"]:
        geo_ref = calcular_geometria_techo(
            st.session_state.partidas["columnas_mayor"]["longitud_m"],
            st.session_state.partidas["columnas_menor"]["longitud_m"],
            cfg["ancho_portico_m"]
        )
    elif cfg["modo_columnas"] == "individual_croquis":
        letras_e, numeros_e = sincronizar_nodos_croquis()
        if len(numeros_e) >= 2 and letras_e:
            l0 = letras_e[0]
            n_sup = st.session_state.nodos_columnas.get(f"{l0}-{numeros_e[0]}", {})
            n_inf = st.session_state.nodos_columnas.get(f"{l0}-{numeros_e[-1]}", {})
            if n_sup.get("activo") and n_inf.get("activo"):
                geo_ref = calcular_geometria_techo(n_sup["altura_m"], n_inf["altura_m"], cfg["ancho_portico_m"])

    if geo_ref is not None:
        with st.container(border=True):
            col_g1, col_g2 = st.columns([3.2, 1.8])
            with col_g1:
                st.markdown(
                    f"📐 **Geometría de Pórtico Calculada:** "
                    f"Luz = `{cfg['ancho_portico_m']:.2f} m` | Desnivel Δh = `{geo_ref['delta_h']:.2f} m` | "
                    f"**Pendiente = `{geo_ref['pendiente_pct']:.2f}%` (`{geo_ref['angulo_deg']:.2f}°`)** | "
                    f"**Longitud Inclinada = `{geo_ref['long_inclinada']:.2f} m`**"
                )
            with col_g2:
                if st.button(f"📏 Usar {geo_ref['long_inclinada']:.2f} m en Brida Superior", use_container_width=True):
                    st.session_state.partidas["brida_sup"]["longitud_m"] = round(geo_ref["long_inclinada"], 2)
                    st.session_state.partidas["brida_inf"]["longitud_m"] = round(cfg["ancho_portico_m"], 2)
                    st.rerun()

    col_tij1, col_tij2 = st.columns([1, 3])
    with col_tij1:
        cfg["num_tijerales"] = st.number_input(
            "N.° de Tijerales iguales",
            min_value=1,
            value=int(cfg["num_tijerales"]),
            step=1
        )
    with col_tij2:
        st.info(
            f"💡 Ingresa abajo las piezas para **1 tijeral**. "
            f"El sistema multiplicará automáticamente todo por **{cfg['num_tijerales']} tijeral(es)** y aprovechará los sobrantes de los perfiles repetidos."
        )

    n_tij = cfg["num_tijerales"]

    renderizar_bloque_elemento(
        "brida_sup",
        "🔼 Tijeral — Brida Superior",
        "Cordón o par superior inclinado del tijeral.",
        es_tijeral=True,
        num_tijerales=n_tij
    )

    renderizar_bloque_elemento(
        "brida_inf",
        "🔽 Tijeral — Brida Inferior",
        "Cordón o tirante inferior del tijeral.",
        es_tijeral=True,
        num_tijerales=n_tij
    )

    st.divider()
    renderizar_gestor_montantes_dinamicos(num_tijerales=n_tij)

    st.write("")
    col_ant, col_esp, col_sig = st.columns([1, 2.5, 1.5])
    with col_ant:
        if st.button("⬅️ Anterior", use_container_width=True):
            ir_a_paso(2)
            st.rerun()
    with col_sig:
        if st.button("Siguiente: Panorama Completo 📊", type="primary", use_container_width=True):
            ir_a_paso(4)
            st.rerun()


# ==============================================================================
# PASO 4: PANORAMA COMPLETO CON CROQUIS Y APROVECHAMIENTO GLOBAL DE SOBRANTES
# ==============================================================================
elif st.session_state.paso == 4:
    cfg = st.session_state.config
    st.subheader(f"📊 Panorama Completo del Proyecto: {cfg['proyecto']}")

    col_opt1, col_opt2 = st.columns([3, 2])
    with col_opt1:
        st.caption(
            f"Barra Tubos ASTM A500: **{cfg['largo_tubos_m']:.2f} m** | "
            f"Barra Vigas WF: **{cfg['largo_wf_m']:.2f} m** | "
            f"Barra Tubos SCH: **{cfg['largo_sch_m']:.2f} m** | "
            f"Corte: **{cfg['ancho_corte_mm']:.1f} mm** | "
            f"Tijerales: **{cfg['num_tijerales']} unid.**"
        )
    with col_opt2:
        cfg["optimizar_sobrantes_mismo_perfil"] = st.checkbox(
            "♻️ Aprovechar sobrantes entre elementos del mismo perfil (Columnas + Bridas + Montantes)",
            value=cfg["optimizar_sobrantes_mismo_perfil"]
        )

    # Construir lista unificada de elementos activos
    lista_items_activos = []
    lista_items_activos.extend(obtener_partidas_columnas_activas())

    for clave in ["vigas_portico", "correas", "brida_sup", "brida_inf"]:
        it = st.session_state.partidas[clave]
        if it["activo"]:
            cant_final = it["cantidad"] * cfg["num_tijerales"] if it["es_tijeral"] else it["cantidad"]
            lista_items_activos.append({
                "nombre": it["nombre"],
                "tipo": it["tipo"],
                "perfil": it["perfil"],
                "cantidad_total": cant_final,
                "longitud_m": it["longitud_m"],
                "largo_barra_m": obtener_largo_comercial_por_tipo(it["tipo"])
            })

    for m_it in st.session_state.lista_montantes:
        if m_it["activo"]:
            lista_items_activos.append({
                "nombre": m_it["nombre"],
                "tipo": m_it["tipo"],
                "perfil": m_it["perfil"],
                "cantidad_total": m_it["cantidad"] * cfg["num_tijerales"],
                "longitud_m": m_it["longitud_m"],
                "largo_barra_m": obtener_largo_comercial_por_tipo(m_it["tipo"])
            })

    if not lista_items_activos:
        st.warning("No hay elementos activos. Regresa a los pasos anteriores y selecciona al menos un elemento.")
    else:
        df_elementos, df_consolidado, planes_por_perfil, df_todos_planes = ejecutar_metrado_y_optimizacion_global(
            lista_items_activos,
            aprovechar_sobrantes=cfg["optimizar_sobrantes_mismo_perfil"]
        )

        # 1. Tarjetas de Resumen Global
        total_barras_comprar = int(df_consolidado["Barras a Comprar"].sum())
        total_barras_aislado = int(df_consolidado["Barras (Sin compartir)"].sum())
        barras_ahorradas = int(df_consolidado["Barras Ahorradas"].sum())
        peso_total_compra = df_consolidado["Peso Compra (kg)"].sum()
        peso_total_req = df_consolidado["Peso Requerido (kg)"].sum()
        area_total_pintura = df_consolidado["Área Requerida (m²)"].sum()
        sobrante_total = df_consolidado["Sobrante Final (m)"].sum()

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric(
            "BARRAS A COMPRAR",
            f"{total_barras_comprar} unid.",
            delta=f"-{barras_ahorradas} barras ahorradas" if barras_ahorradas > 0 else "Optimizado"
        )
        k2.metric("PESO TOTAL COMPRA", f"{peso_total_compra:,.2f} kg", delta=f"Neto: {peso_total_req:,.2f} kg")
        k3.metric("ÁREA EXT. PINTURA", f"{area_total_pintura:,.2f} m²")
        k4.metric("BARRAS SIN COMPARTIR", f"{total_barras_aislado} unid.")
        k5.metric("SOBRANTE FINAL", f"{sobrante_total:,.2f} m")

        if barras_ahorradas > 0:
            st.success(
                f"♻️ **¡Aprovechamiento de retazos activo!** Al reutilizar los tramos sobrantes entre elementos que comparten el mismo perfil, "
                f"redujiste la compra de **{total_barras_aislado} barras** a **{total_barras_comprar} barras** "
                f"(un ahorro directo de **{barras_ahorradas} barra(s) comercial(es)**)."
            )

        if cfg["modo_columnas"] == "individual_croquis":
            with st.expander("🗺️ Ver Croquis en Planta de Ubicación de Columnas (Vista Superior)", expanded=True):
                letras_e, numeros_e = sincronizar_nodos_croquis()
                st.markdown(
                    generar_svg_croquis_columnas(
                        letras_e,
                        numeros_e,
                        st.session_state.nodos_columnas,
                        cfg["ancho_portico_m"]
                    ),
                    unsafe_allow_html=True
                )

        st.divider()

        tab_consolidado, tab_cortes, tab_elementos, tab_catalogo = st.tabs([
            "🛒 1. Orden de Compra Consolidada (Optimizada)",
            "🪚 2. Plan de Corte Combinado por Perfil",
            "📐 3. Metrado Detallado por Elemento y Ubicación",
            "📒 4. Catálogo Técnico (332 Perfiles)"
        ])

        with tab_consolidado:
            st.markdown("#### 🛒 Lista de Compra Optimizada por Tipo de Perfil")
            st.dataframe(df_consolidado, use_container_width=True, hide_index=True)

            csv_compra = df_consolidado.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "⬇️ Descargar Orden de Compra Optimizada (CSV)",
                data=csv_compra,
                file_name="orden_compra_optimizada.csv",
                mime="text/csv"
            )

        with tab_cortes:
            st.markdown("#### 🪚 Plan de Corte en Taller Agrupado por Perfil (Con Reutilización de Sobrantes)")
            for perf_key, datos_plan in planes_por_perfil.items():
                etiqueta_ahorro = f" | ♻️ Ahorro: {datos_plan['ahorro_barras']} barra(s)" if datos_plan["ahorro_barras"] > 0 else ""
                with st.expander(
                    f"📌 Perfil: {perf_key} — Comprar: {datos_plan['total_barras']} barra(s) de {datos_plan['largo_barra']:.2f} m{etiqueta_ahorro}",
                    expanded=True
                ):
                    st.markdown(f"**Elementos / Ubicaciones que abastece este perfil:** `{', '.join(datos_plan['elementos'])}`")
                    if datos_plan["barras_combinadas"] > 0:
                        st.info(
                            f"🔥 Se generaron **{datos_plan['barras_combinadas']} barra(s) de corte combinado** donde los sobrantes de los tramos largos "
                            f"se aprovechan inmediatamente para cortar piezas más cortas del mismo perfil."
                        )
                    st.dataframe(datos_plan["df_plan"], use_container_width=True, hide_index=True)

            csv_cortes = df_todos_planes.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "⬇️ Descargar Plan de Corte Combinado Completo (CSV)",
                data=csv_cortes,
                file_name="plan_corte_combinado_taller.csv",
                mime="text/csv"
            )

        with tab_elementos:
            st.markdown("#### 📐 Desglose de Metrado por Elemento Estructural y Ubicación en Croquis")
            st.dataframe(df_elementos, use_container_width=True, hide_index=True)

            csv_elem = df_elementos.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "⬇️ Descargar Metrado por Elemento (CSV)",
                data=csv_elem,
                file_name="metrado_por_elemento.csv",
                mime="text/csv"
            )

        with tab_catalogo:
            st.markdown("#### 📒 Catálogos Oficiales Integrados (332 Perfiles)")
            sub_sch, sub_wf, sub_a500 = st.tabs([
                "⭕ Tubos Schedule SCH Sin Costura (30 perfiles)",
                "🏗️ Vigas H Alas Anchas WF (156 perfiles)",
                "⬜ Tubos Cuadrados y Rectangulares ASTM A500 (146 perfiles)"
            ])

            with sub_sch:
                df_prop_sch = pd.DataFrame([
                    {"Norma Técnica": "ASTM A53 / A53M", "Grado": "B", "Fluencia mín. (ksi)": 35, "Fluencia mín. (MPa)": 240, "Tracción mín. (ksi)": 60, "Tracción mín. (MPa)": 415},
                    {"Norma Técnica": "ASTM A106 / A106M", "Grado": "B", "Fluencia mín. (ksi)": 35, "Fluencia mín. (MPa)": 240, "Tracción mín. (ksi)": 60, "Tracción mín. (MPa)": 415},
                    {"Norma Técnica": "API 5L PSL 1", "Grado": "B", "Fluencia mín. (ksi)": 35, "Fluencia mín. (MPa)": 241, "Tracción mín. (ksi)": 60, "Tracción mín. (MPa)": 413},
                ])
                st.dataframe(df_prop_sch, use_container_width=True, hide_index=True)
                df_vista_sch = pd.DataFrame(CATALOGO_TUBOS_SCH)[[
                    "nom_pulg", "od_pulg", "lado_a_mm", "t_pulg", "espesor_mm",
                    "peso_kg_m", "peso_tipo", "sch_no", "presion_psi", "area_m2_m", "extremos"
                ]].rename(columns={
                    "nom_pulg": "Diám. Nominal (pulg)",
                    "od_pulg": "Diám. Exterior (pulg)",
                    "lado_a_mm": "Diám. Exterior (mm)",
                    "t_pulg": "Espesor Pared (pulg)",
                    "espesor_mm": "Espesor Pared (mm)",
                    "peso_kg_m": "Peso (kg/m)",
                    "peso_tipo": "Peso Tipo",
                    "sch_no": "SCH N.°",
                    "presion_psi": "Presión Prueba Grado B (psi)",
                    "area_m2_m": "Área Ext. (m²/m)",
                    "extremos": "Extremos"
                })
                st.dataframe(df_vista_sch, use_container_width=True, hide_index=True, height=420)

            with sub_wf:
                df_prop_wf = pd.DataFrame([
                    {"Norma Técnica": "ASTM A36 / A36M-19", "Grado": "—", "Fluencia (MPa ≥)": "250", "Rotura (MPa ≥)": "400 - 550", "Elongación % ≥": '21% (2") / 20% (8")'},
                    {"Norma Técnica": "ASTM A572 / A572M-21e1", "Grado": "50", "Fluencia (MPa ≥)": "345", "Rotura (MPa ≥)": "450 mín", "Elongación % ≥": '21% (2") / 16% (8")'},
                    {"Norma Técnica": "ASTM A992 / A992M-22", "Grado": "—", "Fluencia (MPa ≥)": "345", "Rotura (MPa ≥)": "450 - 550", "Elongación % ≥": '21% (2") / 18% (8")'},
                ])
                st.dataframe(df_prop_wf, use_container_width=True, hide_index=True)
                df_vista_wf = pd.DataFrame(CATALOGO_VIGAS_WF)[[
                    "selector", "d_pulg", "b_pulg", "lado_a_mm", "lado_b_mm",
                    "espesor_mm", "espesor_alma_mm", "peso_lb_pie", "peso_kg_m", "area_m2_m"
                ]].rename(columns={
                    "selector": "Designación Nominal",
                    "d_pulg": "Peralte d (pulg)",
                    "b_pulg": "Ala b (pulg)",
                    "lado_a_mm": "Peralte d (mm)",
                    "lado_b_mm": "Ala b (mm)",
                    "espesor_mm": "Espesor Ala f (mm)",
                    "espesor_alma_mm": "Espesor Alma w (mm)",
                    "peso_lb_pie": "Peso (lb/pie)",
                    "peso_kg_m": "Peso (kg/m)",
                    "area_m2_m": "Área Ext. (m²/m)"
                })
                st.dataframe(df_vista_wf, use_container_width=True, hide_index=True, height=420)

            with sub_a500:
                df_vista_a500 = pd.DataFrame(CATALOGO_CUADRADOS + CATALOGO_RECTANGULARES)[[
                    "tipo", "selector", "equiv_pulg", "lado_a_mm", "lado_b_mm",
                    "espesor_mm", "peso_kg_m", "peso_6m_ficha", "area_m2_m", "nota"
                ]].rename(columns={
                    "tipo": "Tipo",
                    "selector": "Perfil | Espesor",
                    "equiv_pulg": "Equiv. Pulg.",
                    "lado_a_mm": "Lado A (mm)",
                    "lado_b_mm": "Lado B (mm)",
                    "espesor_mm": "Espesor (mm)",
                    "peso_kg_m": "Peso (kg/m)",
                    "peso_6m_ficha": "Peso 6 m Ficha (kg)",
                    "area_m2_m": "Área Ext. (m²/m)",
                    "nota": "Control del Dato"
                })
                st.dataframe(df_vista_a500, use_container_width=True, hide_index=True, height=420)

    st.write("")
    col_volver, col_esp, col_reiniciar = st.columns([1.5, 2.5, 1.5])
    with col_volver:
        if st.button("⬅️ Volver al Paso 3 (Tijeral)", use_container_width=True):
            ir_a_paso(3)
            st.rerun()
    with col_reiniciar:
        if st.button("🔄 Volver al Paso 1", use_container_width=True):
            ir_a_paso(1)
            st.rerun()
