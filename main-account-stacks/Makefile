diff-stacks:
	@ls -d */ | xargs -n 1 -I {} bash -c "echo '{} ----------------------------------' && cd {} && formica diff -c stack.config.yaml && echo -e '\n\n'"
