import pytest
from aws_cdk.assertions import Template
from aws_cdk import App, Stack, aws_iam

from dataall.modules.mlstudio.cdk.mlstudio_stack import SagemakerStudioUserProfile
from dataall.modules.mlstudio.cdk.mlstudio_extension import SageMakerDomainExtension


class MockEnvironmentSageMakerExtension(Stack):
    def environment(self):
        return self._environment

    def get_engine(self):
        return self._db

    def __init__(self, scope, id, env, db, **kwargs):
        super().__init__(
            scope,
            id,
            description='Cloud formation stack of ENVIRONMENT: {}; URI: {}; DESCRIPTION: {}'.format(
                env.label,
                env.environmentUri,
                env.description,
            )[:1024],
            **kwargs,
        )
        self._environment = env
        self._db = db
        self.default_role = aws_iam.Role(self, "DefaultRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Example role..."
        )
        self.group_roles = []
        SageMakerDomainExtension.extent(self)


@pytest.fixture(scope='function', autouse=True)
def patch_methods_sagemaker_studio(mocker, db, sgm_studio, env_fixture, org_fixture):
    mocker.patch(
        'dataall.modules.mlstudio.cdk.mlstudio_stack.SagemakerStudioUserProfile.get_engine',
        return_value=db,
    )
    mocker.patch(
        'dataall.base.aws.sts.SessionHelper.get_delegation_role_name',
        return_value="dataall-pivot-role-name-pytest",
    )
    mocker.patch(
        'dataall.modules.mlstudio.cdk.mlstudio_stack.SagemakerStudioUserProfile.get_target',
        return_value=sgm_studio,
    )
    mocker.patch(
        'dataall.core.stacks.services.runtime_stacks_tagging.TagsUtil.get_engine', return_value=db
    )
    mocker.patch(
        'dataall.core.stacks.services.runtime_stacks_tagging.TagsUtil.get_target',
        return_value=sgm_studio,
    )
    mocker.patch(
        'dataall.core.stacks.services.runtime_stacks_tagging.TagsUtil.get_environment',
        return_value=env_fixture,
    )
    mocker.patch(
        'dataall.core.stacks.services.runtime_stacks_tagging.TagsUtil.get_organization',
        return_value=org_fixture,
    )


@pytest.fixture(scope='function', autouse=True)
def patch_methods_sagemaker_studio_extension(mocker, sgm_studio_domain):
    mocker.patch(
        'dataall.base.aws.sts.SessionHelper.get_cdk_look_up_role_arn',
        return_value="arn:aws:iam::1111111111:role/cdk-hnb659fds-lookup-role-1111111111-eu-west-1",
    )
    mocker.patch(
        'dataall.base.aws.ec2_client.EC2.check_default_vpc_exists',
        return_value=False,
    )
    mocker.patch(
        'dataall.modules.mlstudio.db.mlstudio_repositories.SageMakerStudioRepository.get_sagemaker_studio_domain_by_env_uri',
        return_value=sgm_studio_domain,
    )

def test_resources_sgmstudio_stack_created(sgm_studio):
    app = App()

    # Create the Stack
    stack = SagemakerStudioUserProfile(
        app, 'Domain', target_uri=sgm_studio.sagemakerStudioUserUri
    )

    # Prepare the stack for assertions.
    template = Template.from_stack(stack)

    # Assert that we have created a SageMaker user profile
    # TODO: Add more assertions
    template.resource_count_is("AWS::SageMaker::UserProfile", 1)


def test_resources_sgmstudio_extension_stack_created(db, env_fixture):
    app = App()

    # Create the Stack
    stack = MockEnvironmentSageMakerExtension(
        app, 'SagemakerExtension', env=env_fixture, db=db,
    )

    # Prepare the stack for assertions.
    template = Template.from_stack(stack)

    # Assert that we have created a SageMaker domain
    # TODO: Add more assertions
    template.resource_count_is("AWS::SageMaker::Domain", 1)
