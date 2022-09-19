# newchain-account

Sign NewChain transactions and messages with local private keys

## Quickstart

```sh
pip install newchain-account
```

## Developer Setup

## Developer setup

If you would like to hack on newchain-account, please check out the
[Ethereum Development Tactical Manual](https://github.com/pipermerriam/ethereum-dev-tactical-manual)
for information on how we do:

- Testing
- Pull Requests
- Code Style
- Documentation

### Development Environment Setup

You can set up your dev environment with:

```sh

git clone git@github.com:newtonproject/newchain-lib-account-py.git
cd newchain-lib-account-py
virtualenv -p python3 venv
. venv/bin/activate
pip install -e ".[dev]"
```

To run the integration test cases, you need to install node and the custom cli tool as follows:

```sh
apt-get install -y nodejs  # As sudo
./tests/integration/ethers-cli/setup_node_v12.sh  # As sudo
cd tests/integration/ethers-cli
npm install -g .  # As sudo
```

### Testing Setup

During development, you might like to have tests run on every file save.

Show flake8 errors on file change:

```sh
# Test flake8
when-changed -v -s -r -1 newchain_account/ tests/ -c "clear; flake8 newchain_account tests && echo 'flake8 success' || echo 'error'"
```

Run multi-process tests in one command, but without color:

```sh
# in the project root:
pytest --numprocesses=4 --looponfail --maxfail=1
# the same thing, succinctly:
pytest -n 4 -f --maxfail=1
```

Run in one thread, with color and desktop notifications:

```sh
cd venv
ptw --onfail "notify-send -t 5000 'Test failure ⚠⚠⚠⚠⚠' 'python 3 test on newchain-account failed'" ../tests ../newchain_account
```

### Release setup

For Debian-like systems:
```
apt install pandoc
```

To release a new version:

```sh
make release bump=$$VERSION_PART_TO_BUMP$$
```

#### How to bumpversion

The version format for this repo is `{major}.{minor}.{patch}` for stable, and
`{major}.{minor}.{patch}-{stage}.{devnum}` for unstable (`stage` can be alpha or beta).

To issue the next version in line, specify which part to bump,
like `make release bump=minor` or `make release bump=devnum`. This is typically done from the
master branch, except when releasing a beta (in which case the beta is released from master,
and the previous stable branch is released from said branch).

If you are in a beta version, `make release bump=stage` will switch to a stable.

To issue an unstable version when the current version is stable, specify the
new version explicitly, like `make release bump="--new-version 4.0.0-alpha.1 devnum"`
