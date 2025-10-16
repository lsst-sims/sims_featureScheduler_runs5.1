__all__ = ("SmallFP1", "SmallFP2")

import numpy as np
import healpy as hp
from rubin_scheduler.scheduler.utils import CurrentAreaMap
from rubin_scheduler.utils import DEFAULT_NSIDE


default_kwargs = {"nside":DEFAULT_NSIDE,
        "dust_limit":0.199,
        "smoothing_cutoff":0.45,
        "smoothing_beam":10,
        "lmc_ra":80.893860,
        "lmc_dec":-69.756126,
        "lmc_radius":6,
        "smc_ra": 13.186588,
        "smc_dec" : -72.828599,
        "smc_radius": 4,
        "scp_dec_max":-60,
        "gal_long1":335,
        "gal_long2":25,
        "gal_lat_width_max":23,
        "center_width":12,
        "end_width":4,
        "gal_dec_max":12,
        "low_dust_dec_min":-70,
        "low_dust_dec_max":15,
        "adjust_halves":12,
        "dusty_dec_min":-90,
        "dusty_dec_max":15,
        "eclat_min":-10,
        "eclat_max":10,
        "eclip_dec_min":0,
        "nes_glon_limit":45.0,
        "virgo_ra":186.75,
        "virgo_dec":12.717,
        "virgo_radius":8.75,
        "euclid_contour_file":None,
}


class SmallFP1(CurrentAreaMap):
    """Adjust the limits of the footprint
    """

    def __init__(self):
        kw = default_kwargs

        kw["low_dust_dec_max"] = 5
        kw["dusty_dec_max"] = 5
        kw["eclip_dec_min"] = -10

        super().__init__(**kw)

    def return_maps(
        self,
        magellenic_clouds_ratios={
            "u": 0.65,
            "g": 0.65,
            "r": 1.1,
            "i": 1.1,
            "z": 0.34,
            "y": 0.35,
        },
        scp_ratios={"u": 0.1, "g": 0.175, "r": 0.1, "i": 0.135, "z": 0.046, "y": 0.047},
        nes_ratios={"g": 0.255, "r": 0.33, "i": 0.33, "z": 0.23},
        dusty_plane_ratios={
            "u": 0.093,
            "g": 0.26,
            "r": 0.26,
            "i": 0.26,
            "z": 0.26,
            "y": 0.093,
        },
        low_dust_ratios={"u": 0.35, "g": 0.4, "r": 1.0, "i": 1.0, "z": 0.9, "y": 0.9},
        bulge_ratios={"u": 0.17, "g": 0.93, "r": 0.98, "i": 0.98, "z": 0.93, "y": 0.21},
        virgo_ratios={"u": 0.35, "g": 0.4, "r": 1.0, "i": 1.0, "z": 0.9, "y": 0.9},
        euclid_ratios={"u": 0.35, "g": 0.4, "r": 1.0, "i": 1.0, "z": 0.9, "y": 0.9},
    ):
        # Array to hold the labels for each pixel
        self.pix_labels = np.zeros(hp.nside2npix(self.nside), dtype="U20")
        self.healmaps = np.zeros(
            hp.nside2npix(self.nside),
            dtype=list(zip(["u", "g", "r", "i", "z", "y"], [float] * 7)),
        )

        # Note, order here matters.
        # Once a HEALpix is set and labled, subsequent add_ methods
        # will not override that pixel.
        self.add_magellanic_clouds(magellenic_clouds_ratios)
        self.add_lowdust_wfd(low_dust_ratios)
        self.add_virgo_cluster(virgo_ratios)
        self.add_bulgy(bulge_ratios)
        self.add_nes(nes_ratios)
        self.add_dusty_plane(dusty_plane_ratios)
        self.add_euclid_overlap(euclid_ratios)
        self.add_scp(scp_ratios)

        return self.healmaps, self.pix_labels


class SmallFP2(CurrentAreaMap):
    """Adjust the limits of the footprint
    """

    def __init__(self):
        kw = default_kwargs

        kw["low_dust_dec_max"] = 2.
        kw["low_dust_dec_min"] = -60
        kw["dusty_dec_max"] = 2
        kw["eclip_dec_min"] = -10

        super().__init__(**kw)
