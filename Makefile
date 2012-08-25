CONFIGS = $(patsubst %.cft,%.conf,$(wildcard *.cft))
VERSION = $(shell tmux -V | awk '{print $$NF}')

ifeq ($(VERSION),1.6)
	DEFINE = TMUX_1_6
else
	DEFINE = TMUX_1_4
endif

all:: $(CONFIGS)

%.conf: %.cft
	cpp -P -I. -Wall -Werror -D$(DEFINE) $< $@

debug:
	@echo $(CONFIGS)
	@echo $(VERSION)

clean:
	rm -rf $(CONFIGS)

