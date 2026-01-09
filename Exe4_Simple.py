"""
EJERCICIO 4 - SIMULACIÓN DE FIBRA ÓPTICA (VERSIÓN SIMPLE)
==========================================================

Este programa simula cómo se propaga una señal digital en una fibra óptica.
Código muy simple, paso a paso, con explicaciones.

Autor: Estudiante IMT Atlantique
Fecha: Enero 2026
"""

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# PASO 0: CONFIGURACIÓN - CAMBIA ESTOS VALORES PARA DIFERENTES CASOS
# =============================================================================

# ¿Cuántos bits queremos enviar?
numero_bits = 100  # Empezamos con pocos bits para que sea rápido

# ¿A qué velocidad enviamos? (bits por segundo)
velocidad = 10e9  # 10 Gigabits/segundo (10 Gb/s)

# ¿Cuántas muestras usamos para dibujar cada bit?
muestras_por_bit = 32  # Más muestras = gráfico más suave

# ¿Qué fibra usamos?
longitud_fibra_km = 50  # 50 kilómetros
dispersion = 17  # ps/(nm·km) - típico de fibra G.652

# Constantes físicas
longitud_onda_nm = 1550  # nanómetros (1550 nm es estándar)
velocidad_luz = 3e8  # metros/segundo

print("="*60)
print("SIMULACIÓN DE FIBRA ÓPTICA - VERSIÓN SIMPLE")
print("="*60)
print(f"Bits a transmitir: {numero_bits}")
print(f"Velocidad: {velocidad/1e9:.0f} Gb/s")
print(f"Longitud de fibra: {longitud_fibra_km} km")
print(f"Dispersión: {dispersion} ps/(nm·km)")
print("="*60)

# =============================================================================
# PASO 1: CREAR UNA SECUENCIA DE BITS ALEATORIA
# =============================================================================
print("\nPASO 1: Generando secuencia de bits aleatoria...")

# Crear bits aleatorios (0 o 1)
bits = np.random.randint(0, 2, numero_bits)

# Mostrar los primeros 20 bits
print(f"Primeros 20 bits: {bits[:20]}")

# =============================================================================
# PASO 2: CONVERTIR BITS A SEÑAL NRZ (Non-Return-to-Zero)
# =============================================================================
print("\nPASO 2: Convirtiendo bits a señal NRZ...")

# Calcular valores básicos
tiempo_por_bit = 1 / velocidad  # cuánto dura cada bit (en segundos)
frecuencia_muestreo = velocidad * muestras_por_bit  # Hz

print(f"Tiempo por bit: {tiempo_por_bit*1e12:.1f} picosegundos")
print(f"Frecuencia de muestreo: {frecuencia_muestreo/1e9:.1f} GHz")

# Crear la señal NRZ: cada bit se repite varias veces
# Si bit=0 → 1 Volt, si bit=1 → 2 Volts
señal_nrz = np.repeat(bits, muestras_por_bit)  # repetir cada bit
señal_nrz = señal_nrz + 1  # convertir [0,1] a [1,2] Volts

# Crear eje de tiempo (en nanosegundos para el gráfico)
total_muestras = len(señal_nrz)
tiempo_ns = np.arange(total_muestras) / frecuencia_muestreo * 1e9  # nanosegundos

print(f"Total de muestras: {total_muestras}")

# =============================================================================
# PASO 3: CALCULAR DISPERSIÓN EN LA FIBRA
# =============================================================================
print("\nPASO 3: Calculando efecto de dispersión...")

# Convertir unidades a SI (Sistema Internacional)
L = longitud_fibra_km * 1000  # km → metros
D = dispersion * 1e-12 / 1e-9 / 1000  # ps/(nm·km) → s/m²
lambda_m = longitud_onda_nm * 1e-9  # nm → metros

# Calcular beta2 (parámetro de dispersión)
# Esta es la fórmula que relaciona D con beta2
beta2 = -(D * lambda_m**2) / (2 * np.pi * velocidad_luz)

print(f"Beta2 = {beta2:.3e} s²/m")

# =============================================================================
# PASO 4: PROPAGAR LA SEÑAL EN LA FIBRA (usando FFT)
# =============================================================================
print("\nPASO 4: Propagando señal en la fibra...")

# ¿Por qué FFT? Porque es más fácil calcular la dispersión en frecuencia
# FFT = Fast Fourier Transform (convierte tiempo → frecuencia)

# 4.1: Transformar señal a frecuencia
señal_frecuencia = np.fft.fft(señal_nrz)

# 4.2: Crear eje de frecuencias
N = len(señal_nrz)
frecuencias = np.fft.fftfreq(N, 1/frecuencia_muestreo)
omega = 2 * np.pi * frecuencias  # frecuencia angular (rad/s)

# 4.3: Aplicar dispersión
# La dispersión hace que diferentes frecuencias viajen a diferentes velocidades
# Esto se modela con una fase que depende de omega²
fase_dispersion = np.exp(1j * (beta2/2) * omega**2 * L)
señal_dispersada_freq = señal_frecuencia * fase_dispersion

# 4.4: Volver al dominio del tiempo
señal_salida = np.fft.ifft(señal_dispersada_freq)
señal_salida = np.real(señal_salida)  # tomar solo parte real

print("✓ Propagación completada")

# =============================================================================
# PASO 5: SIMULAR FOTODIODO (detector)
# =============================================================================
print("\nPASO 5: Simulando detección con fotodiodo...")

# El fotodiodo detecta potencia óptica, que es proporcional al cuadrado
# de la amplitud del campo eléctrico
fotocorriente = señal_salida**2

# Eliminar componente DC (continua)
fotocorriente = fotocorriente - np.mean(fotocorriente)

print("✓ Detección completada")

# =============================================================================
# PASO 6: GRAFICAR RESULTADOS
# =============================================================================
print("\nPASO 6: Generando gráficos...")

# Cuántos bits mostrar (para no saturar el gráfico)
bits_a_mostrar = min(50, numero_bits)
muestras_a_mostrar = bits_a_mostrar * muestras_por_bit

# -------------------------
# GRÁFICO 1: Señal de entrada
# -------------------------
plt.figure(figsize=(14, 10))

plt.subplot(4, 1, 1)
plt.plot(tiempo_ns[:muestras_a_mostrar], señal_nrz[:muestras_a_mostrar], 
         'b-', linewidth=2, label='Señal NRZ')
plt.xlabel('Tiempo (ns)')
plt.ylabel('Amplitud (V)')
plt.title(f'SEÑAL DE ENTRADA - {velocidad/1e9:.0f} Gb/s', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()
plt.ylim([0.5, 2.5])

# -------------------------
# GRÁFICO 2: Señal después de la fibra
# -------------------------
plt.subplot(4, 1, 2)
plt.plot(tiempo_ns[:muestras_a_mostrar], señal_salida[:muestras_a_mostrar], 
         'r-', linewidth=2, label=f'Después de {longitud_fibra_km} km')
plt.xlabel('Tiempo (ns)')
plt.ylabel('Amplitud (V)')
plt.title(f'SEÑAL DESPUÉS DE LA FIBRA - Dispersión visible', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()

# -------------------------
# GRÁFICO 3: Comparación entrada vs salida
# -------------------------
plt.subplot(4, 1, 3)
plt.plot(tiempo_ns[:muestras_a_mostrar], señal_nrz[:muestras_a_mostrar], 
         'b-', linewidth=2, alpha=0.7, label='Entrada')
plt.plot(tiempo_ns[:muestras_a_mostrar], señal_salida[:muestras_a_mostrar], 
         'r-', linewidth=2, alpha=0.7, label='Salida')
plt.xlabel('Tiempo (ns)')
plt.ylabel('Amplitud (V)')
plt.title('COMPARACIÓN: Entrada vs Salida', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()

# -------------------------
# GRÁFICO 4: Fotocorriente detectada
# -------------------------
plt.subplot(4, 1, 4)
plt.plot(tiempo_ns[:muestras_a_mostrar], fotocorriente[:muestras_a_mostrar], 
         'g-', linewidth=2, label='Fotocorriente')
plt.xlabel('Tiempo (ns)')
plt.ylabel('Corriente (u.a.)')
plt.title('SEÑAL DETECTADA (después del fotodiodo)', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

# =============================================================================
# PASO 7: CALCULAR ESPECTRO (opcional pero útil)
# =============================================================================
print("\nPASO 7: Calculando espectros...")

# Calcular espectro de entrada
espectro_entrada = np.abs(np.fft.fft(señal_nrz)) / N
espectro_entrada = np.fft.fftshift(espectro_entrada)

# Calcular espectro de salida
espectro_salida = np.abs(np.fft.fft(señal_salida)) / N
espectro_salida = np.fft.fftshift(espectro_salida)

# Eje de frecuencias (en GHz)
freqs_plot = np.fft.fftshift(frecuencias) / 1e9

# Gráfico de espectros
plt.figure(figsize=(14, 6))

plt.subplot(1, 2, 1)
# Convertir a dB para ver mejor
espectro_entrada_dB = 20 * np.log10(espectro_entrada + 1e-10)
plt.plot(freqs_plot, espectro_entrada_dB, 'b-', linewidth=1.5)
plt.xlabel('Frecuencia (GHz)')
plt.ylabel('Magnitud (dB)')
plt.title('ESPECTRO DE ENTRADA', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xlim([-3*velocidad/1e9, 3*velocidad/1e9])

plt.subplot(1, 2, 2)
espectro_salida_dB = 20 * np.log10(espectro_salida + 1e-10)
plt.plot(freqs_plot, espectro_salida_dB, 'r-', linewidth=1.5)
plt.xlabel('Frecuencia (GHz)')
plt.ylabel('Magnitud (dB)')
plt.title('ESPECTRO DE SALIDA', fontsize=12, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xlim([-3*velocidad/1e9, 3*velocidad/1e9])

plt.tight_layout()

# =============================================================================
# RESUMEN Y ANÁLISIS
# =============================================================================
print("\n" + "="*60)
print("RESUMEN DE LA SIMULACIÓN")
print("="*60)

# Calcular ensanchamiento aproximado del pulso
# (comparando ancho de entrada vs salida)
print(f"\nParámetros de transmisión:")
print(f"  • Velocidad: {velocidad/1e9:.0f} Gb/s")
print(f"  • Período de bit: {tiempo_por_bit*1e12:.1f} ps")
print(f"  • Longitud de fibra: {longitud_fibra_km} km")
print(f"  • Dispersión: {dispersion} ps/(nm·km)")

# Estimación teórica del ensanchamiento
# Δt ≈ D × L × Δλ (asumiendo Δλ ≈ 0.1 nm típico)
delta_lambda_nm = 0.1  # ancho espectral típico
ensanchamiento_ps = dispersion * longitud_fibra_km * delta_lambda_nm

print(f"\nEnsanchamiento teórico estimado: {ensanchamiento_ps:.1f} ps")
print(f"Ensanchamiento relativo: {ensanchamiento_ps/(tiempo_por_bit*1e12)*100:.1f}%")

if ensanchamiento_ps < 0.2 * tiempo_por_bit * 1e12:
    print("\n✓ Dispersión BAJA - Señal bien preservada")
    print("  La transmisión funcionará correctamente.")
elif ensanchamiento_ps < 0.5 * tiempo_por_bit * 1e12:
    print("\n⚠ Dispersión MODERADA - Señal degradada")
    print("  La transmisión puede funcionar pero con errores.")
else:
    print("\n✗ Dispersión ALTA - Señal muy distorsionada")
    print("  La transmisión fallará sin compensación de dispersión.")

print("\n" + "="*60)
print("CONSEJOS PARA EXPERIMENTAR:")
print("="*60)
print("\n1. Para ver MÁS dispersión:")
print("   - Aumenta 'longitud_fibra_km' (ej: 100 km)")
print("   - Aumenta 'velocidad' (ej: 50e9 para 50 Gb/s)")
print("\n2. Para ver MENOS dispersión:")
print("   - Reduce 'longitud_fibra_km' (ej: 10 km)")
print("   - Reduce 'velocidad' (ej: 1e9 para 1 Gb/s)")
print("\n3. Para cambiar el tipo de fibra:")
print("   - Cambia 'dispersion' (ej: 4 para fibra NZDSF)")
print("="*60)

print("\n✓ Simulación completada. Mostrando gráficos...")
plt.show()
