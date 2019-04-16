# Main Account Stacks

The main account stacks are deployed with [`formica`](https://theserverlessway.com/tools/formica/). To update a stack go into the respective directory and run `formica change -c stack.config.yaml`. This will create a change set that you can then deploy with `formica deploy -c stack.config.yaml`.

Before deploying the stacks you should run `formica diff -c stack.config.yaml` to get a complete diff of the changes about to be deployed. ChangeSets and a Diff together provide a secure way of knowing what is about to change before deploying changes.

For individual documentation on each stack please consult the `README.md` in each of the stack directories.

## Makefile

The Makefile lets you easily add diff all stacks in this account.