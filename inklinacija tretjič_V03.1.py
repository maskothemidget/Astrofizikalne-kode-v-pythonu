import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from skimage.measure import regionprops, label
from skimage.filters import threshold_otsu

def find_ellipse_diameters(image, center, debug=False):
    print("Začetek funkcije 'find_ellipse_diameters'")
    y0, x0 = center
    print("Središče:", center)
    
    # Apply a threshold to create a binary image
    threshold_value = threshold_otsu(image)
    binary_image = image > threshold_value
    print("Ustvarjena binarna slika")
    
    # Label connected components
    labeled_image = label(binary_image)
    print("Označene povezane komponente")
    
    # Extract region properties
    props = regionprops(labeled_image)
    print("Izvlečene lastnosti regij")
    
    """
    if debug:
        # Debugging: visualize the binary image and labeled regions
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.title('Binary Image')
        plt.imshow(binary_image, cmap='gray')
        plt.scatter(x0, y0, color='red', label='Center')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.title('Labeled Regions')
        plt.imshow(labeled_image, cmap='nipy_spectral')
        plt.scatter(x0, y0, color='red', label='Center')
        plt.legend()
        plt.show()
    """

    # Find the region that contains the center
    for prop in props:
        if prop.bbox[0] <= y0 < prop.bbox[2] and prop.bbox[1] <= x0 < prop.bbox[3]:
            major_diameter = prop.major_axis_length
            minor_diameter = prop.minor_axis_length
            print("Najdena regija, ki vsebuje središče")
            return major_diameter, minor_diameter
    
    # If no region is found, return None
    print("Ni bilo mogoče najti regije z danim središčem")
    return 0, 0

def calculate_inclination(a, b):
    if b == 0:
        raise ValueError("Minor diameter cannot be zero.")
    print(f"Izračun naklona za a={a}, b={b}")
    cos_i = a / b
    inclination = np.arccos(b/a) * (180 / np.pi)  # Convert radians to degrees
    print(f"Naklon je {inclination:.2f} stopinj")
    return inclination

def process_fits_file(file_path, center, debug=False):
    print(f"Začetek obdelave FITS datoteke: {file_path}")
    try:
        with fits.open(file_path) as hdul:
            data = hdul[0].data
            if len(data.shape) != 2:
                raise ValueError("Image data is not 2D.")
            print("FITS datoteka uspešno odprta in prebrana")
            
            major_diameter, minor_diameter = find_ellipse_diameters(data, center, debug)
            if major_diameter == 0 or minor_diameter == 0:
                print("Ni bilo mogoče najti elipse z danim središčem.")
                return None
            
            inclination = calculate_inclination(major_diameter, minor_diameter)
            print("Obdelava končana")
            return inclination
    except Exception as e:
        print(f"Prišlo je do napake: {e}")
        return None

# Primer uporabe
file_path = 'D:\\fmf\\aop\\projekt\\kalibrirano\\master_calibration_m63_5s.fits'  # Zamenjaj s potjo do tvoje FITS datoteke
center = (1731, 869)  # Zamenjaj z znanim središčem galaksije
print("Začetek obdelave")
inclination = process_fits_file(file_path, center, debug=True)
if inclination is not None:
    print(f'Nagnjenost galaksije je {inclination:.2f} stopinj.')
else:
    print("Ni bilo mogoče izračunati nagnjenosti.")

print("Obdelava končana.")
