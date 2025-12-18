import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.ticker import MultipleLocator
import tkinter as tk
import numpy as np
import time



################################################################
# Configuracion de buffers, puerto serie y velocidad, muestreo ADC
max_size = 5000  # tamaño maximo de ventana de visualizacion
update_block = 50  # cantidad de muestras leidas por actualizacion
baud = 90000 # velocidad de comunicacion serial
fs = 61      # frecuencia de muestreo ADC
Ts = 1.0/fs  # periodo de muestreo ADC
ser = serial.Serial('COM3', baudrate=baud, timeout=1)
################################################################



################################################################
# Flags utiles para control de ejecucion
iniciar_tkinter = True  # Para detener la GUI 
run_stop = True         # Para pausar/reanudar visualización de datos
################################################################




################################################################
#definicion de ventanas de tiempo, tiempo/division
time_divs = [
    0.01,   # 10 ms/div
    0.02,   # 20 ms/div
    0.05,   # 50 ms/div
    0.1,    # 100 ms/div
    0.2,    # 200 ms/div
    0.5,    # 500 ms/div
    1.0,    # 1 s/div
    2.0,    # 2 s/div
    5.0,    # 5 s/div
]
time_div_index = 5  # indice para seleccionar tiempo/division
# funcion para obtener ventana de tiempo 
def get_time_window():
    return time_divs[time_div_index] * 10 # 10 divisiones en pantalla
################################################################



################################################################
# Creacion del objeto tkinter principal, mi osciloscopio
root = tk.Tk()
root.title("Osciloscopio en tiempo real")
main = tk.Frame(root)
main.pack(fill=tk.BOTH, expand=True)
#separo el frame de graficacion y el de mediciones
plot_frame = tk.Frame(main)  #ploteo
plot_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
meas_frame = tk.Frame(main, width=200) #mediciones
meas_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
# Creo la figura y el eje de matplotlib
fig, ay = plt.subplots(figsize=(8,6))
################################################################



################################################################
# Creo canvas y luego el toolbar de matplotlib + barra de control (run/stop, time/div, salir)
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
toolbar = NavigationToolbar2Tk(canvas, plot_frame)
toolbar.update()
toolbar.pack(side=tk.TOP, anchor='center')
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
#creo barra de mediciones lateral
tk.Label(
    meas_frame,
    text="MEDICIONES",
    font=("Arial", 12, "bold")
).pack(pady=(5,10))
Vactual_var = tk.StringVar(value="Vactual: --")
Vmax_var = tk.StringVar(value="Vmax: --")
Vmin_var = tk.StringVar(value="Vmin: --")
vpp_var  = tk.StringVar(value="Vpp:  --")
vrms_var = tk.StringVar(value="Vrms: --")
tk.Label(meas_frame, textvariable=Vactual_var, font=("Consolas", 18)).pack(anchor="w", pady=2)
tk.Label(meas_frame, textvariable=Vmax_var, font=("Consolas", 18)).pack(anchor="w", pady=2)
tk.Label(meas_frame, textvariable=Vmin_var, font=("Consolas", 18)).pack(anchor="w", pady=2)
tk.Label(meas_frame, textvariable=vpp_var, font=("Consolas", 18)).pack(anchor="w", pady=2)
tk.Label(meas_frame, textvariable=vrms_var, font=("Consolas", 18)).pack(anchor="w", pady=2)
# barra de controles inferior
ctrl = tk.Frame(root)
ctrl.pack(pady=5)
# barra para visualizar y ajustar time/div
time_ctrl = tk.Frame(ctrl)
time_ctrl.pack(side=tk.LEFT, padx=10)
################################################################


################################################################
# botones para funcionalidades adicionales
def stop():    #frena ejecucion de tkinter    
    global iniciar_tkinter
    iniciar_tkinter = False
    try:
        ser.close()
    except:
        pass
    root.quit()
    root.destroy()
def pot(val):   #ajusta time/div
    global time_div_index
    time_div_index = int(float(val))
    update_time_scale()
    update_time_label()
def run_sstop():  #pausa/reanuda visualización de datos
    global run_stop
    run_stop = not run_stop
    run_btn.config(text="RUN" if not run_stop else "PAUSE")
################################################################


################################################################
# Configuracion del potenciometro para time/div y botones de control
time_scale = tk.Scale(
    time_ctrl,
    from_=0,
    to=len(time_divs)-1,
    orient=tk.HORIZONTAL,
    showvalue=False,
    command=pot,
    label="Time / div"
)
time_scale.pack(side=tk.LEFT, padx=10)
run_btn = tk.Button(ctrl, text="PAUSE", command=run_sstop)
run_btn.pack(side=tk.LEFT, padx=5)
tk.Button(ctrl, text="Salir", command=stop).pack(side=tk.LEFT, padx=20)
timebase_var = tk.StringVar()
timebase_label = tk.Label(
    time_ctrl,
    textvariable=timebase_var,
    font=("Consolas", 10, "bold")
)
timebase_label.pack(side=tk.LEFT, padx=10)
################################################################


################################################################
# buffers para almacenamiento de datos y tiempos
buffer = np.zeros(50000)   # buffer grande de historia / no se utiliza para graficar
index = 0
################################################################

################################################################
# Funcion para ajustar eje temporal segun ventana de tiempo
def make_time_axis(N):
    T = get_time_window()
    return np.linspace(-T/2, T/2, N)
# Configuracion inicial del grafico
N0 = int(fs * get_time_window())
N0 = min(N0, max_size)
time_axis = make_time_axis(N0)
display = np.zeros(N0)
line, = ay.plot(time_axis, display)
ay.set_xlim(time_axis[0], time_axis[-1])  # limites iniciales del eje x
ay.set_ylim(0, 5.5) #Fijar limites del eje y, arduino no mide mas alla de 5V ni menos de 0V
ay.set_xlim(time_axis[0], time_axis[-1])  # limites iniciales del eje x
ay.set_xlabel("Tiempo [s]")
ay.set_ylabel("Voltaje [V]")
ay.grid(True)
################################################################



################################################################
# Funciones utiles para actualizar time/div, eje temporal, y mediciones
def update_time_label():            #actualiza etiqueta de time/div
    t = time_divs[time_div_index]
    if t < 1:
        timebase_var.set(f"{t*1000:.0f} ms/div")
    else:
        timebase_var.set(f"{t:.0f} s/div")
def update_time_scale():            #actualiza eje temporal segun time/div
    global display, time_axis
    T = get_time_window()
    time_div = time_divs[time_div_index]
    N = int(fs * T)
    N = min(N, max_size)
    display = np.zeros(N)
    time_axis = np.linspace(-T/2, T/2, N)
    line.set_xdata(time_axis)
    line.set_ydata(display)
    ay.set_xlim(-T/2, T/2)
    ay.xaxis.set_major_locator(MultipleLocator(time_div))     #aca se actualizan los ticks mayores y menores, fijo grilla
    ay.xaxis.set_minor_locator(MultipleLocator(time_div / 5))
    canvas.draw_idle()
def measurements(sig, fs):  #calcula y actualiza mediciones
    if sig is None or len(sig) < 10:
        return

    vpp = sig.max() - sig.min()
    vrms = np.sqrt(np.mean(sig**2))
    Vmax = sig.max()
    Vmin = sig.min()
    Vact = sig[-1]

    Vactual_var.set(value=f"Vact: {Vact:6.3f} V")
    Vmax_var.set(f"Vmax: {Vmax:6.3f} V")
    Vmin_var.set(f"Vmin: {Vmin:6.3f} V")
    vpp_var.set(f"Vpp:  {vpp:6.3f} V")
    vrms_var.set(f"Vrms: {vrms:6.3f} V")

def update():                      #funcion principal de actualizacion de datos y grafico
    global buffer, index, display, iniciar_tkinter

    if not iniciar_tkinter:  #salgo del loop de tkinter
        return

    while ser.in_waiting >= 2: #lee datos del puerto serie si hay al menos 2 bytes disponibles
        raw = ser.read(2)
        value = raw[0] | (raw[1] << 8)
        value = value * 5.0 / 1023.0

        buffer[index % buffer.size] = value    #elimina jitter visual, el indice crece indefinidamente, pero se reajusta el buffer_size
        index += 1

    N = len(display)          #cantidad de muestras a mostrar en pantalla
    if run_stop and (index >= N):  #actualiza grafico solo si no esta en pausa y hay suficientes datos
        idxs = (np.arange(index - N, index)) % buffer.size  #indices circulares para obtener las ultimas N muestras
        display[:] = buffer[idxs]  #actualiza datos a mostrar segun los indices obtenidos

    line.set_ydata(display)        #actualiza datos del grafico
    canvas.draw_idle()
    measurements(display, fs)      #actualiza mediciones


    root.after(1, update)
################################################################


################################################################
# Inicializacion de time/div
time_scale.set(time_div_index)
update_time_scale()
update_time_label()

# Comienzo del loop principal de tkinter
root.after(1, update)
root.mainloop()
################################################################