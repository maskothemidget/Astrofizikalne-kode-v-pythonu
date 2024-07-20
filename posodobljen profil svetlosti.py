import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# Odpri FITS datoteko
fits_image_filename = 'D:\\fmf\\aop\\projekt\\kalibrirano\\master_calibration_m51_5s.fits'
hdul = fits.open(fits_image_filename)
image_data = hdul[0].data
hdul.close()

# Podatki o središču galaksije (x in y koordinate)
center_x = 1306  # zamenjajte s svojo vrednostjo
center_y = 1733  # zamenjajte s svojo vrednostjo

# Definiraj funkcijo za izračun radialnega profila
def radial_profile(data, center_x, center_y):
    y, x = np.indices((data.shape))
    r = np.sqrt((x - center_x)**2 + (y - center_y)**2)
    r = r.astype(int)  # Popravljeno: uporabite vgrajeni 'int'

    # Ustvarjanje binov in povprečenje svetlosti v vsakem binu
    try:
        tbin = np.bincount(r.ravel(), data.ravel())
        nr = np.bincount(r.ravel())
        radialprofile = tbin / nr
    except Exception as e:
        print("Prišlo je do napake pri izračunu radialnega profila:", e)
        radialprofile = None

    return radialprofile

# Izračun radialnega profila
try:
    radial_prof = radial_profile(image_data, center_x, center_y)
    if radial_prof is not None:
        # Risanje radialnega profila
        plt.figure()
        plt.plot(radial_prof, label='Radialni profil')
        plt.xlabel('Razdalja od središča (piksli)')
        plt.ylabel('Povprečna svetlost')
        plt.title('Radialni profil svetlosti galaksije')
        plt.legend()
        plt.grid(True)
        plt.show()
    else:
        print("Radialni profil ni bil uspešno izračunan.")
except Exception as e:
    print("Prišlo je do napake pri glavnem izračunu:", e)
