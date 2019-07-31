evaluate-instances:
	awsie stack.config.yaml configservice start-config-rules-evaluation --config-rule-names cf:ValidateStackSetDeploymentsConfigRule:
	awsie --command stack.config.yaml awsinfo logs -iSs now cf:ValidateStackSetDeploymentsLambdaLogGroup: