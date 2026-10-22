import math
import streamlit as st
import pandas as pd

# 1. Configuración general de la página
st.set_page_config(
    page_title="Calculadora Estructural ASTM A500 | Techos y Tijerales",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Catálogo Completo ASTM A500: Tubos Cuadrados (68) + Tubos Rectangulares de Ficha Técnica (78)
CATALOGO_CUADRADOS = [
    {"selector": "20 x 20 | 0.9 mm", "tipo": "Cuadrado", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_a_mm": 20, "lado_b_mm": 20, "espesor_mm": 0.9, "peso_kg_m": 0.49, "peso_6m_ficha": 2.96, "nota": ""},
    {"selector": "20 x 20 | 1.5 mm", "tipo": "Cuadrado", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_a_mm": 20, "lado_b_mm": 20, "espesor_mm": 1.5, "peso_kg_m": 0.86, "peso_6m_ficha": 5.14, "nota": ""},
    {"selector": "20 x 20 | 2 mm", "tipo": "Cuadrado", "perfil": "20 x 20", "equiv_pulg": '3/4" x 3/4"', "lado_a_mm": 20, "lado_b_mm": 20, "espesor_mm": 2.0, "peso_kg_m": 1.04, "peso_6m_ficha": 6.24, "nota": ""},
    {"selector": "25 x 25 | 1.5 mm", "tipo": "Cuadrado", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_a_mm": 25, "lado_b_mm": 25, "espesor_mm": 1.5, "peso_kg_m": 1.06, "peso_6m_ficha": 6.37, "nota": ""},
    {"selector": "25 x 25 | 2 mm", "tipo": "Cuadrado", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_a_mm": 25, "lado_b_mm": 25, "espesor_mm": 2.0, "peso_kg_m": 1.46, "peso_6m_ficha": 8.76, "nota": ""},
    {"selector": "25 x 25 | 2.5 mm", "tipo": "Cuadrado", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_a_mm": 25, "lado_b_mm": 25, "espesor_mm": 2.5, "peso_kg_m": 1.67, "peso_6m_ficha": 10.02, "nota": ""},
    {"selector": "25 x 25 | 3 mm", "tipo": "Cuadrado", "perfil": "25 x 25", "equiv_pulg": '1" x 1"', "lado_a_mm": 25, "lado_b_mm": 25, "espesor_mm": 3.0, "peso_kg_m": 1.93, "peso_6m_ficha": 11.58, "nota": ""},
    {"selector": "30 x 30 | 1.2 mm", "tipo": "Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30, "lado_b_mm": 30, "espesor_mm": 1.2, "peso_kg_m": 1.04, "peso_6m_ficha": 6.24, "nota": ""},
    {"selector": "30 x 30 | 1.5 mm", "tipo": "Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30, "lado_b_mm": 30, "espesor_mm": 1.5, "peso_kg_m": 1.30, "peso_6m_ficha": 7.80, "nota": ""},
    {"selector": "30 x 30 | 1.8 mm", "tipo": "Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30, "lado_b_mm": 30, "espesor_mm": 1.8, "peso_kg_m": 1.68, "peso_6m_ficha": 10.08, "nota": ""},
    {"selector": "30 x 30 | 2 mm", "tipo": "Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30, "lado_b_mm": 30, "espesor_mm": 2.0, "peso_kg_m": 1.86, "peso_6m_ficha": 11.16, "nota": ""},
    {"selector": "30 x 30 | 2.5 mm", "tipo": "Cuadrado", "perfil": "30 x 30", "equiv_pulg": '1 1/4" x 1 1/4"', "lado_a_mm": 30, "lado_b_mm": 30, "espesor_mm": 2.5, "peso_kg_m": 2.17, "peso_6m_ficha": 13.02, "nota": ""},
    {"selector": "40 x 40 | 1.5 mm", "tipo": "Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40, "lado_b_mm": 40, "espesor_mm": 1.5, "peso_kg_m": 1.77, "peso_6m_ficha": 10.62, "nota": ""},
    {"selector": "40 x 40 | 1.8 mm", "tipo": "Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40, "lado_b_mm": 40, "espesor_mm": 1.8, "peso_kg_m": 2.03, "peso_6m_ficha": 12.18, "nota": ""},
    {"selector": "40 x 40 | 2 mm", "tipo": "Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40, "lado_b_mm": 40, "espesor_mm": 2.0, "peso_kg_m": 2.24, "peso_6m_ficha": 13.46, "nota": ""},
    {"selector": "40 x 40 | 2.5 mm", "tipo": "Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40, "lado_b_mm": 40, "espesor_mm": 2.5, "peso_kg_m": 2.99, "peso_6m_ficha": 17.94, "nota": ""},
    {"selector": "40 x 40 | 3 mm", "tipo": "Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40, "lado_b_mm": 40, "espesor_mm": 3.0, "peso_kg_m": 3.54, "peso_6m_ficha": 21.24, "nota": ""},
    {"selector": "40 x 40 | 4.5 mm", "tipo": "Cuadrado", "perfil": "40 x 40", "equiv_pulg": '1 1/2" x 1 1/2"', "lado_a_mm": 40, "lado_b_mm": 40, "espesor_mm": 4.5, "peso_kg_m": 4.52, "peso_6m_ficha": 27.12, "nota": ""},
    {"selector": "50 x 50 | 1.2 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 1.2, "peso_kg_m": 1.87, "peso_6m_ficha": 11.24, "nota": ""},
    {"selector": "50 x 50 | 1.5 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 1.5, "peso_kg_m": 2.25, "peso_6m_ficha": 13.50, "nota": ""},
    {"selector": "50 x 50 | 1.8 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 1.8, "peso_kg_m": 2.70, "peso_6m_ficha": 16.20, "nota": ""},
    {"selector": "50 x 50 | 2 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 2.0, "peso_kg_m": 3.12, "peso_6m_ficha": 18.73, "nota": ""},
    {"selector": "50 x 50 | 2.5 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 2.5, "peso_kg_m": 3.87, "peso_6m_ficha": 23.23, "nota": ""},
    {"selector": "50 x 50 | 3 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 3.0, "peso_kg_m": 4.49, "peso_6m_ficha": 26.94, "nota": ""},
    {"selector": "50 x 50 | 4 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 4.0, "peso_kg_m": 6.57, "peso_6m_ficha": 39.41, "nota": "Revisar: valor 4 mm (6.57 kg/m) mayor que 4.5 mm (6.02 kg/m)"},
    {"selector": "50 x 50 | 4.5 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 4.5, "peso_kg_m": 6.02, "peso_6m_ficha": 36.12, "nota": ""},
    {"selector": "50 x 50 | 6 mm", "tipo": "Cuadrado", "perfil": "50 x 50", "equiv_pulg": '2" x 2"', "lado_a_mm": 50, "lado_b_mm": 50, "espesor_mm": 6.0, "peso_kg_m": 8.54, "peso_6m_ficha": 51.21, "nota": ""},
    {"selector": "60 x 60 | 2 mm", "tipo": "Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60, "lado_b_mm": 60, "espesor_mm": 2.0, "peso_kg_m": 3.56, "peso_6m_ficha": 21.36, "nota": ""},
    {"selector": "60 x 60 | 2.5 mm", "tipo": "Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60, "lado_b_mm": 60, "espesor_mm": 2.5, "peso_kg_m": 4.39, "peso_6m_ficha": 26.34, "nota": ""},
    {"selector": "60 x 60 | 3 mm", "tipo": "Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60, "lado_b_mm": 60, "espesor_mm": 3.0, "peso_kg_m": 5.19, "peso_6m_ficha": 31.14, "nota": ""},
    {"selector": "60 x 60 | 4 mm", "tipo": "Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60, "lado_b_mm": 60, "espesor_mm": 4.0, "peso_kg_m": 7.14, "peso_6m_ficha": 42.86, "nota": ""},
    {"selector": "60 x 60 | 4.5 mm", "tipo": "Cuadrado", "perfil": "60 x 60", "equiv_pulg": '2 1/2" x 2 1/2"', "lado_a_mm": 60, "lado_b_mm": 60, "espesor_mm": 4.5, "peso_kg_m": 7.43, "peso_6m_ficha": 44.58, "nota": ""},
    {"selector": "75 x 75 | 1.5 mm", "tipo": "Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75, "lado_b_mm": 75, "espesor_mm": 1.5, "peso_kg_m": 3.41, "peso_6m_ficha": 20.43, "nota": ""},
    {"selector": "75 x 75 | 2 mm", "tipo": "Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75, "lado_b_mm": 75, "espesor_mm": 2.0, "peso_kg_m": 4.50, "peso_6m_ficha": 27.00, "nota": ""},
    {"selector": "75 x 75 | 2.5 mm", "tipo": "Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75, "lado_b_mm": 75, "espesor_mm": 2.5, "peso_kg_m": 5.56, "peso_6m_ficha": 33.36, "nota": ""},
    {"selector": "75 x 75 | 3 mm", "tipo": "Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75, "lado_b_mm": 75, "espesor_mm": 3.0, "peso_kg_m": 6.81, "peso_6m_ficha": 40.86, "nota": ""},
    {"selector": "75 x 75 | 4 mm", "tipo": "Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75, "lado_b_mm": 75, "espesor_mm": 4.0, "peso_kg_m": 8.59, "peso_6m_ficha": 51.54, "nota": ""},
    {"selector": "75 x 75 | 4.5 mm", "tipo": "Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75, "lado_b_mm": 75, "espesor_mm": 4.5, "peso_kg_m": 9.55, "peso_6m_ficha": 57.30, "nota": ""},
    {"selector": "75 x 75 | 6 mm", "tipo": "Cuadrado", "perfil": "75 x 75", "equiv_pulg": '3" x 3"', "lado_a_mm": 75, "lado_b_mm": 75, "espesor_mm": 6.0, "peso_kg_m": 13.11, "peso_6m_ficha": 78.66, "nota": ""},
    {"selector": "100 x 100 | 2 mm", "tipo": "Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100, "lado_b_mm": 100, "espesor_mm": 2.0, "peso_kg_m": 6.17, "peso_6m_ficha": 36.99, "nota": ""},
    {"selector": "100 x 100 | 2.5 mm", "tipo": "Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100, "lado_b_mm": 100, "espesor_mm": 2.5, "peso_kg_m": 7.68, "peso_6m_ficha": 46.05, "nota": ""},
    {"selector": "100 x 100 | 3 mm", "tipo": "Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100, "lado_b_mm": 100, "espesor_mm": 3.0, "peso_kg_m": 9.20, "peso_6m_ficha": 55.21, "nota": ""},
    {"selector": "100 x 100 | 4 mm", "tipo": "Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100, "lado_b_mm": 100, "espesor_mm": 4.0, "peso_kg_m": 12.17, "peso_6m_ficha": 73.03, "nota": ""},
    {"selector": "100 x 100 | 4.5 mm", "tipo": "Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100, "lado_b_mm": 100, "espesor_mm": 4.5, "peso_kg_m": 13.59, "peso_6m_ficha": 81.56, "nota": ""},
    {"selector": "100 x 100 | 6 mm", "tipo": "Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100, "lado_b_mm": 100, "espesor_mm": 6.0, "peso_kg_m": 16.98, "peso_6m_ficha": 101.88, "nota": ""},
    {"selector": "100 x 100 | 9.5 mm", "tipo": "Cuadrado", "perfil": "100 x 100", "equiv_pulg": '4" x 4"', "lado_a_mm": 100, "lado_b_mm": 100, "espesor_mm": 9.5, "peso_kg_m": 25.70, "peso_6m_ficha": 154.20, "nota": ""},
    {"selector": "125 x 125 | 3 mm", "tipo": "Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125, "lado_b_mm": 125, "espesor_mm": 3.0, "peso_kg_m": 11.31, "peso_6m_ficha": 67.86, "nota": ""},
    {"selector": "125 x 125 | 4 mm", "tipo": "Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125, "lado_b_mm": 125, "espesor_mm": 4.0, "peso_kg_m": 14.87, "peso_6m_ficha": 89.22, "nota": ""},
    {"selector": "125 x 125 | 4.5 mm", "tipo": "Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125, "lado_b_mm": 125, "espesor_mm": 4.5, "peso_kg_m": 17.17, "peso_6m_ficha": 103.02, "nota": ""},
    {"selector": "125 x 125 | 4.7 mm", "tipo": "Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125, "lado_b_mm": 125, "espesor_mm": 4.7, "peso_kg_m": 17.81, "peso_6m_ficha": 106.86, "nota": ""},
    {"selector": "125 x 125 | 6 mm", "tipo": "Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125, "lado_b_mm": 125, "espesor_mm": 6.0, "peso_kg_m": 21.69, "peso_6m_ficha": 130.14, "nota": ""},
    {"selector": "125 x 125 | 6.35 mm", "tipo": "Cuadrado", "perfil": "125 x 125", "equiv_pulg": '5" x 5"', "lado_a_mm": 125, "lado_b_mm": 125, "espesor_mm": 6.35, "peso_kg_m": 23.24, "peso_6m_ficha": 139.44, "nota": ""},
    {"selector": "150 x 150 | 3 mm", "tipo": "Cuadrado", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_a_mm": 150, "lado_b_mm": 150, "espesor_mm": 3.0, "peso_kg_m": 13.67, "peso_6m_ficha": 82.02, "nota": ""},
    {"selector": "150 x 150 | 4 mm", "tipo": "Cuadrado", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_a_mm": 150, "lado_b_mm": 150, "espesor_mm": 4.0, "peso_kg_m": 18.01, "peso_6m_ficha": 108.06, "nota": ""},
    {"selector": "150 x 150 | 4.5 mm", "tipo": "Cuadrado", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_a_mm": 150, "lado_b_mm": 150, "espesor_mm": 4.5, "peso_kg_m": 20.80, "peso_6m_ficha": 124.80, "nota": ""},
    {"selector": "150 x 150 | 6 mm", "tipo": "Cuadrado", "perfil": "150 x 150", "equiv_pulg": '6" x 6"', "lado_a_mm": 150, "lado_b_mm": 150, "espesor_mm": 6.0, "peso_kg_m": 27.39, "peso_6m_ficha": 164.32, "nota": ""},
    {"selector": "200 x 200 | 3 mm", "tipo": "Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200, "lado_b_mm": 200, "espesor_mm": 3.0, "peso_kg_m": 18.63, "peso_6m_ficha": 111.76, "nota": ""},
    {"selector": "200 x 200 | 4 mm", "tipo": "Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200, "lado_b_mm": 200, "espesor_mm": 4.0, "peso_kg_m": 24.29, "peso_6m_ficha": 145.74, "nota": ""},
    {"selector": "200 x 200 | 4.5 mm", "tipo": "Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200, "lado_b_mm": 200, "espesor_mm": 4.5, "peso_kg_m": 27.77, "peso_6m_ficha": 166.64, "nota": ""},
    {"selector": "200 x 200 | 4.7 mm", "tipo": "Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200, "lado_b_mm": 200, "espesor_mm": 4.7, "peso_kg_m": 29.21, "peso_6m_ficha": 175.26, "nota": ""},
    {"selector": "200 x 200 | 6 mm", "tipo": "Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200, "lado_b_mm": 200, "espesor_mm": 6.0, "peso_kg_m": 35.82, "peso_6m_ficha": 214.92, "nota": ""},
    {"selector": "200 x 200 | 8 mm", "tipo": "Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200, "lado_b_mm": 200, "espesor_mm": 8.0, "peso_kg_m": 48.68, "peso_6m_ficha": 292.10, "nota": ""},
    {"selector": "200 x 200 | 9 mm", "tipo": "Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200, "lado_b_mm": 200, "espesor_mm": 9.0, "peso_kg_m": 52.34, "peso_6m_ficha": 314.04, "nota": ""},
    {"selector": "200 x 200 | 9.5 mm", "tipo": "Cuadrado", "perfil": "200 x 200", "equiv_pulg": '8" x 8"', "lado_a_mm": 200, "lado_b_mm": 200, "espesor_mm": 9.5, "peso_kg_m": 56.08, "peso_6m_ficha": 336.48, "nota": ""},
    {"selector": "250 x 250 | 4.7 mm", "tipo": "Cuadrado", "perfil": "250 x 250", "equiv_pulg": '10" x 10"', "lado_a_mm": 250, "lado_b_mm": 250, "espesor_mm": 4.7, "peso_kg_m": 36.86, "peso_6m_ficha": 221.14, "nota": ""},
    {"selector": "250 x 250 | 6 mm", "tipo": "Cuadrado", "perfil": "250 x 250", "equiv_pulg": '10" x 10"', "lado_a_mm": 250, "lado_b_mm": 250, "espesor_mm": 6.0, "peso_kg_m": 45.24, "peso_6m_ficha": 271.44, "nota": ""},
    {"selector": "300 x 300 | 6 mm", "tipo": "Cuadrado", "perfil": "300 x 300", "equiv_pulg": '12" x 12"', "lado_a_mm": 300, "lado_b_mm": 300, "espesor_mm": 6.0, "peso_kg_m": 54.66, "peso_6m_ficha": 327.96, "nota": ""},
    {"selector": "300 x 300 | 8 mm", "tipo": "Cuadrado", "perfil": "300 x 300", "equiv_pulg": '12" x 12"', "lado_a_mm": 300, "lado_b_mm": 300, "espesor_mm": 8.0, "peso_kg_m": 73.82, "peso_6m_ficha": 442.90, "nota": ""},
]

CATALOGO_RECTANGULARES = [
    {"selector": "20 x 40 | 1.5 mm", "tipo": "Rectangular", "perfil": "20 x 40", "equiv_pulg": '3/4" x 1 1/2"', "lado_a_mm": 20, "lado_b_mm": 40, "espesor_mm": 1.5, "peso_kg_m": 1.35, "peso_6m_ficha": 8.12, "nota": ""},
    {"selector": "20 x 40 | 2 mm", "tipo": "Rectangular", "perfil": "20 x 40", "equiv_pulg": '3/4" x 1 1/2"', "lado_a_mm": 20, "lado_b_mm": 40, "espesor_mm": 2.0, "peso_kg_m": 1.70, "peso_6m_ficha": 10.20, "nota": ""},
    {"selector": "20 x 50 | 2 mm", "tipo": "Rectangular", "perfil": "20 x 50", "equiv_pulg": '3/4" x 2"', "lado_a_mm": 20, "lado_b_mm": 50, "espesor_mm": 2.0, "peso_kg_m": 2.10, "peso_6m_ficha": 12.60, "nota": ""},
    {"selector": "25 x 50 | 1.2 mm", "tipo": "Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25, "lado_b_mm": 50, "espesor_mm": 1.2, "peso_kg_m": 1.34, "peso_6m_ficha": 8.04, "nota": ""},
    {"selector": "25 x 50 | 1.5 mm", "tipo": "Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25, "lado_b_mm": 50, "espesor_mm": 1.5, "peso_kg_m": 1.65, "peso_6m_ficha": 9.90, "nota": ""},
    {"selector": "25 x 50 | 1.8 mm", "tipo": "Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25, "lado_b_mm": 50, "espesor_mm": 1.8, "peso_kg_m": 2.07, "peso_6m_ficha": 12.42, "nota": ""},
    {"selector": "25 x 50 | 2 mm", "tipo": "Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25, "lado_b_mm": 50, "espesor_mm": 2.0, "peso_kg_m": 2.26, "peso_6m_ficha": 13.57, "nota": ""},
    {"selector": "25 x 50 | 2.5 mm", "tipo": "Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25, "lado_b_mm": 50, "espesor_mm": 2.5, "peso_kg_m": 2.98, "peso_6m_ficha": 17.87, "nota": ""},
    {"selector": "25 x 50 | 3 mm", "tipo": "Rectangular", "perfil": "25 x 50", "equiv_pulg": '1" x 2"', "lado_a_mm": 25, "lado_b_mm": 50, "espesor_mm": 3.0, "peso_kg_m": 3.35, "peso_6m_ficha": 20.09, "nota": ""},
    {"selector": "40 x 50 | 2 mm", "tipo": "Rectangular", "perfil": "40 x 50", "equiv_pulg": "—", "lado_a_mm": 40, "lado_b_mm": 50, "espesor_mm": 2.0, "peso_kg_m": 2.62, "peso_6m_ficha": 15.72, "nota": ""},
    {"selector": "40 x 60 | 1.2 mm", "tipo": "Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40, "lado_b_mm": 60, "espesor_mm": 1.2, "peso_kg_m": 1.82, "peso_6m_ficha": 10.92, "nota": ""},
    {"selector": "40 x 60 | 1.5 mm", "tipo": "Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40, "lado_b_mm": 60, "espesor_mm": 1.5, "peso_kg_m": 2.26, "peso_6m_ficha": 13.56, "nota": ""},
    {"selector": "40 x 60 | 2 mm", "tipo": "Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40, "lado_b_mm": 60, "espesor_mm": 2.0, "peso_kg_m": 3.03, "peso_6m_ficha": 18.20, "nota": ""},
    {"selector": "40 x 60 | 2.5 mm", "tipo": "Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40, "lado_b_mm": 60, "espesor_mm": 2.5, "peso_kg_m": 3.60, "peso_6m_ficha": 21.60, "nota": ""},
    {"selector": "40 x 60 | 3 mm", "tipo": "Rectangular", "perfil": "40 x 60", "equiv_pulg": '1 1/2" x 1 3/4"', "lado_a_mm": 40, "lado_b_mm": 60, "espesor_mm": 3.0, "peso_kg_m": 4.25, "peso_6m_ficha": 25.50, "nota": ""},
    {"selector": "40 x 80 | 1.5 mm", "tipo": "Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40, "lado_b_mm": 80, "espesor_mm": 1.5, "peso_kg_m": 2.71, "peso_6m_ficha": 16.26, "nota": ""},
    {"selector": "40 x 80 | 1.8 mm", "tipo": "Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40, "lado_b_mm": 80, "espesor_mm": 1.8, "peso_kg_m": 3.29, "peso_6m_ficha": 19.76, "nota": ""},
    {"selector": "40 x 80 | 2 mm", "tipo": "Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40, "lado_b_mm": 80, "espesor_mm": 2.0, "peso_kg_m": 3.66, "peso_6m_ficha": 21.96, "nota": ""},
    {"selector": "40 x 80 | 2.5 mm", "tipo": "Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40, "lado_b_mm": 80, "espesor_mm": 2.5, "peso_kg_m": 4.39, "peso_6m_ficha": 26.34, "nota": ""},
    {"selector": "40 x 80 | 3 mm", "tipo": "Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40, "lado_b_mm": 80, "espesor_mm": 3.0, "peso_kg_m": 5.19, "peso_6m_ficha": 31.14, "nota": ""},
    {"selector": "40 x 80 | 4 mm", "tipo": "Rectangular", "perfil": "40 x 80", "equiv_pulg": '1 1/2" x 3 3/16"', "lado_a_mm": 40, "lado_b_mm": 80, "espesor_mm": 4.0, "peso_kg_m": 6.92, "peso_6m_ficha": 41.52, "nota": ""},
    {"selector": "50 x 70 | 2 mm", "tipo": "Rectangular", "perfil": "50 x 70", "equiv_pulg": "—", "lado_a_mm": 50, "lado_b_mm": 70, "espesor_mm": 2.0, "peso_kg_m": 3.58, "peso_6m_ficha": 21.48, "nota": ""},
    {"selector": "50 x 70 | 3 mm", "tipo": "Rectangular", "perfil": "50 x 70", "equiv_pulg": "—", "lado_a_mm": 50, "lado_b_mm": 70, "espesor_mm": 3.0, "peso_kg_m": 5.37, "peso_6m_ficha": 32.22, "nota": ""},
    {"selector": "50 x 75 | 1.8 mm", "tipo": "Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50, "lado_b_mm": 75, "espesor_mm": 1.8, "peso_kg_m": 3.25, "peso_6m_ficha": 19.52, "nota": ""},
    {"selector": "50 x 75 | 2 mm", "tipo": "Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50, "lado_b_mm": 75, "espesor_mm": 2.0, "peso_kg_m": 3.95, "peso_6m_ficha": 23.68, "nota": ""},
    {"selector": "50 x 75 | 2.5 mm", "tipo": "Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50, "lado_b_mm": 75, "espesor_mm": 2.5, "peso_kg_m": 4.88, "peso_6m_ficha": 29.28, "nota": ""},
    {"selector": "50 x 75 | 3 mm", "tipo": "Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50, "lado_b_mm": 75, "espesor_mm": 3.0, "peso_kg_m": 5.42, "peso_6m_ficha": 32.54, "nota": ""},
    {"selector": "50 x 75 | 4.5 mm", "tipo": "Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50, "lado_b_mm": 75, "espesor_mm": 4.5, "peso_kg_m": 7.98, "peso_6m_ficha": 47.88, "nota": ""},
    {"selector": "50 x 75 | 4.7 mm", "tipo": "Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50, "lado_b_mm": 75, "espesor_mm": 4.7, "peso_kg_m": 8.33, "peso_6m_ficha": 50.00, "nota": ""},
    {"selector": "50 x 75 | 6 mm", "tipo": "Rectangular", "perfil": "50 x 75", "equiv_pulg": '2" x 3"', "lado_a_mm": 50, "lado_b_mm": 75, "espesor_mm": 6.0, "peso_kg_m": 10.85, "peso_6m_ficha": 65.08, "nota": ""},
    {"selector": "50 x 100 | 1.8 mm", "tipo": "Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50, "lado_b_mm": 100, "espesor_mm": 1.8, "peso_kg_m": 3.96, "peso_6m_ficha": 23.76, "nota": ""},
    {"selector": "50 x 100 | 2 mm", "tipo": "Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50, "lado_b_mm": 100, "espesor_mm": 2.0, "peso_kg_m": 4.50, "peso_6m_ficha": 27.00, "nota": ""},
    {"selector": "50 x 100 | 2.5 mm", "tipo": "Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50, "lado_b_mm": 100, "espesor_mm": 2.5, "peso_kg_m": 5.56, "peso_6m_ficha": 33.36, "nota": ""},
    {"selector": "50 x 100 | 3 mm", "tipo": "Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50, "lado_b_mm": 100, "espesor_mm": 3.0, "peso_kg_m": 6.85, "peso_6m_ficha": 41.07, "nota": ""},
    {"selector": "50 x 100 | 4 mm", "tipo": "Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50, "lado_b_mm": 100, "espesor_mm": 4.0, "peso_kg_m": 8.59, "peso_6m_ficha": 51.54, "nota": ""},
    {"selector": "50 x 100 | 4.5 mm", "tipo": "Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50, "lado_b_mm": 100, "espesor_mm": 4.5, "peso_kg_m": 9.90, "peso_6m_ficha": 59.40, "nota": ""},
    {"selector": "50 x 100 | 4.7 mm", "tipo": "Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50, "lado_b_mm": 100, "espesor_mm": 4.7, "peso_kg_m": 10.22, "peso_6m_ficha": 61.33, "nota": ""},
    {"selector": "50 x 100 | 6 mm", "tipo": "Rectangular", "perfil": "50 x 100", "equiv_pulg": '2" x 4"', "lado_a_mm": 50, "lado_b_mm": 100, "espesor_mm": 6.0, "peso_kg_m": 13.20, "peso_6m_ficha": 79.20, "nota": ""},
    {"selector": "50 x 125 | 2 mm", "tipo": "Rectangular", "perfil": "50 x 125", "equiv_pulg": '2" x 5"', "lado_a_mm": 50, "lado_b_mm": 125, "espesor_mm": 2.0, "peso_kg_m": 5.44, "peso_6m_ficha": 32.64, "nota": ""},
    {"selector": "50 x 125 | 2.5 mm", "tipo": "Rectangular", "perfil": "50 x 125", "equiv_pulg": '2" x 5"', "lado_a_mm": 50, "lado_b_mm": 125, "espesor_mm": 2.5, "peso_kg_m": 6.80, "peso_6m_ficha": 40.80, "nota": ""},
    {"selector": "50 x 125 | 3 mm", "tipo": "Rectangular", "perfil": "50 x 125", "equiv_pulg": '2" x 5"', "lado_a_mm": 50, "lado_b_mm": 125, "espesor_mm": 3.0, "peso_kg_m": 8.16, "peso_6m_ficha": 48.96, "nota": ""},
    {"selector": "50 x 150 | 2 mm", "tipo": "Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50, "lado_b_mm": 150, "espesor_mm": 2.0, "peso_kg_m": 6.18, "peso_6m_ficha": 37.10, "nota": ""},
    {"selector": "50 x 150 | 2.5 mm", "tipo": "Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50, "lado_b_mm": 150, "espesor_mm": 2.5, "peso_kg_m": 7.70, "peso_6m_ficha": 46.19, "nota": ""},
    {"selector": "50 x 150 | 3 mm", "tipo": "Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50, "lado_b_mm": 150, "espesor_mm": 3.0, "peso_kg_m": 9.17, "peso_6m_ficha": 55.04, "nota": ""},
    {"selector": "50 x 150 | 4 mm", "tipo": "Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50, "lado_b_mm": 150, "espesor_mm": 4.0, "peso_kg_m": 11.73, "peso_6m_ficha": 70.38, "nota": ""},
    {"selector": "50 x 150 | 4.5 mm", "tipo": "Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50, "lado_b_mm": 150, "espesor_mm": 4.5, "peso_kg_m": 13.76, "peso_6m_ficha": 82.56, "nota": ""},
    {"selector": "50 x 150 | 4.7 mm", "tipo": "Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50, "lado_b_mm": 150, "espesor_mm": 4.7, "peso_kg_m": 14.37, "peso_6m_ficha": 86.23, "nota": ""},
    {"selector": "50 x 150 | 6 mm", "tipo": "Rectangular", "perfil": "50 x 150", "equiv_pulg": '2" x 6"', "lado_a_mm": 50, "lado_b_mm": 150, "espesor_mm": 6.0, "peso_kg_m": 18.26, "peso_6m_ficha": 109.56, "nota": ""},
    {"selector": "50 x 200 | 3 mm", "tipo": "Rectangular", "perfil": "50 x 200", "equiv_pulg": '2" x 8"', "lado_a_mm": 50, "lado_b_mm": 200, "espesor_mm": 3.0, "peso_kg_m": 11.75, "peso_6m_ficha": 70.50, "nota": ""},
    {"selector": "50 x 200 | 4.5 mm", "tipo": "Rectangular", "perfil": "50 x 200", "equiv_pulg": '2" x 8"', "lado_a_mm": 50, "lado_b_mm": 200, "espesor_mm": 4.5, "peso_kg_m": 17.45, "peso_6m_ficha": 104.70, "nota": ""},
    {"selector": "75 x 100 | 2 mm", "tipo": "Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75, "lado_b_mm": 100, "espesor_mm": 2.0, "peso_kg_m": 5.44, "peso_6m_ficha": 32.64, "nota": ""},
    {"selector": "75 x 100 | 3 mm", "tipo": "Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75, "lado_b_mm": 100, "espesor_mm": 3.0, "peso_kg_m": 8.16, "peso_6m_ficha": 48.96, "nota": ""},
    {"selector": "75 x 100 | 4 mm", "tipo": "Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75, "lado_b_mm": 100, "espesor_mm": 4.0, "peso_kg_m": 10.88, "peso_6m_ficha": 65.28, "nota": ""},
    {"selector": "75 x 100 | 4.5 mm", "tipo": "Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75, "lado_b_mm": 100, "espesor_mm": 4.5, "peso_kg_m": 12.07, "peso_6m_ficha": 72.42, "nota": ""},
    {"selector": "75 x 100 | 6 mm", "tipo": "Rectangular", "perfil": "75 x 100", "equiv_pulg": '3" x 4"', "lado_a_mm": 75, "lado_b_mm": 100, "espesor_mm": 6.0, "peso_kg_m": 15.87, "peso_6m_ficha": 95.22, "nota": ""},
    {"selector": "75 x 125 | 6 mm", "tipo": "Rectangular", "perfil": "75 x 125", "equiv_pulg": '3" x 5"', "lado_a_mm": 75, "lado_b_mm": 125, "espesor_mm": 6.0, "peso_kg_m": 17.96, "peso_6m_ficha": 107.75, "nota": ""},
    {"selector": "75 x 150 | 3 mm", "tipo": "Rectangular", "perfil": "75 x 150", "equiv_pulg": '3" x 6"', "lado_a_mm": 75, "lado_b_mm": 150, "espesor_mm": 3.0, "peso_kg_m": 10.55, "peso_6m_ficha": 63.30, "nota": ""},
    {"selector": "75 x 200 | 3 mm", "tipo": "Rectangular", "perfil": "75 x 200", "equiv_pulg": '3" x 8"', "lado_a_mm": 75, "lado_b_mm": 200, "espesor_mm": 3.0, "peso_kg_m": 12.94, "peso_6m_ficha": 77.64, "nota": ""},
    {"selector": "75 x 200 | 4.7 mm", "tipo": "Rectangular", "perfil": "75 x 200", "equiv_pulg": '3" x 8"', "lado_a_mm": 75, "lado_b_mm": 200, "espesor_mm": 4.7, "peso_kg_m": 20.27, "peso_6m_ficha": 121.64, "nota": ""},
    {"selector": "100 x 150 | 3 mm", "tipo": "Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100, "lado_b_mm": 150, "espesor_mm": 3.0, "peso_kg_m": 11.56, "peso_6m_ficha": 69.34, "nota": ""},
    {"selector": "100 x 150 | 4.5 mm", "tipo": "Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100, "lado_b_mm": 150, "espesor_mm": 4.5, "peso_kg_m": 17.17, "peso_6m_ficha": 103.02, "nota": ""},
    {"selector": "100 x 150 | 4.7 mm", "tipo": "Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100, "lado_b_mm": 150, "espesor_mm": 4.7, "peso_kg_m": 17.00, "peso_6m_ficha": 102.00, "nota": "Revisar: en catálogo 4.7 mm (17.00 kg/m) es menor que 4.5 mm (17.17 kg/m)"},
    {"selector": "100 x 150 | 6 mm", "tipo": "Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100, "lado_b_mm": 150, "espesor_mm": 6.0, "peso_kg_m": 21.70, "peso_6m_ficha": 130.20, "nota": ""},
    {"selector": '100 x 150 | 5/16" (7.94 mm)', "tipo": "Rectangular", "perfil": "100 x 150", "equiv_pulg": '4" x 6"', "lado_a_mm": 100, "lado_b_mm": 150, "espesor_mm": 7.94, "peso_kg_m": 28.39, "peso_6m_ficha": 170.34, "nota": ""},
    {"selector": "100 x 200 | 3 mm", "tipo": "Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100, "lado_b_mm": 200, "espesor_mm": 3.0, "peso_kg_m": 13.91, "peso_6m_ficha": 83.48, "nota": ""},
    {"selector": "100 x 200 | 4 mm", "tipo": "Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100, "lado_b_mm": 200, "espesor_mm": 4.0, "peso_kg_m": 18.45, "peso_6m_ficha": 110.72, "nota": ""},
    {"selector": "100 x 200 | 4.5 mm", "tipo": "Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100, "lado_b_mm": 200, "espesor_mm": 4.5, "peso_kg_m": 20.70, "peso_6m_ficha": 124.22, "nota": ""},
    {"selector": "100 x 200 | 6 mm", "tipo": "Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100, "lado_b_mm": 200, "espesor_mm": 6.0, "peso_kg_m": 26.40, "peso_6m_ficha": 158.40, "nota": ""},
    {"selector": "100 x 200 | 8 mm", "tipo": "Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100, "lado_b_mm": 200, "espesor_mm": 8.0, "peso_kg_m": 34.38, "peso_6m_ficha": 206.28, "nota": ""},
    {"selector": "100 x 200 | 9.3 mm", "tipo": "Rectangular", "perfil": "100 x 200", "equiv_pulg": '4" x 8"', "lado_a_mm": 100, "lado_b_mm": 200, "espesor_mm": 9.3, "peso_kg_m": 40.92, "peso_6m_ficha": 245.52, "nota": ""},
    {"selector": "100 x 250 | 4 mm", "tipo": "Rectangular", "perfil": "100 x 250", "equiv_pulg": '4" x 10"', "lado_a_mm": 100, "lado_b_mm": 250, "espesor_mm": 4.0, "peso_kg_m": 21.60, "peso_6m_ficha": 129.57, "nota": ""},
    {"selector": "100 x 250 | 4.5 mm", "tipo": "Rectangular", "perfil": "100 x 250", "equiv_pulg": '4" x 10"', "lado_a_mm": 100, "lado_b_mm": 250, "espesor_mm": 4.5, "peso_kg_m": 24.24, "peso_6m_ficha": 145.43, "nota": ""},
    {"selector": "100 x 250 | 6 mm", "tipo": "Rectangular", "perfil": "100 x 250", "equiv_pulg": '4" x 10"', "lado_a_mm": 100, "lado_b_mm": 250, "espesor_mm": 6.0, "peso_kg_m": 31.10, "peso_6m_ficha": 186.60, "nota": ""},
    {"selector": "150 x 200 | 4 mm", "tipo": "Rectangular", "perfil": "150 x 200", "equiv_pulg": '6" x 8"', "lado_a_mm": 150, "lado_b_mm": 200, "espesor_mm": 4.0, "peso_kg_m": 21.15, "peso_6m_ficha": 126.90, "nota": ""},
    {"selector": "150 x 200 | 4.5 mm", "tipo": "Rectangular", "perfil": "150 x 200", "equiv_pulg": '6" x 8"', "lado_a_mm": 150, "lado_b_mm": 200, "espesor_mm": 4.5, "peso_kg_m": 23.68, "peso_6m_ficha": 142.08, "nota": ""},
    {"selector": "150 x 200 | 6 mm", "tipo": "Rectangular", "perfil": "150 x 200", "equiv_pulg": '6" x 8"', "lado_a_mm": 150, "lado_b_mm": 200, "espesor_mm": 6.0, "peso_kg_m": 31.10, "peso_6m_ficha": 186.60, "nota": ""},
    {"selector": "150 x 250 | 6 mm", "tipo": "Rectangular", "perfil": "150 x 250", "equiv_pulg": '6" x 10"', "lado_a_mm": 150, "lado_b_mm": 250, "espesor_mm": 6.0, "peso_kg_m": 35.80, "peso_6m_ficha": 214.80, "nota": ""},
    {"selector": "150 x 300 | 4.5 mm", "tipo": "Rectangular", "perfil": "150 x 300", "equiv_pulg": '6" x 12"', "lado_a_mm": 150, "lado_b_mm": 300, "espesor_mm": 4.5, "peso_kg_m": 30.75, "peso_6m_ficha": 184.50, "nota": ""},
]

CATALOGO_TOTAL = CATALOGO_CUADRADOS + CATALOGO_RECTANGULARES
for item in CATALOGO_TOTAL:
    item["peso_6m_calc"] = round(item["peso_kg_m"] * 6.0, 2)
    item["area_m2_m"] = round(2.0 * (item["lado_a_mm"] + item["lado_b_mm"]) / 1000.0, 4)
    item["area_6m_m2"] = round(item["area_m2_m"] * 6.0, 4)

MAPA_PERFILES = {item["selector"]: item for item in CATALOGO_TOTAL}
LISTA_CUADRADOS = [item["selector"] for item in CATALOGO_CUADRADOS]
LISTA_RECTANGULARES = [item["selector"] for item in CATALOGO_RECTANGULARES]


# 3. Inicialización de Estado (Session State) para navegación guiada por pasos
if "paso" not in st.session_state:
    st.session_state.paso = 1

if "config" not in st.session_state:
    st.session_state.config = {
        "proyecto": "Estructura de Techo Metálico",
        "largo_comercial_m": 6.00,
        "ancho_corte_mm": 0.0,
        "num_tijerales": 4
    }

if "partidas" not in st.session_state:
    st.session_state.partidas = {
        "columnas": {
            "activo": True, "nombre": "Columnas", "es_tijeral": False,
            "tipo": "Cuadrado", "perfil": "100 x 100 | 3 mm", "cantidad": 8, "longitud_m": 4.50
        },
        "correas": {
            "activo": True, "nombre": "Correas", "es_tijeral": False,
            "tipo": "Rectangular", "perfil": "40 x 80 | 2 mm", "cantidad": 14, "longitud_m": 9.00
        },
        "brida_sup": {
            "activo": True, "nombre": "Tijeral - Brida Superior", "es_tijeral": True,
            "tipo": "Rectangular", "perfil": "50 x 100 | 2.5 mm", "cantidad": 2, "longitud_m": 6.20
        },
        "brida_inf": {
            "activo": True, "nombre": "Tijeral - Brida Inferior", "es_tijeral": True,
            "tipo": "Rectangular", "perfil": "50 x 100 | 2 mm", "cantidad": 1, "longitud_m": 12.00
        },
        "montantes": {
            "activo": True, "nombre": "Tijeral - Montantes", "es_tijeral": True,
            "tipo": "Cuadrado", "perfil": "40 x 40 | 2 mm", "cantidad": 9, "longitud_m": 1.10
        },
        "montantes_2": {
            "activo": False, "nombre": "Tijeral - Montantes / Diagonales (2.ª medida)", "es_tijeral": True,
            "tipo": "Rectangular", "perfil": "25 x 50 | 2 mm", "cantidad": 8, "longitud_m": 1.65
        }
    }


def ir_a_paso(nuevo_paso):
    st.session_state.paso = nuevo_paso


# 4. Función de cálculo exacto de barras, cortes y empalmes
def calcular_despiece_elemento(nombre_elem, perfil_info, cantidad_total, long_elem_m, largo_comercial_m, ancho_corte_mm):
    kerf_m = ancho_corte_mm / 1000.0
    peso_kg_m = perfil_info["peso_kg_m"]
    area_m2_m = perfil_info["area_m2_m"]

    metraje_requerido = cantidad_total * long_elem_m

    if largo_comercial_m > 0:
        tramos_completos = int(long_elem_m // largo_comercial_m)
        tramo_residual = round(long_elem_m % largo_comercial_m, 6)
        if abs(tramo_residual - largo_comercial_m) < 1e-6:
            tramo_residual = 0.0
            tramos_completos += 1
    else:
        tramos_completos = 0
        tramo_residual = 0.0

    if tramo_residual == 0:
        piezas_cortas_por_barra = 0
    else:
        denom = tramo_residual + kerf_m
        piezas_cortas_por_barra = int(math.floor((largo_comercial_m + kerf_m + 1e-9) / denom)) if denom > 0 else 0

    barras_completas = tramos_completos * cantidad_total

    if piezas_cortas_por_barra == 0:
        barras_tramos_cortos = 0
    else:
        barras_tramos_cortos = math.ceil(cantidad_total / piezas_cortas_por_barra)

    total_barras = barras_completas + barras_tramos_cortos

    if largo_comercial_m > 0:
        empalmes = cantidad_total * max(0, math.ceil(long_elem_m / largo_comercial_m) - 1)
    else:
        empalmes = 0

    piezas_necesarias = cantidad_total * (tramos_completos + (1 if tramo_residual > 0 else 0))
    metraje_comprado = total_barras * largo_comercial_m

    if barras_tramos_cortos == 0:
        perdida_cortes = 0.0
    else:
        if (largo_comercial_m - piezas_cortas_por_barra * tramo_residual - piezas_cortas_por_barra * kerf_m) >= -1e-7:
            perdida_barra_llena = piezas_cortas_por_barra * kerf_m
        else:
            perdida_barra_llena = max(0, piezas_cortas_por_barra - 1) * kerf_m

        piezas_ultima_barra = cantidad_total - (barras_tramos_cortos - 1) * piezas_cortas_por_barra
        if (largo_comercial_m - piezas_ultima_barra * tramo_residual - piezas_ultima_barra * kerf_m) >= -1e-7:
            perdida_ultima_barra = piezas_ultima_barra * kerf_m
        else:
            perdida_ultima_barra = max(0, piezas_ultima_barra - 1) * kerf_m

        perdida_cortes = (barras_tramos_cortos - 1) * perdida_barra_llena + perdida_ultima_barra

    sobrante_aprovechable = metraje_comprado - metraje_requerido - perdida_cortes
    peso_requerido = metraje_requerido * peso_kg_m
    peso_comprado = metraje_comprado * peso_kg_m
    area_requerida = metraje_requerido * area_m2_m
    area_comprada = metraje_comprado * area_m2_m

    if tramo_residual == 0:
        texto_plan = f"Usar {barras_completas} barra(s) completa(s); no requiere cortes de extensión."
    else:
        texto_plan = (
            f"Usar {barras_completas} barra(s) completa(s) de {largo_comercial_m:.2f} m "
            f"y cortar {cantidad_total} pieza(s) de {tramo_residual:.2f} m "
            f"desde {barras_tramos_cortos} barra(s) adicional(es) "
            f"(salen hasta {piezas_cortas_por_barra} piezas por barra)."
        )

    filas_plan = []
    if barras_completas > 0:
        filas_plan.append({
            "Elemento": nombre_elem,
            "Perfil": perfil_info["selector"],
            "N.° barra(s)": f"1 a {barras_completas}",
            "Tipo de uso": "Barras completas",
            "Piezas": barras_completas,
            "Largo/pieza (m)": round(largo_comercial_m, 2),
            "Metraje útil (m)": round(barras_completas * largo_comercial_m, 2),
            "Pérdida corte (m)": 0.0,
            "Sobrante (m)": 0.0,
            "Destino / indicación": "Tramos principales sin corte"
        })

    for i in range(1, barras_tramos_cortos + 1):
        num_barra = barras_completas + i
        tipo_uso = "Piezas cortas" if tramos_completos == 0 else "Extensiones"
        piezas_en_barra = min(piezas_cortas_por_barra, cantidad_total - (i - 1) * piezas_cortas_por_barra)
        largo_pieza = tramo_residual
        metraje_util = piezas_en_barra * largo_pieza

        if (largo_comercial_m - metraje_util - piezas_en_barra * kerf_m) >= -1e-7:
            perdida_barra = piezas_en_barra * kerf_m
        else:
            perdida_barra = max(0, piezas_en_barra - 1) * kerf_m

        sobrante_barra = max(0.0, largo_comercial_m - metraje_util - perdida_barra)

        filas_plan.append({
            "Elemento": nombre_elem,
            "Perfil": perfil_info["selector"],
            "N.° barra(s)": str(num_barra),
            "Tipo de uso": tipo_uso,
            "Piezas": piezas_en_barra,
            "Largo/pieza (m)": round(largo_pieza, 2),
            "Metraje útil (m)": round(metraje_util, 2),
            "Pérdida corte (m)": round(perdida_barra, 4),
            "Sobrante (m)": round(sobrante_barra, 2),
            "Destino / indicación": f"Cortar {piezas_en_barra} pieza(s) de {largo_pieza:.2f} m"
        })

    return {
        "Elemento": nombre_elem,
        "Tipo": perfil_info["tipo"],
        "Perfil": perfil_info["selector"],
        "Equiv. pulg.": perfil_info["equiv_pulg"],
        "Peso unit. (kg/m)": peso_kg_m,
        "Peso 6m ficha (kg)": perfil_info["peso_6m_ficha"],
        "Cant. Elementos": cantidad_total,
        "Longitud Final c/u (m)": long_elem_m,
        "Metraje Requerido (m)": round(metraje_requerido, 2),
        "Tramos Completos/Elem": tramos_completos,
        "Pieza Corta/Ext. (m)": round(tramo_residual, 2),
        "Piezas/Barra": piezas_cortas_por_barra,
        "Barras Completas": barras_completas,
        "Barras p/ Cortes": barras_tramos_cortos,
        "Tubos a Comprar": total_barras,
        "Empalmes": empalmes,
        "Piezas Totales": piezas_necesarias,
        "Metraje Comprado (m)": round(metraje_comprado, 2),
        "Pérdida Corte (m)": round(perdida_cortes, 3),
        "Sobrante (m)": round(sobrante_aprovechable, 2),
        "Peso Requerido (kg)": round(peso_requerido, 2),
        "Peso Compra (kg)": round(peso_comprado, 2),
        "Área Requerida (m²)": round(area_requerida, 2),
        "Área Compra (m²)": round(area_comprada, 2),
        "texto_plan": texto_plan,
        "df_plan": pd.DataFrame(filas_plan)
    }


# 5. Bloque interactivo para cada elemento estructural
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
            c1, c2, c3, c4 = st.columns([1.3, 2.2, 1.2, 1.3])
            with c1:
                opciones_tipo = ["Cuadrado", "Rectangular"]
                idx_tipo = opciones_tipo.index(datos["tipo"]) if datos["tipo"] in opciones_tipo else 0
                datos["tipo"] = st.selectbox(
                    "Tipo de Tubo",
                    options=opciones_tipo,
                    index=idx_tipo,
                    key=f"tipo_{clave}"
                )

            with c2:
                lista_perfiles = LISTA_CUADRADOS if datos["tipo"] == "Cuadrado" else LISTA_RECTANGULARES
                idx_perf = lista_perfiles.index(datos["perfil"]) if datos["perfil"] in lista_perfiles else 0
                datos["perfil"] = st.selectbox(
                    "Perfil y espesor (mm)",
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
            cant_real = datos["cantidad"] * num_tijerales if es_tijeral else datos["cantidad"]
            metraje_subtotal = cant_real * datos["longitud_m"]

            nota_extra = f" | Total en {num_tijerales} tijerales: **{cant_real} pzas**" if es_tijeral else ""
            st.caption(
                f"📌 **Ficha ASTM A500:** Equiv. `{info_p['equiv_pulg']}` | "
                f"Peso teórico: `{info_p['peso_kg_m']:.2f} kg/m` (`{info_p['peso_6m_ficha']:.2f} kg/barra 6m`) | "
                f"Área ext.: `{info_p['area_m2_m']:.2f} m²/m`{nota_extra} | "
                f"Metraje lineal neto: **{metraje_subtotal:.2f} m**"
            )
            if info_p["nota"]:
                st.warning(f"⚠️ {info_p['nota']}")


# 6. Barra Lateral: Navegación por pasos y resumen técnico ASTM A500
with st.sidebar:
    st.header("🧭 Pasos del Asistente")
    paso_actual = st.session_state.paso

    if st.button("1️⃣ Parámetros Generales", use_container_width=True, type="primary" if paso_actual == 1 else "secondary"):
        ir_a_paso(1)
        st.rerun()
    if st.button("2️⃣ Columnas y Correas", use_container_width=True, type="primary" if paso_actual == 2 else "secondary"):
        ir_a_paso(2)
        st.rerun()
    if st.button("3️⃣ Tijeral (Bridas y Montantes)", use_container_width=True, type="primary" if paso_actual == 3 else "secondary"):
        ir_a_paso(3)
        st.rerun()
    if st.button("4️⃣ Panorama Completo", use_container_width=True, type="primary" if paso_actual == 4 else "secondary"):
        ir_a_paso(4)
        st.rerun()

    st.divider()
    st.markdown("##### 📋 Especificaciones ASTM A500 Grado A")
    st.caption(
        "• **Proceso:** Laminado en caliente (LAC), soldadura ERW\n"
        "• **Fluencia mín.:** 269 MPa\n"
        "• **Tracción mín.:** 310 MPa\n"
        "• **Elongación (8\"):** 25.0% mín.\n"
        "• **Tolerancia espesor:** +/- 10%\n"
        "• **Tolerancia longitud:** +127 / -64 mm"
    )


# 7. Encabezado y Barra de Progreso
st.title("🏗️ Calculadora Estructural de Tubos Cuadrados y Rectangulares ASTM A500")

titulos_pasos = {
    1: "Paso 1 de 4: Configuración General del Proyecto",
    2: "Paso 2 de 4: Selección de Columnas y Correas",
    3: "Paso 3 de 4: Diseño del Tijeral (Brida Superior, Brida Inferior y Montantes)",
    4: "Paso 4 de 4: Panorama Completo de Compra, Metrado y Plan de Corte"
}
st.progress(st.session_state.paso / 4.0, text=titulos_pasos[st.session_state.paso])
st.divider()


# ==============================================================================
# PASO 1: CONFIGURACIÓN GENERAL
# ==============================================================================
if st.session_state.paso == 1:
    st.subheader("1️⃣ Configuración General de Barras y Corte")
    st.markdown("Configura los datos base del proyecto antes de seleccionar los perfiles de cada elemento estructural.")

    with st.container(border=True):
        st.session_state.config["proyecto"] = st.text_input(
            "Nombre del Proyecto / Obra",
            value=st.session_state.config["proyecto"]
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state.config["largo_comercial_m"] = st.number_input(
                "Largo comercial del tubo (m)",
                min_value=1.00,
                value=float(st.session_state.config["largo_comercial_m"]),
                step=0.50,
                format="%.2f",
                help="Longitud estándar de catálogo: 6.00 metros."
            )
        with col2:
            st.session_state.config["ancho_corte_mm"] = st.number_input(
                "Ancho de corte / disco (mm)",
                min_value=0.0,
                value=float(st.session_state.config["ancho_corte_mm"]),
                step=0.5,
                format="%.1f",
                help="Usa 0 mm para cálculo nominal o el espesor del disco de corte."
            )
        with col3:
            st.session_state.config["num_tijerales"] = st.number_input(
                "Cantidad de Tijerales iguales en el techo",
                min_value=1,
                value=int(st.session_state.config["num_tijerales"]),
                step=1,
                help="Multiplicará automáticamente las piezas de cada tijeral en el Paso 3."
            )

    st.write("")
    col_nav1, col_nav2 = st.columns([4, 1])
    with col_nav2:
        if st.button("Siguiente ➡️", type="primary", use_container_width=True):
            ir_a_paso(2)
            st.rerun()


# ==============================================================================
# PASO 2: COLUMNAS Y CORREAS
# ==============================================================================
elif st.session_state.paso == 2:
    st.subheader("2️⃣ Selección de Perfiles para Columnas y Correas")
    st.markdown("Elige si cada elemento lleva tubo **Cuadrado** o **Rectangular**, su medida, cantidad total y longitud final.")

    renderizar_bloque_elemento(
        "columnas",
        "🏛️ Columnas",
        "Elementos verticales de soporte principal del techo.",
        es_tijeral=False
    )

    renderizar_bloque_elemento(
        "correas",
        "📏 Correas",
        "Perfiles longitudinales de soporte de cobertura.",
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
# PASO 3: TIJERAL (BRIDA SUPERIOR, BRIDA INFERIOR, MONTANTES)
# ==============================================================================
elif st.session_state.paso == 3:
    st.subheader("3️⃣ Selección de Perfiles para el Tijeral")

    col_tij1, col_tij2 = st.columns([1, 3])
    with col_tij1:
        st.session_state.config["num_tijerales"] = st.number_input(
            "N.° de Tijerales iguales",
            min_value=1,
            value=int(st.session_state.config["num_tijerales"]),
            step=1
        )
    with col_tij2:
        st.info(
            f"💡 Ingresa abajo las piezas para **1 tijeral**. "
            f"El sistema multiplicará automáticamente las cantidades por **{st.session_state.config['num_tijerales']} tijeral(es)**."
        )

    n_tij = st.session_state.config["num_tijerales"]

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
        "Cordón o tirante horizontal inferior del tijeral.",
        es_tijeral=True,
        num_tijerales=n_tij
    )

    renderizar_bloque_elemento(
        "montantes",
        "⏸️ Tijeral — Montantes",
        "Elementos internos verticales o diagonales del tijeral (Medida principal).",
        es_tijeral=True,
        num_tijerales=n_tij
    )

    renderizar_bloque_elemento(
        "montantes_2",
        "📐 Tijeral — Montantes / Diagonales (2.ª medida opcional)",
        "Activa esta casilla si el tijeral lleva un segundo grupo de montantes o diagonales con otra longitud o perfil.",
        es_tijeral=True,
        num_tijerales=n_tij
    )

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
# PASO 4: PANORAMA COMPLETO DE COMPRA, METRADO Y PLAN DE CORTE
# ==============================================================================
elif st.session_state.paso == 4:
    cfg = st.session_state.config
    st.subheader(f"📊 Panorama Completo del Proyecto: {cfg['proyecto']}")
    st.caption(
        f"Largo comercial de barra: **{cfg['largo_comercial_m']:.2f} m** | "
        f"Ancho de corte: **{cfg['ancho_corte_mm']:.1f} mm** | "
        f"Tijerales considerados: **{cfg['num_tijerales']} unid.**"
    )

    resultados_partidas = []
    planes_corte_dfs = []

    for clave, item in st.session_state.partidas.items():
        if item["activo"]:
            cant_final = item["cantidad"] * cfg["num_tijerales"] if item["es_tijeral"] else item["cantidad"]
            perfil_info = MAPA_PERFILES[item["perfil"]]
            res_elem = calcular_despiece_elemento(
                nombre_elem=item["nombre"],
                perfil_info=perfil_info,
                cantidad_total=cant_final,
                long_elem_m=item["longitud_m"],
                largo_comercial_m=cfg["largo_comercial_m"],
                ancho_corte_mm=cfg["ancho_corte_mm"]
            )
            resultados_partidas.append(res_elem)
            planes_corte_dfs.append(res_elem["df_plan"])

    if not resultados_partidas:
        st.warning("No hay elementos activos. Regresa a los pasos anteriores y selecciona al menos un elemento.")
    else:
        df_resumen_elementos = pd.DataFrame([
            {k: v for k, v in r.items() if k not in ("texto_plan", "df_plan")}
            for r in resultados_partidas
        ])

        # 1. Tarjetas de Resumen Global
        total_tubos_proyecto = int(df_resumen_elementos["Tubos a Comprar"].sum())
        peso_total_compra = df_resumen_elementos["Peso Compra (kg)"].sum()
        peso_total_req = df_resumen_elementos["Peso Requerido (kg)"].sum()
        area_total_pintura = df_resumen_elementos["Área Requerida (m²)"].sum()
        empalmes_totales = int(df_resumen_elementos["Empalmes"].sum())
        sobrante_total = df_resumen_elementos["Sobrante (m)"].sum()

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("TUBOS A COMPRAR", f"{total_tubos_proyecto} barras")
        k2.metric("PESO TOTAL COMPRA", f"{peso_total_compra:,.2f} kg", delta=f"Neto: {peso_total_req:,.2f} kg")
        k3.metric("ÁREA EXT. REQUERIDA", f"{area_total_pintura:,.2f} m²")
        k4.metric("EMPALMES TOTALES", f"{empalmes_totales} unid.")
        k5.metric("SOBRANTE TOTAL", f"{sobrante_total:,.2f} m")

        st.divider()

        tab_consolidado, tab_elementos, tab_cortes, tab_catalogo = st.tabs([
            "🛒 1. Orden de Compra Consolidada",
            "📐 2. Metrado por Elemento (Columnas, Correas, Tijeral)",
            "🪚 3. Plan de Corte Barra por Barra",
            "📒 4. Catálogo ASTM A500 (Cuadrados y Rectangulares)"
        ])

        with tab_consolidado:
            st.markdown("#### 🛒 Resumen Consolidado de Compra por Tipo de Perfil")
            st.caption("Totaliza las barras a comprar agrupando los elementos que comparten el mismo perfil.")
            df_compra = (
                df_resumen_elementos.groupby(
                    ["Tipo", "Perfil", "Equiv. pulg.", "Peso unit. (kg/m)", "Peso 6m ficha (kg)"],
                    as_index=False
                )
                .agg({
                    "Metraje Requerido (m)": "sum",
                    "Tubos a Comprar": "sum",
                    "Metraje Comprado (m)": "sum",
                    "Sobrante (m)": "sum",
                    "Peso Compra (kg)": "sum",
                    "Área Compra (m²)": "sum"
                })
            )
            st.dataframe(df_compra, use_container_width=True, hide_index=True)

            csv_compra = df_compra.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "⬇️ Descargar Orden de Compra Consolidada (CSV)",
                data=csv_compra,
                file_name="orden_compra_astm_a500.csv",
                mime="text/csv"
            )

        with tab_elementos:
            st.markdown("#### 📐 Desglose Completo por Elemento Estructural")
            st.dataframe(df_resumen_elementos, use_container_width=True, hide_index=True)

            csv_elem = df_resumen_elementos.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "⬇️ Descargar Metrado por Elemento (CSV)",
                data=csv_elem,
                file_name="metrado_por_elemento_techo.csv",
                mime="text/csv"
            )

        with tab_cortes:
            st.markdown("#### 🪚 Plan de Barras y Cortes Detallado")
            for r in resultados_partidas:
                with st.expander(f"📌 {r['Elemento']} — Perfil: {r['Perfil']} ({r['Tubos a Comprar']} barras)", expanded=True):
                    st.info(f"**Resumen de corte:** {r['texto_plan']}")
                    st.dataframe(r["df_plan"], use_container_width=True, hide_index=True)

            df_todos_cortes = pd.concat(planes_corte_dfs, ignore_index=True)
            csv_cortes = df_todos_cortes.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "⬇️ Descargar Plan de Corte Completo (CSV)",
                data=csv_cortes,
                file_name="plan_corte_completo_taller.csv",
                mime="text/csv"
            )

        with tab_catalogo:
            st.markdown("#### 📒 Catálogo Oficial ASTM A500 (68 Cuadrados + 78 Rectangulares)")
            col_prop1, col_prop2 = st.columns(2)
            with col_prop1:
                st.info(
                    "**Propiedades Mecánicas (ASTM A500 / AISI A500 Grado A):**\n"
                    "- Límite de Fluencia mín.: **269 MPa**\n"
                    "- Resistencia a la Tracción mín.: **310 MPa**\n"
                    "- Elongación (Probeta 8\"): **25.0% mínimo**"
                )
            with col_prop2:
                st.info(
                    "**Características y Tolerancias:**\n"
                    "- Acero estructural laminado en caliente (LAC), soldadura ERW, barras de **6 m**\n"
                    "- Tolerancia en Espesor: **+/- 10%**\n"
                    "- Tolerancia en Longitud: **+127 / -64 mm**"
                )

            df_cat_vista = pd.DataFrame(CATALOGO_TOTAL)[[
                "tipo", "selector", "equiv_pulg", "lado_a_mm", "lado_b_mm",
                "espesor_mm", "peso_kg_m", "peso_6m_ficha", "area_m2_m", "area_6m_m2", "nota"
            ]].rename(columns={
                "tipo": "Geometría",
                "selector": "Perfil | Espesor",
                "equiv_pulg": "Equiv. Pulg.",
                "lado_a_mm": "Lado A (mm)",
                "lado_b_mm": "Lado B (mm)",
                "espesor_mm": "Espesor (mm)",
                "peso_kg_m": "Peso Teórico (kg/m)",
                "peso_6m_ficha": "Peso 6 m Ficha (kg)",
                "area_m2_m": "Área Ext. (m²/m)",
                "area_6m_m2": "Área 6 m (m²)",
                "nota": "Control del Dato"
            })
            st.dataframe(df_cat_vista, use_container_width=True, hide_index=True, height=500)

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
