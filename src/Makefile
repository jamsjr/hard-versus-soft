
INI_DONE= $(patsubst %.ini,%.done,$(wildcard config/*.ini))

all: $(INI_DONE)

%.done: %.ini
	python simul.py run $<
