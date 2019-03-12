deploy:
	deployto

evaluate-instances: deploy
	awsie validate-stack-set-deployments configservice start-config-rules-evaluation --config-rule-names cf:ValidateStackSetDeploymentsConfigRule:
	awsie --command validate-stack-set-deployments awsinfo logs -s now cf:ValidateStackSetDeploymentsLambdaLogGroup:

evaluate-stacksets: deploy
	awsie validate-stack-set-deployments configservice start-config-rules-evaluation --config-rule-names cf:ValidateStackSetUpToDateConfigRule:
	awsie --command validate-stack-set-deployments awsinfo logs -s now cf:ValidateStackSetUpToDateLambdaLogGroup:
