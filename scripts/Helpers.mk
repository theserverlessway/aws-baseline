excluded-stack-sets:
	@echo "Excluded Stack Sets:"
	@ls -d */ | grep -f Excluded

LIST_DIRS=@ls -d */ | grep -v -f Excluded

FOR_ALL_DIRS=$(LIST_DIRS) | xargs -n 1 -I {} bash -c "cd {} && echo '--------- {}' && $1"