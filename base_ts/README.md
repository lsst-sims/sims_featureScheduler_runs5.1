Try importing and running the scheduler that's in ts_config_scheduler

to setup and sync files:


cp ~/git_repos/ts_config_scheduler/Scheduler/feature_scheduler/maintel/fbs_config_lsst_survey.py .
# cp ~/git_repos/ts_config_scheduler/Scheduler/ddf_gen/lsst_ddf_gen.py .


checking cross-platform:
on M2:
Flushed 219757 observations from queue for being stale
Completed 2029642 observations
ran in 778 min = 13.0 hours

on usdf:
Flushed 219757 observations from queue for being stale
Completed 2029642 observations
ran in 1377 min = 23.0 hours

so we are cross-platform at least
