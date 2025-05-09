from scipy.ndimage import gaussian_filter1d
import numpy as np
import matplotlib.pyplot as plt


g_constant = 6.67e-11

def generate_light_curve(period_days, amplitude=0.1, noise_level=0.0):
    """Generate a simple sinusoidal light curve with optional noise."""
    time = np.linspace(0, 5*period_days, 100)  # Observe for 5 periods (defining cadence of observation)
    flux = 1 + amplitude * np.sin(2 * np.pi * time / period_days)
    
    if noise_level > 0:
        noise = np.random.normal(0, noise_level, size=time.shape)
        flux += noise
        
    return time, flux


def smooth_light_curve(period_days, amplitude=0.1, noise_level=0.0, sigma=2):
    
    # Simulate a noisy light curve
    time, noisy_flux = generate_light_curve(period_days=1.0, amplitude=amplitude, noise_level=noise_level)
    
    """Smooth the light curve using a Gaussian filter."""
    return gaussian_filter1d(noisy_flux, sigma=sigma)