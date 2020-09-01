# Running aws-baseline from Microsoft Windows

While aws-baseline itself requires a POSIX environment, it can now run within Microsoft Windows. This is done by passing commands through Docker using the [3 Musketeers](https://3musketeers.io/) developer pattern.

## Installation

The following software is required to run aws-baseline under Windows:

- [Docker Desktop](https://www.docker.com/products/docker-desktop) for Windows (version 2.0 or later)
- GNU Make (version 3.81 or later)

### Installing GNU Make

GNU Make can be installed in Windows though package managers such as [Chocolatey](https://chocolatey.org) and [scoop](https://scoop.sh).

Installing make via Chocolatey:

```bat
choco install -y make
```

Install make via Scoop:

```bat
scoop install make
```

### Optional components

The following is optional but highly recommended:

- [AWS Command Line Interface](https://aws.amazon.com/cli/) (version 1.17 or greater)

## Using aws-baseline through Docker

### Running awsinfo commands

Before you can run `awsinfo` commands you should pull the awsinfo image from the Docker Hub registry:

```bat
make pull-awsinfo
```

To tell `make` to run awsinfo through Docker Compose, use the `ComposeAwsinfo=1` argument. This is required when invoking the `list-accounts` target as it depends on awsinfo.

```bat
make ComposeAwsinfo=1 list-accounts
```

For custom invocations of awsinfo, the Makefile has an `awsinfo` target with a required `Args` variable. Here is an example of running `aws credentials`:

```bat
make ComposeAwsinfo=1 awsinfo Args=credentials
```

### Running baseline operations

To run a baseline operation, run the corresponding baseline make target through Docker Compose. The Makefile has a `compose-make` target for this purpose.

The `compose-make` target is required to invoke any of the following top-level make targets from Windows:

- rollout
- diff
- excluded
- test-python

The following targets require either the use of `compose-make` or for the AWS command-line client to be installed:

- create-account
- create-account-alias

Note that the `compose-make` target builds the baseline Docker image at each invocation. The first invocation may be quite slow as the Docker image is built, but subsequent invocations should be much faster as successful Docker build steps are cached.

#### Example

To roll out the baseline with the default values (normally "make rollout"):

```bat
make compose-make Args=rollout
```
