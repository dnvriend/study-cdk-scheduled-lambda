import os
import aws_cdk as cdk
from aws_cdk import Stack
from aws_cdk import aws_logs as logs
import dotenv

dotenv.load_dotenv()

class ScheduledLambdaStack(Stack):
    def __init__(self, scope: cdk.App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create, deploy, and configure the lambda function, including the log group and retention; no need to create a 
        # cloudwatch log group or policy and role
        scheduled_lambda = cdk.aws_lambda.Function(
            self,
            "scheduled_lambda",
            runtime=cdk.aws_lambda.Runtime.PYTHON_3_12,
            handler="lambda.handler",
            code=cdk.aws_lambda.Code.from_asset("lambda"),  # Assumes your Lambda code is in a 'lambda' directory
            timeout=cdk.Duration.minutes(1),
            environment={
                "LOG_LEVEL": "INFO",
            },
            log_retention=logs.RetentionDays.ONE_WEEK
        )

        # create aws events rule
        events_rule = cdk.aws_events.Rule(
            self,
            "scheduled_lambda_event_rule",
            schedule=cdk.aws_events.Schedule.rate(cdk.Duration.minutes(1)),
        )

        # Add the Lambda function as a target for the CloudWatch Event Rule
        events_rule.add_target(cdk.aws_events_targets.LambdaFunction(scheduled_lambda))


app = cdk.App()
# set the environment
env = cdk.Environment(account=os.getenv('AWS_ACCOUNT'), region=os.getenv('AWS_REGION'))
# create the stack
scheduled_lambda_stack = ScheduledLambdaStack(app, "ScheduledLambdaStack", env=env)
# synthesize the CFN template
app.synth()
