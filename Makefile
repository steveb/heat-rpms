#!/usr/bin/make

NAME = "heat"
ASCII2MAN = a2x -D $(dir $@) -d manpage -f manpage $<
ASCII2HTMLMAN = a2x -D docs/html/man/ -d manpage -f xhtml
MANPAGES := docs/man/man1/heat.1 docs/man/man1/heat-engine.1 docs/man/man1/heat-api.1
SITELIB = $(shell python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")
RPMVERSION := $(shell awk '/Version/{print $$2; exit}' < heat.spec | cut -d "%" -f1)
RPMRELEASE := $(shell awk '/Release/{print $$2; exit}' < heat.spec | cut -d "%" -f1)
RPMNVR = "$(NAME)-$(RPMVERSION)-$(RPMRELEASE)"

all: clean python

docs: $(MANPAGES)

%.1: %.1.asciidoc
	$(ASCII2MAN)

%.5: %.5.asciidoc
	$(ASCII2MAN)

rpmcommon:
	@mkdir -p rpm-build
	@cp *.gz rpm-build/

clean:
	@echo "Cleaning up, removing rpm-build dir"
	-rm -rf rpm-build

srpm: rpmcommon
	@rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir %{_topdir}" \
	-bs heat.spec
	@echo "#############################################"
	@echo "heat SRPM is built:"
	@echo "    rpm-build/$(RPMNVR).src.rpm"
	@echo "#############################################"

rpm: rpmcommon
	@rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir %{_topdir}" \
	-ba heat.spec
	@echo "#############################################"
	@echo "heat RPM is built:"
	@echo "    rpm-build/noarch/$(RPMNVR).noarch.rpm"
	@echo "#############################################"

.PHONEY: docs manual clean pep8
vpath %.asciidoc docs/man/man1
