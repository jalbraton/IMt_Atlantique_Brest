
"""
BE1 - Ejercicio 4: Simulación de Propagación en Fibra Óptica
Simulación de dispersión cromática en fibra óptica monomodo

Autor: Estudiante IMT Atlantique
Fecha: Enero 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fftfreq, fftshift

# =============================================================================
# PARÁMETROS CONFIGURABLES DEL SIMULADOR
# =============================================================================

# Parámetros de la señal
n_bits = 1000           # Número de bits a transmitir (reducido para visualización)
B = 10e9                # Debit (bit-rate) en bit/s - CAMBIAR SEGÚN CASO: 1e9, 10e9, 50e9, 200e9
Ns = 32                 # Número de muestras por bit (32 según enunciado)

# Parámetros de la fibra óptica
lambda_c = 1550e-9      # Longitud de onda de la portadora óptica (1550 nm)
D_coeff = 17e-12        # Coeficiente de dispersión cromática para G.652 [s/(m²)] = 17 ps/(nm·km)
L_fiber = 50e3          # Longitud de la fibra en metros (50 km) - AJUSTAR SEGÚN CASO

# Constantes físicas
c = 3e8                 # Velocidad de la luz en el vacío [m/s]

# Parámetros calculados automáticamente
T_bit = 1/B             # Duración de un bit [s]
Fs = Ns * B             # Frecuencia de muestreo [Hz]
Ts = 1/Fs               # Período de muestreo [s]

# =============================================================================
# a) GENERACIÓN DE SECUENCIA BINARIA PSEUDO-ALEATORIA
# =============================================================================

def generar_secuencia_binaria(n_bits):
    """
    Genera una secuencia binaria pseudo-aleatoria de 0s y 1s.
    
    Parámetros:
        n_bits (int): Número de bits a generar
    
    Retorna:
        numpy.array: Secuencia de n_bits valores (0 o 1)
    
    Ejemplo:
        >>> seq = generar_secuencia_binaria(10)
        >>> print(seq)  # [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
    """
    # np.random.randint genera números enteros aleatorios
    # randint(0, 2, size) genera números entre 0 (incluido) y 2 (excluido)
    # es decir, solo 0 o 1
    secuencia = np.random.randint(0, 2, size=n_bits)
        
    return secuencia

# =============================================================================
# b) MODULACIÓN NRZ (Non-Return-to-Zero) Y MUESTREO
# =============================================================================

def modular_NRZ(secuencia_bits, Ns):
    """
    Modula la secuencia binaria en formato NRZ con amplitud entre +1V y +2V.
    
    El formato NRZ mantiene el nivel de voltaje durante todo el período del bit:
    - Bit 0 → +1 Volt (nivel bajo con DC offset)
    - Bit 1 → +2 Volts (nivel alto)
    
    Parámetros:
        secuencia_bits (array): Secuencia de bits (0s y 1s)
        Ns (int): Número de muestras por bit
    
    Retorna:
        numpy.array: Señal NRZ muestreada
        numpy.array: Vector de tiempo correspondiente
    
    Explicación del DC offset:
        El componente DC (+1V base) simula la transmisión con láser directamente 
        modulado, donde la potencia óptica nunca es exactamente cero (siempre hay
        una emisión mínima del láser).
    """
    n_bits = len(secuencia_bits)
    n_samples = n_bits * Ns  # Total de muestras en la señal
    
    # Crear señal NRZ: cada bit se repite Ns veces
    # np.repeat repite cada elemento del array
    # Ejemplo: [0, 1, 1] con Ns=3 → [0,0,0, 1,1,1, 1,1,1]
    signal_NRZ = np.repeat(secuencia_bits, Ns)
    
    # Añadir componente DC: convertir de [0,1] a [1,2] Volts
    # Bit 0 → 0+1 = 1V
    # Bit 1 → 1+1 = 2V
    signal_NRZ = signal_NRZ + 1
    
    # Crear vector de tiempo
    # np.arange crea un array de 0 a n_samples
    # Multiplicamos por Ts para convertir a segundos
    tiempo = np.arange(n_samples) * Ts
    # [0, 1, 2, 3, 4] * 0.001
    # [0, 0.001, 0.002, 0.003, 0.004]
    return signal_NRZ, tiempo

def calcular_espectro(signal, Fs):
    """
    Calcula el espectro de frecuencias de la señal usando FFT.
    
    La FFT (Fast Fourier Transform) convierte la señal del dominio del tiempo
    al dominio de la frecuencia, mostrando qué frecuencias componen la señal.
    
    Parámetros:
        signal (array): Señal en el tiempo
        Fs (float): Frecuencia de muestreo [Hz]
    
    Retorna:
        freqs (array): Vector de frecuencias [Hz]
        spectrum (array): Magnitud del espectro (valor absoluto de FFT)
    """
    # Número de muestras
    N = len(signal)
    
    # Calcular FFT (Transformada Rápida de Fourier)
    # fft() convierte del dominio tiempo → dominio frecuencia
    fft_signal = fft(signal)
    
    # Calcular magnitud del espectro (valor absoluto de números complejos)
    # Normalizamos dividiendo por N para tener amplitudes correctas
    spectrum = np.abs(fft_signal) / N
    
    # Generar vector de frecuencias correspondiente
    # fftfreq genera las frecuencias asociadas a cada componente FFT
    freqs = fftfreq(N, d=1/Fs)
    
    # Usar fftshift para centrar el espectro en 0 Hz
    # (pone frecuencias negativas a la izquierda, positivas a la derecha)
    freqs = fftshift(freqs)
    spectrum = fftshift(spectrum)
    
    return freqs, spectrum

# =============================================================================
# c) PROPAGACIÓN EN FIBRA: RESOLVER ECUACIÓN DE SCHRÖDINGER
# =============================================================================

def calcular_beta2(D_coeff, lambda_c, c):
    """
    Calcula el parámetro β₂ (dispersión de velocidad de grupo - GVD).
    
    Relación entre D (dispersión cromática) y β₂:
        β₂ = -(D × λ²) / (2πc)
    
    Parámetros:
        D_coeff: Coeficiente de dispersión [s/m²]
        lambda_c: Longitud de onda [m]
        c: Velocidad de la luz [m/s]
    
    Retorna:
        beta2: Parámetro β₂ [s²/m]
    
    Interpretación física:
        β₂ > 0: Dispersión anómala (frecuencias altas viajan más rápido)
        β₂ < 0: Dispersión normal (frecuencias bajas viajan más rápido)
        
        Para G.652 @ 1550nm: D ≈ 17 ps/(nm·km) → β₂ < 0 (normal)
    """
    beta2 = -(D_coeff * lambda_c**2) / (2 * np.pi * c)

    
    return beta2

def propagar_en_fibra(signal_entrada, L, beta2, Fs):
    """
    Simula la propagación de la señal en fibra óptica con dispersión cromática.
    
    Resuelve la ecuación diferencial de Schrödinger no lineal (solo parte lineal):
        ∂A/∂z = -(iβ₂/2) × ∂²A/∂t²
    
    MÉTODO DE RESOLUCIÓN - Split-Step Fourier Method (simplificado):
    
    1. Transformar señal al dominio de frecuencias (FFT)
    2. Aplicar operador de dispersión en frecuencia (más simple matemáticamente)
    3. Transformar de vuelta al dominio del tiempo (IFFT)
    
    ¿Por qué en frecuencia?
        En tiempo: ∂²A/∂t² es una derivada (complicado numéricamente)
        En frecuencia: ∂²A/∂t² → multiplicación por -(iω)² (¡mucho más simple!)
    
    Parámetros:
        signal_entrada (array): Señal a la entrada de la fibra
        L (float): Longitud de la fibra [m]
        beta2 (float): Parámetro de dispersión [s²/m]
        Fs (float): Frecuencia de muestreo [Hz]
    
    Retorna:
        signal_salida (array): Señal a la salida de la fibra
    """
    # Número de muestras
    N = len(signal_entrada)
    
    # 1. TRANSFORMADA DE FOURIER: tiempo → frecuencia
    # Convertimos la señal al dominio de frecuencias
    A_freq = fft(signal_entrada)
    
    # 2. VECTOR DE FRECUENCIAS ANGULARES
    # ω = 2πf (frecuencia angular en rad/s)
    freqs = fftfreq(N, d=1/Fs)  # Frecuencias [Hz]
    omega = 2 * np.pi * freqs    # Frecuencias angulares [rad/s]
    
    # 3. OPERADOR DE DISPERSIÓN EN FRECUENCIA
    # La ecuación ∂A/∂z = -(iβ₂/2) × ∂²A/∂t² en frecuencia se convierte en:
    # A(z,ω) = A(0,ω) × exp(i × β₂/2 × ω² × z)
    #
    # Explicación:
    #   - En frecuencia, la derivada ∂²/∂t² se convierte en multiplicar por (iω)²
    #   - La solución es una exponencial que depende de ω² (por eso frecuencias
    #     diferentes viajan a velocidades diferentes → dispersión)
    dispersion_operator = np.exp(1j * (beta2 / 2) * omega**2 * L)
    
    # 4. APLICAR DISPERSIÓN
    # Multiplicamos cada componente de frecuencia por el operador de dispersión
    A_freq_propagada = A_freq * dispersion_operator
    
    # 5. TRANSFORMADA INVERSA: frecuencia → tiempo
    # Volvemos al dominio del tiempo para tener la señal de salida
    signal_salida = ifft(A_freq_propagada)
    
    # ifft puede devolver números complejos con parte imaginaria residual pequeña
    # Tomamos solo la parte real (la imaginaria es ruido numérico)
    signal_salida = np.real(signal_salida)
    
    
    return signal_salida

# =============================================================================
# d) DETECCIÓN CON FOTODIODO Y DC-BLOCK
# =============================================================================

def detectar_con_fotodiodo(signal_optica):
    """
    Simula la detección con fotodiodo (detector cuadrático).
    
    Un fotodiodo es un detector de ley cuadrada: la fotocorriente es proporcional
    a la potencia óptica, que a su vez es proporcional al cuadrado de la amplitud
    del campo eléctrico.
    
    I_fotodiodo ∝ |A(t)|²
    
    Parámetros:
        signal_optica (array): Amplitud de la señal óptica
    
    Retorna:
        fotocorriente (array): Corriente del fotodiodo [unidades arbitrarias]
    """
    # Detección cuadrática: elevar al cuadrado
    fotocorriente = signal_optica**2
    
    return fotocorriente

def aplicar_DC_block(signal):
    """
    Elimina la componente continua (DC) de la señal.
    
    Un DC-block es un filtro paso-alto que elimina la frecuencia 0 Hz (componente
    continua), dejando pasar solo las variaciones temporales (AC).
    
    Implementación simple: restar la media de la señal
    
    Parámetros:
        signal (array): Señal con componente DC
    
    Retorna:
        signal_AC (array): Señal sin componente DC (solo AC)
    """
    # Calcular el valor medio (componente DC)
    DC_component = np.mean(signal)
    
    # Restar la componente DC
    signal_AC = signal - DC_component
    
    return signal_AC

# =============================================================================
# FUNCIONES DE VISUALIZACIÓN
# =============================================================================

def graficar_senal_tiempo(tiempo, signal, titulo, n_bits_mostrar=50):
    """
    Grafica la señal en el dominio del tiempo.
    
    Parámetros:
        tiempo (array): Vector de tiempo [s]
        signal (array): Señal a graficar
        titulo (str): Título del gráfico
        n_bits_mostrar (int): Número de bits a mostrar (para no saturar el gráfico)
    """
    # Calcular cuántas muestras corresponden a n_bits_mostrar
    muestras_mostrar = n_bits_mostrar * Ns
    
    plt.figure(figsize=(12, 4))
    plt.plot(tiempo[:muestras_mostrar] * 1e9, signal[:muestras_mostrar], linewidth=1)
    plt.xlabel('Tiempo [ns]')
    plt.ylabel('Amplitud [V]')
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
def graficar_espectro(freqs, spectrum, titulo):
    """
    Grafica el espectro de frecuencias de la señal.
    
    Parámetros:
        freqs (array): Vector de frecuencias [Hz]
        spectrum (array): Magnitud del espectro
        titulo (str): Título del gráfico
    """
    plt.figure(figsize=(12, 4))
    # Graficamos en escala logarítmica (dB) para ver mejor los detalles
    # 20*log10 convierte a decibelios
    spectrum_dB = 20 * np.log10(spectrum + 1e-12)  # +1e-12 para evitar log(0)
    plt.plot(freqs / 1e9, spectrum_dB, linewidth=1)  # Frecuencias en GHz
    plt.xlabel('Frecuencia [GHz]')
    plt.ylabel('Magnitud [dB]')
    plt.title(titulo)
    plt.grid(True, alpha=0.3)
    plt.xlim([-3*B/1e9, 3*B/1e9])  # Mostrar ±3 veces el bit-rate
    plt.tight_layout()

def graficar_comparacion(tiempo, signal_in, signal_out, n_bits_mostrar=50):
    """
    Grafica comparación entrada vs salida de la fibra.
    """
    muestras_mostrar = n_bits_mostrar * Ns
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))
    
    # Señal de entrada
    ax1.plot(tiempo[:muestras_mostrar] * 1e9, signal_in[:muestras_mostrar], 'b-', linewidth=1)
    ax1.set_ylabel('Amplitud [V]')
    ax1.set_title('Señal a la ENTRADA de la fibra')
    ax1.grid(True, alpha=0.3)
    
    # Señal de salida
    ax2.plot(tiempo[:muestras_mostrar] * 1e9, signal_out[:muestras_mostrar], 'r-', linewidth=1)
    ax2.set_xlabel('Tiempo [ns]')
    ax2.set_ylabel('Amplitud [V]')
    ax2.set_title('Señal a la SALIDA de la fibra (después de dispersión)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()

# =============================================================================
# FUNCIÓN PRINCIPAL: EJECUTAR SIMULACIÓN COMPLETA
# =============================================================================

def ejecutar_simulacion():
    """
    Ejecuta la simulación completa del ejercicio 4.
    """
    print("="*70)
    print(" SIMULACIÓN DE PROPAGACIÓN EN FIBRA ÓPTICA - Ejercicio 4")
    print("="*70)
    print(f"\nParámetros de simulación:")
    print(f"  • Bit-rate: {B/1e9:.1f} Gb/s")
    print(f"  • Longitud de fibra: {L_fiber/1000:.1f} km")
    print(f"  • Longitud de onda: {lambda_c*1e9:.0f} nm")
    print(f"  • Dispersión cromática: {D_coeff*1e12:.1f} ps/(nm·km)")
    print(f"  • Número de bits: {n_bits}")
    print(f"  • Muestras por bit: {Ns}")
    print()
    
    # a) Generar secuencia binaria
    print("\n[PASO 1] Generación de secuencia binaria")
    print("-" * 70)
    bits = generar_secuencia_binaria(n_bits)
    
    # b) Modular en NRZ
    print("\n[PASO 2] Modulación NRZ")
    print("-" * 70)
    signal_NRZ, tiempo = modular_NRZ(bits, Ns)
    
    # Calcular y graficar espectro de entrada
    freqs_in, spectrum_in = calcular_espectro(signal_NRZ, Fs)
    
    # c) Propagar en fibra
    print("\n[PASO 3] Propagación en fibra óptica")
    print("-" * 70)
    beta2 = calcular_beta2(D_coeff, lambda_c, c)
    signal_fibra = propagar_en_fibra(signal_NRZ, L_fiber, beta2, Fs)
    
    # d) Detección y DC-block
    print("\n[PASO 4] Detección con fotodiodo y DC-block")
    print("-" * 70)
    fotocorriente = detectar_con_fotodiodo(signal_fibra)
    corriente_AC = aplicar_DC_block(fotocorriente)
    
    # Calcular espectro de salida
    freqs_out, spectrum_out = calcular_espectro(corriente_AC, Fs)
    
    # VISUALIZACIÓN
    print("\n[PASO 5] Generación de gráficos")
    print("-" * 70)
    
    # Gráfico 1: Señal NRZ entrada
    graficar_senal_tiempo(tiempo, signal_NRZ, 
                          f'Señal NRZ a la entrada ({B/1e9:.0f} Gb/s)')
    
    # Gráfico 2: Espectro entrada
    graficar_espectro(freqs_in, spectrum_in, 
                      f'Espectro de la señal de entrada ({B/1e9:.0f} Gb/s)')
    
    # Gráfico 3: Comparación entrada/salida
    graficar_comparacion(tiempo, signal_NRZ, signal_fibra)
    
    # Gráfico 4: Corriente detectada (con DC-block)
    graficar_senal_tiempo(tiempo, corriente_AC, 
                          f'Corriente detectada después de DC-block ({L_fiber/1000:.0f} km)')
    
    # Gráfico 5: Espectro salida
    graficar_espectro(freqs_out, spectrum_out, 
                      f'Espectro de corriente detectada ({L_fiber/1000:.0f} km)')
    
    print("\n✓ Simulación completada. Mostrando gráficos...")
    plt.show()
    
    print("\n" + "="*70)
    print(" FIN DE LA SIMULACIÓN")
    print("="*70)
    print("\nNOTA: Para probar diferentes bit-rates (ejercicio e), modifica:")
    print("      B = 1e9   # para 1 Gb/s")
    print("      B = 10e9  # para 10 Gb/s")
    print("      B = 50e9  # para 50 Gb/s")
    print("      B = 200e9 # para 200 Gb/s")
    print("\n      Y ajusta L_fiber según el caso de estudio.")

# =============================================================================
# EJECUCIÓN DEL PROGRAMA
# =============================================================================

if __name__ == "__main__":
    # Ejecutar la simulación
    ejecutar_simulacion()

