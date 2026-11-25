module := "gmacli"

run:
  python -m {{module}}

fmt:
  black {{module}}
  isort {{module}}

# TODO: bump command
