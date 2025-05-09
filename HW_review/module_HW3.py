import numpy as np
import matplotlib.pyplot as plt



def create_double_source_image(size, centers, amplitudes, sigmas, noise_level=50):
    """
    Generate a simulated image with two Gaussian sources at given centers, amplitudes, and sigmas.
    The background should have Gaussian noise with mean 1000 and given noise_level.
    """


    # Initialize the background with Gaussian noise
    np.random.seed(42)
    background = np.random.normal(loc=1000, scale=noise_level, size=size)


    # Create a coordinate grid for the image
    y, x = np.indices(size)


    # Create the first source (Gaussian PSF)
    center_x1, center_y1 = centers[0]
    psf1 = amplitudes[0] * np.exp(-((x - center_x1)**2 + (y - center_y1)**2) / (2 * sigmas[0]**2))



    # Create the second source (Gaussian PSF)
    center_x2, center_y2 = centers[1]
    psf2 = amplitudes[1] * np.exp(-((x - center_x2)**2 + (y - center_y2)**2) / (2 * sigmas[1]**2))


     # Add both sources to the background
    image = background + psf1 + psf2
    
    return image



def create_double_source_image(size, centers, amplitudes, sigmas, noise_level=50):
    """
    Generate a simulated image with multiple Gaussian sources at given centers, amplitudes, and sigmas.
    The background should have Gaussian noise with mean 1000 and given noise_level.
    """
    # Create a coordinate grid for the image
    y, x = np.indices(size)
    
    # Initialize the background with Gaussian noise
    background = np.random.normal(loc=1000, scale=noise_level, size=size)
    
    # Loop over each source and add its Gaussian PSF to the image
    image = background
    for center, amplitude, sigma in zip(centers, amplitudes, sigmas):
        center_x, center_y = center
        psf = amplitude * np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2))
        image += psf
    
    return image





# Function to find the brightest pixel
def find_brightest_pixel(image):
    """Finds the brightest pixel in the image."""
    max_value = np.max(image)  # Find the maximum value in the image
    index_max_value = np.argmax(image)
    max_position = np.unravel_index(index_max_value, image.shape)  # Find the (x, y) coordinates of the max value
    return max_position, max_value


# Function to measure the flux within a circular aperture
def measure_flux(image, center, radius):
    """Measures the total flux inside a circular aperture around the center."""
    y, x = np.indices(image.shape)  # Create a grid of (y, x) coordinates
    cx, cy = center  # Get the center coordinates
    # Create a circular mask: True if the point is inside the circle
    mask = (x - cx)**2 + (y - cy)**2 <= radius**2 
    flux = np.sum(image[mask])  # Sum the pixel values inside the circle
    return flux




# Modified function to measure flux with background subtraction
def measure_flux_modified(image, center, radius):
    """Measures the total flux inside a circular aperture after background subtraction."""
    y, x = np.indices(image.shape)  # Create a grid of (y, x) coordinates
    cx, cy = center  # Get the center coordinates
    
    # Subtract the background (median value) from the image
    background = np.median(image)  # Median background level
    image_subtracted = image - background  # Subtract the background
    
    # Create a circular mask: True if the point is inside the circle
    mask = (x - cx)**2 + (y - cy)**2 <= radius**2
    
    # Measure the flux inside the aperture after background subtraction
    flux = np.sum(image_subtracted[mask])  # Sum the pixel values inside the circle
    return flux, background





def simulate_variable_star(time_span_days, period_days, amplitude, noise_std):
    """
    Simulate a light curve of a variable star as a sine wave plus Gaussian noise.
    Returns both noisy and noiseless flux.
    """
    # Generate 100 time observations evenly spaced over the time span
    time = np.linspace(0, time_span_days, 100)
    
    # Create the true (noiseless) flux using a sine wave
    without_noise_flux = 1 + amplitude * np.sin(2 * np.pi * time / period_days)
    
    # Add Gaussian noise to the true flux to simulate observed flux
    noise = np.random.normal(0, noise_std, size=time.shape)
    noisy_flux = without_noise_flux + noise
    
    return time, without_noise_flux, noisy_flux


