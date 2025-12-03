# Formularios y Resúmenes AIST

Esta carpeta contiene materiales de referencia para el curso AIST.

## Contenido

### Formulario_AIST.tex
Formulario compacto de una página (formato landscape, 3 columnas) con todas las fórmulas esenciales:

**Sección RF:**
- Fórmulas de antenas (ganancia, ancho de haz)
- Pérdidas en espacio libre (FSL)
- Pérdidas adicionales (atmosfera, lluvia, polarización)
- Link budget
- Ruido y fórmula de Friis
- Modulaciones y eficiencia espectral
- Enlaces satelitales

**Sección Óptica:**
- Line rate y eficiencia espectral
- OSNR (fórmulas de cálculo)
- ASE noise
- Ingeniería de enlaces (amplificadores, canales)
- Budget de enlaces no amplificados
- Tipos de fibra

**Conversiones y constantes:**
- dB ↔ Lineal
- Frecuencia ↔ Longitud de onda
- Bandas de frecuencia RF y ópticas
- Constantes físicas

### Formulario_AIST_NUEVO.tex
Versión extendida y mejorada del formulario con:
- Diagramas visuales (arquitectura WDM)
- Tablas de referencia (modulaciones, pérdidas ópticas, amplificadores)
- Sección de procedimientos paso a paso
- Conceptos clave explicados
- Estrategia para exámenes (metodología, verificaciones)
- Sanity checks (valores típicos)

### Resumen_Teoria_AIST.tex
Documento completo de teoría (múltiples páginas) que incluye:

**Arquitecturas de Emisores y Receptores:**
- Superheterodino (problema de frecuencia imagen)
- Homodino (DC offset, radiación del OL)
- Low-IF (rechazo de imagen con Hartley/Weaver)

**Componentes:**
- Oscilador Local y sintetizador de frecuencia
- Mezclador (pérdidas de conversión)
- LNA (amplificador de bajo ruido)
- Antenas (tipos, patrones)

**Sistemas de Transmisión:**
- RF: Link budget detallado, temperatura de ruido, multi-hop
- Óptica: EDFA, WDM, efectos no lineales

**Conceptos teóricos:**
- Explicaciones conceptuales profundas
- Teoremas y principios físicos
- Metodología de diseño

## Uso Recomendado

1. **Para exámenes**: Usar `Formulario_AIST_NUEVO.tex` (más completo, con procedimientos)
2. **Para consulta rápida**: Usar `Formulario_AIST.tex` (compacto, formato 1 página)
3. **Para estudio**: Usar `Resumen_Teoria_AIST.tex` (explicaciones detalladas)

## Compilación

```bash
pdflatex Formulario_AIST_NUEVO.tex
pdflatex Formulario_AIST.tex
pdflatex Resumen_Teoria_AIST.tex
```

**Nota**: El `Formulario_AIST_NUEVO.tex` usa el paquete `tikz` para diagramas.

## Formato

- **Formularios**: Diseñados para impresión en A4 horizontal (landscape)
- **Resumen**: Formato A4 vertical estándar
- **Tipografía**: Optimizada para máxima densidad de información legible
