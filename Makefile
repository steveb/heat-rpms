#!/usr/bin/make

GIT_BRANCH=master
GIT_REPO_HEAT=../heat
GIT_REPO_HEAT_JEOS=../heat-jeos

RPM_HEAT_VERSION=2013.1dev
RPM_HEAT_RELEASE=$(shell date +%Y%m%d)
RPM_HEAT_JEOS_VERSION=7
RPM_HEAT_JEOS_RELEASE=1
RPM_DIST=fc17

YUM_REPO_USER=stevebake
YUM_REPO=heat-trunk
YUM_REPO_REMOTE=$(YUM_REPO_USER)@fedorapeople.org:/srv/repos/heat/$(YUM_REPO)
YUM_DIST=fedora-17

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

yum-repo-clean: yum-repo
	rm -rf yum-repo/$(YUM_REPO)

yum-repo:
	mkdir -p yum-repo/$(YUM_REPO)

yum-repo-populate:
	cp -f rpm-build/noarch/*.$(RPM_DIST).noarch.rpm yum-repo/$(YUM_REPO)/$(YUM_DIST)/i386
	cp -f rpm-build/noarch/*.$(RPM_DIST).noarch.rpm yum-repo/$(YUM_REPO)/$(YUM_DIST)/x86_64
	cp -f rpm-build/*.src.rpm yum-repo/$(YUM_REPO)/$(YUM_DIST)/SRPMS

yum-repo-pull: yum-repo
	rsync -avtx $(YUM_REPO_REMOTE)/* yum-repo/$(YUM_REPO)

yum-repo-push:
	rsync -avtx yum-repo/$(YUM_REPO)/* $(YUM_REPO_REMOTE)

.PHONEY: all rpmcommon clean heatsrpm heatrpm
vpath %.asciidoc docs/man/man1
