clean:
	rm -f python3-globalnoc-wsc-*.rpm
	rm -rf build dist src/globalnoc_wsc.egg-info

rpm:
	fpm -s python -t rpm --python-bin /usr/bin/python3 --python-package-name-prefix python3 setup.py
