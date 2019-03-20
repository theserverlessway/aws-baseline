# Disabled Regions Rules

In disabled regions we want to make sure that no resources are deployed. To achieve this
the `fail-on-resources` Config rule is created that is listening to any resource changes
and fails for all of them.

A few exceptions are made for the resources necessary for auditing that region.
