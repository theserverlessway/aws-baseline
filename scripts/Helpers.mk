.PHONY: excluded
excluded:
	@echo "Excluded:"
	@ls -d */ | grep -Ff Excluded || true

LIST_DIRS=@ls -d */ | grep -vFf Excluded

FOR_ALL_DIRS=$(LIST_DIRS) | xargs -n 1 -I {} bash -c "cd {} && echo '--------- {}' && $1 && echo ''"