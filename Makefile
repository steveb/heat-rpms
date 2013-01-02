#!/usr/bin/make

GIT_BRANCH=master
GIT_REPO_HEAT=../heat
GIT_REPO_HEAT_CFNTOOLS=../heat-cfntools

RPM_HEAT_VERSION=2013.1dev
RPM_HEAT_RELEASE=$(shell date +%Y%m%d)
RPM_HEAT_CFNTOOLS_VERSION=1.0
RPM_HEAT_CFNTOOLS_RELEASE=$(shell date +%Y%m%d)
RPM_DIST=fc17

YUM_REPO_USER=stevebake
YUM_REPO=heat-trunk
YUM_REPO_REMOTE=$(YUM_REPO_USER)@fedorapeople.org:/srv/repos/heat/$(YUM_REPO)

include local.mk

all: clean heat-rpms cfntools-rpms

rpmcommon:
	mkdir -p rpm-build/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	cp patches/* rpm-build/SOURCES/

heatcommon:
	cp *.logrotate rpm-build/SOURCES/
	cp *.service rpm-build/SOURCES/
	cp *.spec rpm-build/SPECS/

clean: 
	@echo "Cleaning up, removing rpm-build dir"
	-rm -rf rpm-build
	-rm -rf git-repos

build-srpm = \
    rpmbuild -bs --define "_topdir $(CURDIR)/rpm-build" \
    --define "_version $(2)" \
    --define "_release $(3)" \
    --target "" \
    rpm-build/SPECS/$(1)

build-rpms = \
    mock -r $(1)\
    --define "_version $(3)" \
    --define "_release $(4)" \
    --resultdir=rpm-build/RPMS \
    rpm-build/SRPMS/$(2)-$(3)-$(4).$(RPM_DIST).src.rpm

heat-srpm: rpmcommon heatcommon rpm-build/SOURCES/heat-$(RPM_HEAT_VERSION).tar.gz
	$(call build-srpm,heat.spec,$(RPM_HEAT_VERSION),$(RPM_HEAT_RELEASE))

heat-rpms: heat-srpm
	$(call build-rpms,fedora-17-x86_64,heat,$(RPM_HEAT_VERSION),$(RPM_HEAT_RELEASE))
	$(call build-rpms,fedora-18-x86_64,heat,$(RPM_HEAT_VERSION),$(RPM_HEAT_RELEASE))

cfntools-srpm: rpmcommon heatcommon rpm-build/SOURCES/heat-cfntools-$(RPM_HEAT_CFNTOOLS_VERSION).tar.gz
	$(call build-srpm,heat-cfntools.spec,$(RPM_HEAT_CFNTOOLS_VERSION),$(RPM_HEAT_CFNTOOLS_RELEASE))

cfntools-rpms: cfntools-srpm
	$(call build-rpms,fedora-16-x86_64,heat-cfntools,$(RPM_HEAT_CFNTOOLS_VERSION),$(RPM_HEAT_CFNTOOLS_RELEASE))
	$(call build-rpms,fedora-17-x86_64,heat-cfntools,$(RPM_HEAT_CFNTOOLS_VERSION),$(RPM_HEAT_CFNTOOLS_RELEASE))
	$(call build-rpms,fedora-18-x86_64,heat-cfntools,$(RPM_HEAT_CFNTOOLS_VERSION),$(RPM_HEAT_CFNTOOLS_RELEASE))
	$(call build-rpms,epel-6-x86_64,heat-cfntools,$(RPM_HEAT_CFNTOOLS_VERSION),$(RPM_HEAT_CFNTOOLS_RELEASE))

git-repos:
	mkdir git-repos

git-repos/heat: git-repos
	git clone $(GIT_REPO_HEAT) git-repos/heat

git-repos/heat-cfntools: git-repos
	git clone $(GIT_REPO_HEAT_CFNTOOLS) git-repos/heat-cfntools

sdist-from-git = \
	cd git-repos/$(1) && \
	git clean -d -x -f && \
	git reset --hard $(2) && \
	git pull origin $(2) && \
	./setup.py sdist && \
	cp dist/* ../../rpm-build/SOURCES

rpm-build/SOURCES/heat-$(RPM_HEAT_VERSION).tar.gz: git-repos/heat
	$(call sdist-from-git,heat,$(GIT_BRANCH))

rpm-build/SOURCES/heat-cfntools-$(RPM_HEAT_CFNTOOLS_VERSION).tar.gz: git-repos/heat-cfntools
	$(call sdist-from-git,heat-cfntools,$(GIT_BRANCH))

yum-repo-clean: yum-repo
	rm -rf yum-repo/$(YUM_REPO)

yum-repo:
	mkdir -p yum-repo/$(YUM_REPO)

repo-populate-single = \
	cp -f rpm-build/RPMS/*.$(2).$(3).rpm yum-repo/$(YUM_REPO)/$(1)/$(4) ; \
	createrepo --database yum-repo/$(YUM_REPO)/$(1)/$(4)

repo-populate = \
	$(call repo-populate-single,$(1),$(2),noarch,i386) && \
	$(call repo-populate-single,$(1),$(2),noarch,x86_64) && \
	$(call repo-populate-single,$(1),$(2),src,SRPMS)

yum-repo-populate: yum-repo-pull
	$(call repo-populate,fedora-16,fc16)
	$(call repo-populate,fedora-17,fc17)
	$(call repo-populate,fedora-18,fc18)
	$(call repo-populate,epel-6,el6)

yum-repo-pull: yum-repo
	rsync -avtx --delete $(YUM_REPO_REMOTE)/* yum-repo/$(YUM_REPO)

yum-repo-push:
	rsync -avtx --delete yum-repo/$(YUM_REPO)/* $(YUM_REPO_REMOTE)

.PHONEY: all rpmcommon clean heatsrpm heatrpm
vpath %.asciidoc docs/man/man1
