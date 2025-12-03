# Exámenes AIST

Esta carpeta contiene los enunciados de exámenes y sus soluciones del curso AIST (Architectures et Ingénierie des Systèmes de Transmission).

## Estructura

Cada examen tiene dos archivos:
- `Enunciado_XXXX.tex`: Enunciado del examen (statement)
- `Soluciones_XXXX.tex`: Soluciones completas con desarrollo detallado

## Contenido por Año

### 2019 (Diciembre)
- **Parte A - RF**: Sistema satelital Globalstar (LEO)
  - Técnicas CDMA/FDMA con multi-beam
  - Enlaces Utilizador ↔ Satélite ↔ Gateway
  - Bilanes de enlace en bandas L, S y C
  
- **Parte B - Óptica**: Liaison DWDM no amplificada
  - Aplicaciones metro (interconexión centros de datos)
  - Transpondeurs 100/200/400 Gbit/s
  - Budget de enlace y alcance máximo

### 2020 (Diciembre)
- **Parte A - RF**: Enlace radio TéraHertz (340 GHz)
  - Transmisiones de corto alcance y muy alto débito
  - Atenuación atmosférica y lluvia
  - Arquitectura de receptor THz
  
- **Parte B - Óptica**: Ingeniería de enlace WDM amplificado
  - Maximización de capacidad total
  - Selección de transpondeurs
  - Optimización OSNR

### 2022 (Diciembre)

#### RF: Sistema HAPS (High-Altitude Platform Station)
- Plataforma a 20-50 km de altitud
- Enlaces HAPS ↔ Estación terrestre
- Dos bandas: Ka (31 GHz) y E (85 GHz)
- Modulaciones QPSK y 256-QAM
- Condiciones de cielo claro y con lluvia (R=25 mm/h)

#### Óptica: Cable submarino entre dos países
- Tres rutas: Norte (3500 km), Central (3000 km), Sur (4000 km)
- Upgrade a transmisión coherente WDM
- Selección de transpondeurs (DP-QPSK, DP-8QAM, DP-16QAM)
- Maximización de capacidad con margen OSNR de 1 dB

### 2023 (Diciembre)
- **Parte Óptica únicamente**: Sistema de cable submarino 8260 km
  - Canales DP-8QAM 100 Gbit/s
  - Espaciado de amplificadores EDFA
  - Eficiencia espectral del sistema
  - Comparación con DP-QPSK

### 2024 (Marzo)
- **Parte A - RF**: Enlaces terrestres y satelitales E-band (83.5 GHz)
  - Enlace terrestre point-to-point (40 km)
  - Enlace con satélite LEO (2000 km)
  - Arquitecturas de transmisión/recepción
  - Modulación QPSK, 5 GHz de ancho de banda
  
- **Parte B - Óptica**: DWDM sin amplificadores en línea
  - Aplicación metropolitana (Data Center Interconnection)
  - Configuraciones A/B/C con transpondeurs 100/200/400 Gbit/s
  - Margen OSNR de 2 dB
  - Budget y alcance máximo

## Temas Principales

### RF
- Bilanes de enlace (link budget)
- Pérdidas en espacio libre (FSL)
- Atenuación atmosférica y por lluvia
- Arquitecturas: Superheterodino, Homodino, Low-IF
- Fórmula de Friis (factor de ruido en cascada)
- Antenas parabólicas y ganancia
- Modulaciones digitales (QPSK, 16-QAM, 64-QAM, 256-QAM)
- Enlaces satelitales (LEO, GEO)

### Óptica
- OSNR (Optical Signal-to-Noise Ratio)
- Amplificadores EDFA (ASE noise)
- Sistemas WDM/DWDM
- Transpondeurs coherentes (DP-QPSK, DP-8QAM, DP-16QAM, DP-64QAM)
- Ingeniería de enlaces: número de amplificadores, espaciado
- Budget de enlace óptico
- Eficiencia espectral
- Cables submarinos de larga distancia

## Compilación

Para compilar cualquier archivo LaTeX:

```bash
pdflatex Enunciado_2022_RF.tex
pdflatex Soluciones_2022_RF.tex
```

## Notas

- Los enunciados están en francés o inglés según el año
- Las soluciones incluyen desarrollo matemático completo
- Se proporcionan explicaciones conceptuales además de cálculos
- Algunos exámenes tienen anexos con gráficas y tablas de datos
