from astropy.io import fits
import numpy as np
import os

def fits_to_txt(input_fits, output_txt):
    # Odpri FITS datoteko
    with fits.open('D:\\fmf\\aop\\projekt\\kalibrirano\\master_calibration_m101_5s.fits') as hdul:
        # Privzeto predpostavimo, da so podatki v prvem razdelku (HDU)
        data = hdul[0].data
    
    # Preveri, ali so podatki naloženi pravilno
    if data is None:
        print("Podatki niso na voljo v prvem razdelku HDU.")
        return

    # Zapiši podatke v TXT datoteko
    np.savetxt(output_txt, data, fmt='%s')

# Primer uporabe
input_fits = 'D:\\fmf\\aop\\projekt\\kalibrirano\\master_calibration_m101_5s.fits'
output_dir = 'D:\\fmf\\aop\\projekt\\kalibrirano\\txt'  # Mapa, kamor želite shraniti TXT datoteko
output_txt = os.path.join(output_dir, 'm101_5s.txt')

# Ustvari mapo, če ne obstaja
os.makedirs(output_dir, exist_ok=True)

fits_to_txt(input_fits, output_txt)
