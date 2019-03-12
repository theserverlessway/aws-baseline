'use strict';
const AWS = require('aws-sdk');
const response = require('cfn-response');
const iam = new AWS.IAM({apiVersion: '2010-05-08'});
exports.handler = (event, context, cb) => {
    console.log(`Invoke: ${JSON.stringify(event)}`);
    const done = (err) => {
        if (err) {
            console.log(`Error: ${JSON.stringify(err)}`);
            response.send(event, context, response.FAILED, {});
        } else {
            response.send(event, context, response.SUCCESS, {});
        }
    };
    if (event.RequestType === 'Delete') {
        iam.deleteAccountPasswordPolicy({}, done);
    } else if (event.RequestType === 'Create' || event.RequestType === 'Update') {
        iam.updateAccountPasswordPolicy({
            AllowUsersToChangePassword: Boolean(event.ResourceProperties.AllowUsersToChangePassword),
            HardExpiry: Boolean(event.ResourceProperties.HardExpiry),
            MaxPasswordAge: event.ResourceProperties.MaxPasswordAge,
            MinimumPasswordLength: event.ResourceProperties.MinimumPasswordLength,
            PasswordReusePrevention: event.ResourceProperties.PasswordReusePrevention,
            RequireLowercaseCharacters: Boolean(event.ResourceProperties.RequireLowercaseCharacters),
            RequireNumbers: Boolean(event.ResourceProperties.RequireNumbers),
            RequireSymbols: Boolean(event.ResourceProperties.RequireSymbols),
            RequireUppercaseCharacters: Boolean(event.ResourceProperties.RequireUppercaseCharacters),
        }, done);
    } else {
        cb(new Error(`unsupported RequestType: ${event.RequestType}`));
    }
};