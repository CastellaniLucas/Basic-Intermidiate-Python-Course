import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
import time

# ----- CONFIGURACIÓN -----
max_size = 2000
update_block = 50
baud = 90000

ser = serial.Serial('COM3', baudrate=baud, timeout=1)

# bandera de ejecución
running = True

# ----- TKINTER -----
root = tk.Tk()
root.title("Osciloscopio en tiempo real")

fig, ax = plt.subplots(figsize=(8,6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# botón de salida
def stop():
    global running
    running = False
    try:
        ser.close()
    except:
        pass
    root.quit()
    root.destroy()

btn = tk.Button(root, text="Salir", command=stop, font=("Arial", 14))
btn.pack(pady=10)

# buffers preasignados
data = [0]*max_size
times = [0]*max_size
count = 0
filled = False
update_count = 0

line, = ax.plot(range(max_size), data)
ax.set_ylim(0, 5.5)

t0 = time.time()

def update():
    global count, filled, update_count, running

    if not running:
        return  # detiene el loop correctamente

    if ser.in_waiting >= 2:
        raw = ser.read(2)
        value = raw[0] | (raw[1] << 8)
        value = value * 5.0/1023.0
        t = time.time() - t0

        if not filled:
            data[count] = value
            times[count] = t
            count += 1

            if count == max_size:
                filled = True
                count = max_size - update_block
        else:
            if count == max_size:
                data[:max_size-update_block] = data[update_block:]
                times[:max_size-update_block] = times[update_block:]
                count = max_size - update_block

            data[count] = value
            times[count] = t
            count += 1

        update_count += 1

        if update_count >= update_block and filled:
            update_count = 0
            line.set_ydata(data)
            canvas.draw_idle()

    root.after(1, update)

root.after(1, update)
root.mainloop()
