Looks like these produce identical output

Ran in the same amount of time (that's kinda imperessive).

They had memory footprints of 11 and 12 GB respectively. I think most of that had to be the sky files not purging properly.

Should do a test where I limit the sky load size


----

testing again with QueueManager and SummitWrapper 


python wrapper.py --verbose --survey_length 60

Flushed 0 observations from queue for being stale
Completed 23452 observations
ran in 10 min = 0.2 hours
Writing results to  wrapper_v5.1.1_0yrs.db


progress = 100.05%Skipped 0 observations
Flushed 0 observations from queue for being stale
Completed 23452 observations
ran in 10 min = 0.2 hours
Writing results to  baseline_v5.1.0_0yrs.db

ok, so wrapper doesn't change anything
