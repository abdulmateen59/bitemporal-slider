python usr/local/bin/bitemporal-slider --initial_start=2000-12-31 --end=2001-01-02 --system_time=2001-01-03 --sliding_steps=3 --sliding_delta=1
echo "**************************************************************************"
python usr/local/bin/bitemporal-slider --initial_start=2001-01-01 --end=2001-01-03 --system_time=2001-01-03 --sliding_steps=3 --sliding_delta=2
echo "**************************************************************************"
python usr/local/bin/bitemporal-slider --initial_start=2001-01-02 --end=2001-01-04 --system_time=2001-01-03 --sliding_steps=3 --sliding_delta=3
echo "**************************************************************************"
python usr/local/bin/bitemporal-slider --initial_start=2001-01-03 --end=2001-01-05 --system_time=2001-01-03 --sliding_steps=2 --sliding_delta=1
echo "**************************************************************************"
python usr/local/bin/bitemporal-slider --initial_start=2001-01-04 --end=2001-01-06 --system_time=2001-01-03 --sliding_steps=4 --sliding_delta=1
