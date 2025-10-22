__all__ = (
    "sched_argparser",
    "set_run_info",
    "run_sched",
)

from fbs_config_lsst_survey import get_scheduler
import argparse
import os
import subprocess
import sys

import numpy as np
import numpy.typing as npt
import rubin_scheduler
from astropy.utils import iers
from rubin_scheduler.scheduler import sim_runner
from rubin_scheduler.scheduler.model_observatory import ModelObservatory, tma_movement
from rubin_scheduler.scheduler.schedulers import CoreScheduler, SimpleBandSched
from rubin_scheduler.scheduler.targetofo import gen_all_events
from rubin_scheduler.scheduler.utils import  ObservationArray
from rubin_scheduler.utils import DEFAULT_NSIDE, SURVEY_START_MJD


# So things don't fail on hyak
iers.conf.auto_download = False
# XXX--note this line probably shouldn't be in production
iers.conf.auto_max_age = None



def set_run_info(
    dbroot: str | None = None, file_end: str = "", out_dir: str = "."
) -> tuple[str, dict]:
    """Gather versions of software used to record"""
    extra_info = {}
    exec_command = ""
    for arg in sys.argv:
        exec_command += " " + arg
    extra_info["exec command"] = exec_command
    try:
        extra_info["git hash"] = subprocess.check_output(["git", "rev-parse", "HEAD"])
    except subprocess.CalledProcessError:
        extra_info["git hash"] = "Not in git repo"

    extra_info["file executed"] = os.path.realpath(__file__)
    try:
        rs_path = rubin_scheduler.__path__[0]
        hash_file = os.path.join(rs_path, "../", ".git/refs/heads/main")
        extra_info["rubin_scheduler git hash"] = subprocess.check_output(
            ["cat", hash_file]
        )
    except subprocess.CalledProcessError:
        pass

    # Use the filename of the script to name the output database
    if dbroot is None:
        fileroot = os.path.basename(sys.argv[0]).replace(".py", "") + "_"
    else:
        fileroot = dbroot + "_"
    fileroot = os.path.join(out_dir, fileroot + file_end)
    return fileroot, extra_info


def run_sched(
    scheduler: CoreScheduler,
    survey_length: float = 365.25,
    nside: int = DEFAULT_NSIDE,
    filename: str | None = None,
    verbose: bool = False,
    extra_info: dict | None = None,
    illum_limit: float = 40.0,
    survey_start_mjd: float = 60796.0,
    event_table: npt.NDArray | None = None,
    sim_to_o=None,
    snapshot_dir: str | None = None,
    readtime: float = 3.07,
    band_changetime: float = 140.0,
    tma_performance: float = 40.0,
) -> tuple[ModelObservatory, CoreScheduler, ObservationArray]:
    """Run survey"""
    n_visit_limit = None
    fs = SimpleBandSched(illum_limit=illum_limit)
    observatory = ModelObservatory(
        nside=nside, mjd_start=survey_start_mjd, sim_to_o=sim_to_o
    )

    tma_kwargs = tma_movement(percent=tma_performance)
    observatory.setup_telescope(**tma_kwargs)
    observatory.setup_camera(band_changetime=band_changetime, readtime=readtime)

    observatory, scheduler, observations = sim_runner(
        observatory,
        scheduler,
        sim_duration=survey_length,
        filename=filename,
        delete_past=True,
        n_visit_limit=n_visit_limit,
        verbose=verbose,
        extra_info=extra_info,
        band_scheduler=fs,
        event_table=event_table,
        snapshot_dir=snapshot_dir,
    )

    return observatory, scheduler, observations


def gen_scheduler(
    args: argparse.ArgumentParser,
) -> tuple[ModelObservatory, CoreScheduler, ObservationArray] | CoreScheduler:

    survey_length = args.survey_length  # Days
    out_dir = args.out_dir
    verbose = args.verbose
    dbroot = args.dbroot
    nside = args.nside
    snapshot_dir = args.snapshot_dir
    too = not args.no_too
    
    survey_start_mjd = SURVEY_START_MJD
    illum_limit = 40.0 

    if too:
        too_scale = 1.0
        sim_ToOs, event_table = gen_all_events(scale=too_scale, nside=nside)

    fileroot, extra_info = set_run_info(
        dbroot=dbroot,
        file_end="v5.1.0_",
        out_dir=out_dir,
    )

    nside, scheduler = get_scheduler()
    
    years = np.round(survey_length / 365.25)
    observatory, scheduler, observations = run_sched(
        scheduler,
        survey_length=survey_length,
        verbose=verbose,
        filename=os.path.join(fileroot + "%iyrs.db" % years),
        extra_info=extra_info,
        nside=nside,
        illum_limit=illum_limit,
        survey_start_mjd=survey_start_mjd,
        event_table=event_table,
        sim_to_o=sim_ToOs,
        snapshot_dir=snapshot_dir,
    )
    return observatory, scheduler, observations


def sched_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose", dest="verbose", action="store_true", help="Print more output"
    )
    parser.set_defaults(verbose=False)
    parser.add_argument(
        "--survey_length", type=float, default=365.25 * 10, help="Survey length in days"
    )
    parser.add_argument("--out_dir", type=str, default="", help="Output directory")
    parser.add_argument("--dbroot", type=str, help="Database root")
    parser.add_argument(
        "--setup_only",
        dest="setup_only",
        default=False,
        action="store_true",
        help="Only construct scheduler, do not simulate",
    )
    parser.add_argument(
        "--nside",
        type=int,
        default=DEFAULT_NSIDE,
        help="Nside should be set to default (32) except for tests.",
    )
    parser.add_argument(
        "--mjd_plus",
        type=float,
        default=0,
        help="number of days to add to the mjd start",
    )
    parser.add_argument(
        "--split_long",
        dest="split_long",
        action="store_true",
        help="Split long ToO exposures into standard visit lengths",
    )
    parser.add_argument(
        "--snapshot_dir",
        type=str,
        default="",
        help="Directory for scheduler snapshots.",
    )
    parser.set_defaults(split_long=False)
    parser.add_argument("--no_too", dest="no_too", action="store_true")
    parser.set_defaults(no_too=False)

    return parser


if __name__ == "__main__":
    parser = sched_argparser()
    args = parser.parse_args()
    gen_scheduler(args)
