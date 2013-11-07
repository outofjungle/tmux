.PHONY: install

all: install

install: tmux.conf
	ln -sf $(CURDIR)/tmux.conf ~/.tmux.conf
