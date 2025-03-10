import { gql } from 'apollo-boost';

export const getDataset = (datasetUri) => ({
  variables: {
    datasetUri
  },
  query: gql`
    query GetDataset($datasetUri: String!) {
      getDataset(datasetUri: $datasetUri) {
        datasetUri
        owner
        description
        label
        name
        region
        created
        imported
        userRoleForDataset
        SamlAdminGroupName
        AwsAccountId
        KmsAlias
        S3BucketName
        GlueDatabaseName
        tags
        businessOwnerEmail
        stewards
        IAMDatasetAdminRoleArn
        businessOwnerDelegationEmails
        stack {
          stack
          status
          stackUri
          targetUri
          accountid
          region
          stackid
          link
          outputs
          resources
        }
        topics
        language
        confidentiality
        organization {
          organizationUri
          label
        }
        terms {
          count
          nodes {
            __typename
            ... on Term {
              nodeUri
              path
              label
            }
          }
        }
        environment {
          environmentUri
          label
          region
          subscriptionsEnabled
          subscriptionsProducersTopicImported
          subscriptionsConsumersTopicImported
          subscriptionsConsumersTopicName
          subscriptionsProducersTopicName
          organization {
            organizationUri
            label
          }
        }
        statistics {
          tables
          locations
          upvotes
        }
      }
    }
  `
});
