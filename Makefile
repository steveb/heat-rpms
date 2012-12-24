#!/usr/bin/make

GIT_BRANCH=master
GIT_REPO_HEAT=../heat
GIT_REPO_HEAT_JEOS=../heat-jeos

RPM_HEAT_VERSION=2013.1dev
RPM_HEAT_RELEASE=$(shell date +%Y%m%d)
RPM_HEAT_JEOS_VERSION=7
RPM_HEAT_JEOS_RELEASE=1
RPM_DIST=fc17

include local.mk

all: clean heatrpm jeosrpm

rpmcommon:
	@mkdir -p rpm-build
	@cp patches/* rpm-build/

heatcommon:
	@cp *.logrotate rpm-build/
	@cp *.service rpm-build/

clean: 
	@echo "Cleaning up, removing rpm-build dir"
	-rm -rf rpm-build
	-rm -rf git-repos

# buildargs, spec, rpmtype
buildrpm = \
	@rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir %{_topdir}" \
	--define "_sourcedir %{_topdir}" \
    --define "_version $(4)" \
    --define "_release $(5)" \
	-$(1) $(2); \
	echo "+++++++++++++++++++++++++++++++++++++++++++++"; \
	echo -n "built:   $(shell awk '/Name/{print $$2}' < $(2))"; \
	echo "-$(4)-$(5).$(3).rpm"; \
	echo "+++++++++++++++++++++++++++++++++++++++++++++";

heatsrpm: rpmcommon heatcommon rpm-build/heat-$(RPM_HEAT_VERSION).tar.gz
	$(call buildrpm,bs,heat.spec,src,$(RPM_HEAT_VERSION),$(RPM_HEAT_RELEASE))

heatrpm: rpmcommon heatcommon rpm-build/heat-$(RPM_HEAT_VERSION).tar.gz
	$(call buildrpm,ba,heat.spec,noarch,$(RPM_HEAT_VERSION),$(RPM_HEAT_RELEASE))

jeossrpm: rpmcommon rpm-build/heat-jeos-$(RPM_HEAT_JEOS_VERSION).tar.gz
	$(call buildrpm,bs,heat-jeos.spec,src,$(RPM_HEAT_JEOS_VERSION),$(RPM_HEAT_JEOS_RELEASE))

jeosrpm: rpmcommon rpm-build/heat-jeos-$(RPM_HEAT_JEOS_VERSION).tar.gz
	$(call buildrpm,ba,heat-jeos.spec,noarch,$(RPM_HEAT_JEOS_VERSION),$(RPM_HEAT_JEOS_RELEASE))

git-repos:
	mkdir git-repos

git-repos/heat: git-repos
	git clone $(GIT_REPO_HEAT) git-repos/heat

git-repos/heat-jeos: git-repos
	git clone $(GIT_REPO_HEAT_JEOS) git-repos/heat-jeos

sdist-from-git = \
	cd git-repos/$(1) && \
	git clean -d -x -f && \
	git reset --hard $(2) && \
	git pull origin $(2) && \
	./setup.py sdist && \
	cp dist/* ../../rpm-build

rpm-build/heat-$(RPM_HEAT_VERSION).tar.gz: git-repos/heat
	$(call sdist-from-git,heat,$(GIT_BRANCH))

rpm-build/heat-jeos-$(RPM_HEAT_JEOS_VERSION).tar.gz: git-repos/heat-jeos
	$(call sdist-from-git,heat-jeos,$(GIT_BRANCH))

.PHONEY: all rpmcommon clean heatsrpm heatrpm
vpath %.asciidoc docs/man/man1
