CONFIGS = $(patsubst %.cft,%.conf,$(wildcard *.cft))
TMUX_VERSION = $(addprefix TMUX_,$(subst .,_,$(shell tmux -V | awk '{print $$NF}')))

.PHONY: install

all: $(CONFIGS)

%.conf: %.cft
ifeq ($(TMUX_VERSION),)
	cpp -P -I. -Wall -Werror $< $@
else
	cpp -P -I. -Wall -Werror -D$(TMUX_VERSION) $< $@
endif

install: tmux.conf
	ln -sf $(CURDIR)/tmux.conf ~/.tmux.conf

clean:
	rm -rf $(CONFIGS)

