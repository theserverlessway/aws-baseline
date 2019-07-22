.PHONY: excluded
LIST_DIRS=@ls -d */ | grep -vFf Excluded


included:
	@echo "Included:"
	$(LIST_DIRS) || true

excluded:
	@echo "Excluded:"
	@ls -d */ | grep -Ff Excluded || true


FOR_ALL_DIRS=$(LIST_DIRS) | xargs -n 1 -I {} bash -c "cd {} && echo '--------- {}' && $1 && echo ''"
