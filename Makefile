################################################################################
NAME = $(shell toml get --raw pyproject.toml tool.poetry.name)
VERSION = $(shell toml get --raw pyproject.toml tool.poetry.version)
RELEASE = $(shell rpmspec --srpm -q --qf '%{release}' $(NAME).spec)

CONFIG_DIR = /etc/grnoc/$(NAME)
VENV_DIR = /opt/rh/rh-python38/root

APP_FULLNAME = $(NAME)-$(VERSION)
DIST_DIR = dist/$(APP_FULLNAME)
TARBALL = dist/rh-python38-$(APP_FULLNAME).tar.gz

# All files needed to build the RPM should be listed here
DIST_FILES = $(NAME).spec pyproject.toml poetry.* README.md
DIST_DIRS = config src
################################################################################

.PHONY: all clean dist rpm setup

all: rpm

clean:
	rm -rf dist

dist: clean
	mkdir -p $(DIST_DIR)

	cp $(DIST_FILES) $(DIST_DIR)
	cp -a $(DIST_DIRS) $(DIST_DIR)

	poetry build
	mv dist/*.whl $(DIST_DIR)

	TMPDIR=$$(mktemp -d); \
		poetry bundle venv --without=dev $${TMPDIR}/venv; \
		pushd $${TMPDIR}/venv; \
		virtualenv-tools --update-path $(VENV_DIR); \
		popd; \
		cp -a $${TMPDIR}/venv $(DIST_DIR); \
		rm -rf $${TMPDIR}

	tar czf $(TARBALL) -C dist $(APP_FULLNAME) --exclude='__pycache__'

rpm: dist
	rpmbuild -vv -tb $(TARBALL) \
		-D 'py_name $(NAME)' \
		-D 'py_version $(VERSION)' \
		-D 'py_venvdir $(VENV_DIR)' \
		-D 'py_configdir $(CONFIG_DIR)' \
		-D '_topdir $(shell pwd)/dist/rpmbuild' \
		-D 'scl rh-python38'
	if test -w "${GITHUB_ENV}"; then \
		echo "name=$(NAME)" >> $$GITHUB_ENV; \
		echo "version=$(VERSION)-$(RELEASE)" >> $$GITHUB_ENV; \
	fi

setup:
	@if test -f setup-project.sh; then \
		bash setup-project.sh; \
	else \
		echo "Setup cannot be rerun. Try reverting git changes."; \
	fi
