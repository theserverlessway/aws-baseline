include ../scripts/Helpers.mk

diff:
	$(call FOR_ALL_DIRS,formica diff -c stack.config.yaml)

rollout:
	$(call FOR_ALL_DIRS,formica change -c stack.config.yaml --create-missing && formica deploy -c stack.config.yaml)

