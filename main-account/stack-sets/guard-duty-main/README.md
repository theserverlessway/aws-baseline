# GuardDuty Master

This StackSet sets up a GuardDuty Master in every region of the main account. Therefore it should only be deployed into the main account to pull data from all Subaccounts.

When adding a new Account please add the account details to the config.yaml file and update the StackSet.

When removing an Account make sure you remove it from the config.yaml file and update this StackSet.
