# mosi.py
Modelling & Optimization Solver Interface (MOSI).

#### PyPITest

###### Register
```bash
python setup.py register -r testpypi
```

###### Upload
```bash
rm -rf build dist
python setup.py sdist bdist_wheel
twine upload -r testpypi dist/*
```

#### PyPIT

###### Register
```bash
python setup.py register -r pypi
```

###### Upload
```bash
rm -rf build dist
python setup.py sdist bdist_wheel
twine upload -r pypi dist/*
```
