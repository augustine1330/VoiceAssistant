import scipy.special as sp

if not hasattr(sp, 'sph_harm'):
    try:
        from scipy.special import sph_harm_y as sph_harm
        sp.sph_harm = sph_harm
    except Exception:
        pass
