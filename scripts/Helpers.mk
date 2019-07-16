.PHONY: excluded
excluded:
	@echo "Excluded Stack Sets:"
	@ls -d */ | grep -Ff Excluded

LIST_DIRS=@ls -d */ | grep -vFf Excluded

FOR_ALL_DIRS=$(LIST_DIRS) | xargs -n 1 -I {} bash -c "cd {} && echo '--------- {}' && $1 && echo ''"