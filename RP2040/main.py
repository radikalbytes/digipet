import gc9a01
from machine import Pin, SPI
import time
import uos

# --- Pines ---
reset_pin = Pin(12, Pin.OUT)
cs_pin = Pin(9, Pin.OUT, value=1)   # aseguramos que CS arranca en HIGH
dc_pin = Pin(13, Pin.OUT)

# --- Reset manual de la pantalla ---
reset_pin.value(0)
time.sleep(0.1)
reset_pin.value(1)
time.sleep(0.1)

# --- Inicialización SPI lenta primero ---
spi = SPI(1, baudrate=20000000, sck=Pin(10), mosi=Pin(11))

# --- Inicialización del display ---
display = gc9a01.GC9A01(spi, 240, 240, reset=reset_pin, cs=cs_pin, dc=dc_pin)
display.init()
time.sleep(0.5)
display.init()
time.sleep(0.2)
display.rotation(0)

# Subimos velocidad SPI tras init
spi.init(baudrate=60000000)

# Pantalla en negro al inicio
display.fill(0)
time.sleep(0.1)

# --- Lista de frames ---
frames = sorted(f for f in uos.listdir("frames_bin") if f.endswith(".bin"))
frame_delay = 0.001

# --- Buffer para 1 fila (240 píxeles × 2 bytes = 480 bytes) ---
row_buffer = bytearray(240*2)

# --- Función para mostrar un frame .bin fila por fila ---
def show_bin_frame(display, filename):
    try:
        with open(filename, "rb") as f:
            for y in range(240):
                f.readinto(row_buffer)
                display.blit_buffer(row_buffer, 0, y, 240, 1)
    except OSError:
        print("Error cargando frame:", filename)

# --- Bucle principal con Ctrl+C seguro ---
try:
    while True:
        for f in frames:
            show_bin_frame(display, "frames_bin/" + f)
            time.sleep(frame_delay)
except KeyboardInterrupt:
    print("Animación detenida")
