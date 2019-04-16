# Stack Sets

The stack sets are deployed with [`formica`](https://theserverlessway.com/tools/formica/). To update a stack set or manage instances go into the respective directory. 

To update the template used by a StackSet run the `update` command`:

```bash
formica stack-set update -c stack-set.config.yaml
``` 

This will update all stack instances currently in use by the stack-set.

To add new instances run `add-instances`:

```bash
formica stack-set add-instances -c stack-set.config.yaml
``` 

To remove instances run `remove-instances`:

```bash
formica stack-set remove-instances -c stack-set.config.yaml
``` 

For a complete documentation of all available stack-set commands in formica check out the [`Commands Reference`](https://theserverlessway.com/tools/formica/commands/)

For individual documentation on each stack please consult the `README.md` in each of the stack directories.

## Execution Role

Before deploying other StackSets you need to deploy the `stack-set-execution-role` to make sure the role is available in each subaccount. Otherwise any further addition of stack instances will fail.
