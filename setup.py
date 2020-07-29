with open('requirements.txt') as fid:
    requires = [line.strip() for line in fid]
...
setup(
  ...,
  install_requires=requires,
  ...
)