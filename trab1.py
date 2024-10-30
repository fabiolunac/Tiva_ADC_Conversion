import serial
import numpy as np
import matplotlib.pyplot as plt

# # Configurar a porta serial
porta_serial = serial.Serial('COM5', baudrate=115200, timeout=1)
N = 100
Fs = 500

def send_int_to_uart(serialobj: serial.Serial, value: int, num_bytes: int, byteorder: str) -> None:
    bytes_to_send = value.to_bytes(num_bytes, byteorder, signed=True)
    serialobj.write(bytes_to_send)


def read_int_vector(serialobj: serial.Serial, num_elements: int) -> np.ndarray:
    signal = []
    while len(signal) < num_elements:
        data = serialobj.read(4)

        if len(data) == 4:
            int_value = (data[0]) | (data[1] << 8) | (data[2] << 16) | (data[3] << 24)
            signal.append(int_value)

        else:
            print('Esperando dados')

    return signal

while True:
    try:
        x = input("Comandos: 1 - Iniciar Transferência | 0 - Não iniciar: ")

        if x == '0':
            send_int_to_uart(porta_serial, int(x), 4, 'little')
            print('Encerrando...\n')
            break

        elif x == '1':
            send_int_to_uart(porta_serial, int(x), 4, 'little')
            y = read_int_vector(porta_serial, N)

            Y = np.fft.fft(y)

            y_fft_magnitude = np.abs(Y)[:N // 2]  # Magnitude da FFT (apenas metade positiva)
            freqs = np.fft.fftfreq(N, 1 / Fs)[:N // 2]  # Frequências correspondentes

            plt.figure()
            plt.subplot(211)
            plt.plot(y)
            plt.grid()
            plt.title('Valores Recebidos')

            plt.subplot(212)
            plt.stem(freqs, y_fft_magnitude*2/N)
            plt.grid()
            plt.title("FFT")
            plt.xlabel("Frequência (Hz)")
            plt.ylabel("Magnitude")

            plt.tight_layout()
            plt.show()

        else:
            print('Comando inválido!\nDigite 1 para iniciar ou 0 para sair\n')

    except ValueError:
        print("Digite uma entrada correta")