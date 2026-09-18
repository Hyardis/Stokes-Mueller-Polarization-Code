"""
Access to the refractiveindex.info database

This module contains a function accessing the RefractiveIndex database.
The function is separated from other modules of this package becasue 
the database import is computationally demanding. 
"""

from refractiveindex import RefractiveIndexMaterial
from .core import eV2nm
import numpy as np


def get_n(material, E_eV, source = "auto", cite = True):
    """
    Returns complex refractive index of the matrial at the specified 
    light beam energy.

    Utilizes the public refractiveindex.info database 
    of optical constants. Current implementation focuses 
    at metals commonly used in EUV reflective optics. 

    Parameters
    ----------
    material : str
        Chemical symbol of the optical medium (e.g., 'Au').
    E_eV : float
        Light energy in electronvolts.
    source : str, optional
        Preffered data source. When set to 'auto', it chooses 
        the best appropriate source for the current material 
        and energy combination. Default is 'auto'.
    cite : bool, optional
        Print the source of the provided refractive index. 
        Default is True. 

    Notes
    -----
    Database website :
        https://refractiveindex.info/
    It is recommended to choose the optical constants source manually 
    to ensure that the most appropriate experimental data were used. 
    When choosing the source, the determining factor should be the 
    energy range (as speciifed on the database website).
    The automatic source selector preference is set for the most recent
    publications with the widest spectral range. However, when requesting 
    data for a spectral range that cannot be covered by a single source,
    multiple sources may be automatically used, in which case consistency 
    and data continuity cannot be guaranteed. 
    """

    wavelength_nm = eV2nm(E_eV)
    wavelength_um = wavelength_nm/1000
    
    def out_of_range():
        raise ValueError(f"Experimental data for {material} at the wavelength of {wavelength_nm} nm are not available in the refractiveindex.info database.")

    if source == "auto":
        # np.all tests whether all array elements evaluate to True (can handle wavelength both as a single number and an array)
        match material:
            case "Be":
                if np.all((4.95937E-03 <= wavelength_um) & (wavelength_um <= 6.07766E-02)):
                    author = "Svechnikov"
                else:
                    out_of_range()
            
            case "diamond":
                if np.all((0.035424054 <= wavelength_um) & (wavelength_um <= 10.0)):
                    material = "C"
                    author = "Phillip"
                else:
                    out_of_range()
            
            case "Al":
                if np.all((1.2399E-04 <= wavelength_um) & (wavelength_um <= 2.0000E+02)):
                    author = "Rakic"
                elif np.all((1.033E-05 <= wavelength_um) & (wavelength_um <= 1.240E+03)):
                    author = "Hagemann"
                else:
                    out_of_range()
            
            case "Ni":
                if np.all((0.188 <= wavelength_um) & (wavelength_um <= 1.937)):
                    author = "Johnson"
                elif np.all((0.667 <= wavelength_um) & (wavelength_um <= 286)):
                    author = "Ordal"
                elif np.all((0.017586 <= wavelength_um) & (wavelength_um <= 2.479684)):
                    author = "Werner"
                else:
                    out_of_range()
            
            case "Ag":
                if np.all((0.1879 <= wavelength_um) & (wavelength_um <= 1.9370)):
                    author = "Johnson"
                elif np.all((0.017586 <= wavelength_um) & (wavelength_um <= 2.479684)):
                    author = "Werner"
                elif np.all(( 2.480E-06 <= wavelength_um) & (wavelength_um <= 2.480E+02)):
                    author = "Hagemann"
                else:
                    out_of_range()

            case "Cr":
                if np.all((0.188 <= wavelength_um) & (wavelength_um <= 1.937)):
                    author = "Johnson"

            case "Au":
                if np.all((3.542E-03 <= wavelength_um) & (wavelength_um <= 8.266E-01)):
                    author = "Hagemann-2"
                elif np.all((0.017586 <= wavelength_um) & (wavelength_um <= 2.479684)):
                    author = "Werner"
                elif np.all((8.266E-06 <= wavelength_um) & (wavelength_um <= 2.480E+02)):
                    author = "Hagemann"
                else:
                    out_of_range()
            
            case "Mo":
                if np.all((0.017586 <= wavelength_um) & (wavelength_um <= 2.479684)):
                    author = "Werner"
                elif np.all((0.2063 <= wavelength_um) & (wavelength_um <= 166.6667)):
                    author = "Querry"
                elif np.all((0.00236 <= wavelength_um) & (wavelength_um <= 0.12157)):
                    author = "Windt"
                else:
                    out_of_range()
                
            case "Rh":
                if np.all((0.2000 <= wavelength_um) & (wavelength_um <= 12.40)):
                    author = "Weaver"
                if np.all((0.00236 <= wavelength_um) & (wavelength_um <= 0.12157)):
                    author = "Windt"
                else:
                    out_of_range()

            case "Ru":
                if np.all((0.00236 <= wavelength_um) & (wavelength_um <= 0.12157)):
                    # only one source available in the database
                    author = "Windt"
                else:
                    out_of_range()

            case "Pd":
                if np.all((0.017586 <= wavelength_um) & (wavelength_um <= 2.479684)):
                    author = "Werner"
                elif np.all((0.00236 <= wavelength_um) & (wavelength_um <= 0.12157)):
                    author = "Windt"
                else:
                    out_of_range()

            case "Pt":
                if np.all((0.017586 <= wavelength_um) & (wavelength_um <= 2.479684)):
                    author = "Werner"
                elif np.all((0.190000 <= wavelength_um) & (wavelength_um <= 3.500000)):
                    author = "Tselin"
                elif np.all((0.00236 <= wavelength_um) & (wavelength_um <= 0.12157)):
                    author = "Windt"
                else:
                    out_of_range()

            case "W":
                if np.all((0.017586 <= wavelength_um) & (wavelength_um <= 2.479684)):
                    author = "Werner"
                if np.all((4.429E-02 <= wavelength_um) & (wavelength_um <= 4.110)):
                    author = "Weaver"
                if np.all((0.667 <= wavelength_um) & (wavelength_um <= 200)):
                    author = "Ordal"
                elif np.all((0.00236 <= wavelength_um) & (wavelength_um <= 0.12157)):
                    author = "Windt"
                else:
                    out_of_range()
    else:
        # override the automatic author selection if necessary
        author = source
        if material == "diamond":
            material = "C"

    # database returns an object
    data = RefractiveIndexMaterial(shelf = "main", book = material, page = author)

    # real part of rf. index @ wavelength
    n_real = data.get_refractive_index(wavelength_nm)
    # im. part of rf. index @ wavelength
    kappa = data.get_extinction_coefficient(wavelength_nm)
    n = n_real - 1j*kappa

    if cite == True:
        print(f"Refractive index of {material} - data source: {author}.")
        if author in ("Windt", "Tselin"):
            print(f"Note: The used optical constants were measured on a thin film of {material}.")

    return(n)