# Budgets

Creates standard budgets in each member account. The StackSet needs to be created in the `devops` account of the corresponding environment.

```
# The account ids from development.checkout and development.core
export INSTANCE_ACCOUNT_IDS="083576646871 019283549872"

# Create the Stack Set if it does not exists. 
formica stack-set create --profile development.devops -c stack.config.yaml ../development.config.yaml

# Add DevOps Instance if it does not exists. (exception-- only run this command when you are creating Devops account for first time) 
formica stack-set add-instances --profile development.devops -c stack.config.yaml --regions eu-central-1 --accounts ${DevOps_ACCOUNT_IDS} --regions eu-central-1


# Update the StackSet
formica stack-set update --profile development.devops -c stack.config.yaml ../development.config.yaml

# Add instances to the StackSet
formica stack-set add-instances --profile development.devops -c stack.config.yaml ../development.config.yaml --accounts ${INSTANCE_ACCOUNT_IDS} --regions eu-central-1
```
