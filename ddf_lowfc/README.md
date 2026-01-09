Only execute when filter is already loaded. Hopefully to reduce total number of filter changes is year 1

Looks like this cuts filter changes in year 1 from 3093 to 2124. Also cuts most DDF visits by nearly ~2x. That's not too surprising since the DDFs are set to a flush length of 0.5 days. Can either increase the flush time, or increase the sequence length.

And increasing the flush by date seems to do the trick. On some it even gets more observations since now we are recovering from weather misses.

