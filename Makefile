#!/usr/bin/make

ASCII2MAN = a2x -D $(dir $@) -d manpage -f manpage $<
ASCII2HTMLMAN = a2x -D docs/html/man/ -d manpage -f xhtml
HEATMANPAGES := docs/man/man1/heat.1 docs/man/man1/heat-engine.1 docs/man/man1/heat-api.1
SITELIB = $(shell python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")

all: clean heatrpm jeosrpm

heatdocs: $(HEATMANPAGES)

%.1: %.1.asciidoc
	$(ASCII2MAN)

%.5: %.5.asciidoc
	$(ASCII2MAN)

rpmcommon:
	@mkdir -p rpm-build
	@cp *.gz rpm-build/
	@cp patches/* rpm-build/

heatcommon:
	@cp *.logrotate rpm-build/
	@cp *.service rpm-build/

clean:
	@echo "Cleaning up, removing rpm-build dir"
	-rm -rf rpm-build

# buildargs, spec, rpmtype
buildrpm = \
		@rpmbuild --define "_topdir %(pwd)/rpm-build" \
		--define "_builddir %{_topdir}" \
		--define "_rpmdir %{_topdir}" \
		--define "_srcrpmdir %{_topdir}" \
		--define "_specdir %{_topdir}" \
		--define "_sourcedir %{_topdir}" \
		-$(1) $(2); \
		echo "+++++++++++++++++++++++++++++++++++++++++++++"; \
		echo -n "built:   $(shell awk '/Name/{print $$2}' < $(2))"; \
		echo -n "-$(shell awk '/Version/{print $$2}' < $(2))"; \
		echo -n "-$(shell awk '/Release/{print $$2}' < $(2))"; \
		echo ".$(3).rpm"; \
		echo "+++++++++++++++++++++++++++++++++++++++++++++";

heatsrpm: rpmcommon heatcommon
	$(call buildrpm,bs,heat.spec,src)

heatrpm: rpmcommon heatcommon
	$(call buildrpm,ba,heat.spec,noarch)

jeossrpm: rpmcommon
	$(call buildrpm,bs,heat_jeos.spec,src)

jeosrpm: rpmcommon
	$(call buildrpm,ba,heat_jeos.spec,noarch)

.PHONEY: all heatdocs rpmcommon clean heatsrpm heatrpm
vpath %.asciidoc docs/man/man1
