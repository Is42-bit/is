import matplotlib.pyplot as plt
import numpy as np

# Data
freq = [100, 150, 200, 500, 1000, 2000, 2500, 2700, 3000, 3500, 5000, 6000, 7000, 8000, 9000, 10000, 10500, 11000, 13000, 13500, 15000, 25000, 35000, 45000, 50000]
gain = [4.08, 4.09, 4.35, 4.8, 1.5, 1.5, 0.82, 0.82, 0.82, -2.0, -2.0, -2.0, -8.0, -8.0, -2.0, -2.0, -2.0, -2.0, 0.82, 1.58, 1.58, 4.08, 4.35, 4.35, 4.35]

# Plot
plt.semilogx(freq, gain, '-o', label='Gain (dB)')
plt.grid(True, which="both")
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain (dB)')
plt.title('Gain vs Frequency (Semilog) - 2nd Order Active Bandpass Filter')
plt.ylim(-10, 5)
plt.legend()
plt.savefig('semilog_graph_2025-08-18.png')
print("Plot saved as 'semilog_graph_2025-08-18.png'")