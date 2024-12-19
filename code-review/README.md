# Research and Engineering Studio (RES)

Research and Engineering Studio (RES) is an AWS supported, open source product that enables IT administrators to provide a web portal for scientists and engineers to run technical computing workloads on AWS. 

- [Documentation](https://docs.aws.amazon.com/res/latest/ug/overview.html)
  - [Deploying in isolated VPC](https://docs.aws.amazon.com/res/latest/ug/prerequisites.html#private-vpc)
- [Source code](https://github.com/aws/res)
- [Demo Installation CFN](https://s3.amazonaws.com/aws-hpc-recipes/main/recipes/res/res_demo_env/assets/res-demo-stack.yaml)
  - [Demo Source Code](https://github.com/aws-samples/aws-hpc-recipes/blob/main/recipes/res/res_demo_env/assets/res-demo-stack.yaml)
  - [Demo components](https://github.com/aws-samples/aws-hpc-recipes/blob/main/recipes/res/)
  - [Demo components documentation](https://github.com/aws-samples/aws-hpc-recipes/tree/main/recipes/res/res_demo_env/docs)
- [Production Install CFN](https://research-engineering-studio-us-east-1.s3.amazonaws.com/releases/latest/ResearchAndEngineeringStudio.template.json)




## Integrated Digital Engineering on AWS (IDEA) 
IDEA is an original project that served as a forked base for RES. NOTE: IDEA is not supported by AWS.

- [IDEA Documentation](https://docs.ide-on-aws.com/idea)
- [IDEA Source Code](https://github.com/cfs-energy/idea)
- [Developer ENv Setup](https://docs.ide-on-aws.com/idea/developer-portal/developer-onboarding)

IDEA has extended documentation , well oriented to the developers and administrators.


# RES Administration Utility

```
# set development mode
export RES_DEV_MODE=true

./res-admin.sh config show --cluster-name res-demo --aws-region eu-west-1 --query "cluster-manager.logging.*" --aws-profile poc-res

./res-admin.sh show-connection-info --cluster-name res-demo --aws-region eu-west-1 --aws-profile poc-res

./res-admin.sh check-cluster-status --cluster-name res-demo --aws-region eu-west-1 --aws-profile poc-res 

(venv) (base) staskh@Stas-MacBook-Pro res % ./res-admin.sh list-modules  --cluster-name res-demo --aws-region eu-west-1 --aws-profile poc-res
+-------------------+----------------------------+-------------------+--------+----------------------------+---------+----------+
| Title             | Name                       | Module ID         | Type   | Stack Name                 | Version | Status   |
+-------------------+----------------------------+-------------------+--------+----------------------------+---------+----------+
| Shared Storage    | shared-storage             | shared-storage    | stack  | res-demo-shared-storage    | 2024.10 | deployed |
| Cluster Manager   | cluster-manager            | cluster-manager   | app    | res-demo-cluster-manager   | 2024.10 | deployed |
| Directory Service | directoryservice           | directoryservice  | stack  | res-demo-directoryservice  | 2024.10 | deployed |
| Identity Provider | identity-provider          | identity-provider | stack  | res-demo-identity-provider | 2024.10 | deployed |
| eVDI              | virtual-desktop-controller | vdc               | app    | res-demo-vdc               | 2024.10 | deployed |
| Cluster           | cluster                    | cluster           | stack  | res-demo-cluster           | 2024.10 | deployed |
| Global Settings   | global-settings            | global-settings   | config | -                          | -       | deployed |
| Bastion Host      | bastion-host               | bastion-host      | stack  | res-demo-bastion-host      | 2024.10 | deployed |
+-------------------+----------------------------+-------------------+--------+----------------------------+---------+----------+


./res-admin.sh list-modules  --cluster-name res-demo --aws-region eu-west-1 


./res-admin.sh cdk diff vdc --cluster-name res-demo --aws-region eu-west-1 --aws-profile poc-res
```

# Demo installation 

[Code](https://github.com/aws-samples/aws-hpc-recipes/blob/main/recipes/res/res_demo_env/assets/res-demo-stack.yaml)


- [res-demo-stack.yaml](https://github.com/aws-samples/aws-hpc-recipes/blob/main/recipes/res/res_demo_env/assets/res-demo-stack.yaml)
  - AdminPassword
  - ServiceAccountPassword
  - Stack: [RESExternal](https://github.com/aws-samples/aws-hpc-recipes/blob/main/recipes/res/res_demo_env/assets/bi.yaml)
  - Stack: [RES](https://research-engineering-studio-us-east-1.s3.amazonaws.com/releases/latest/ResearchAndEngineeringStudio.template.json) (https://github.com/aws/res/blob/mainline/source/idea/app.py#L63) starts after RESExternal completion  
  - Stack: [RESSsoKeycloak - SSO setup with Keycloak](https://github.com/aws-samples/aws-hpc-recipes/blob/main/recipes/res/res_demo_env/assets/res-sso-keycloak.yaml) starts after RES completion
    - KeycloakDataGatherLambdaExecutionRole
    - KeycloakDataGatherHandlerFunction - 'Keycloak Data Gather Handler' gets cognito.UserPoolId, cognito.SAMLRedirectUrl, alb.LoadBalancerDnsName
    - DataGatherCustomResource
    - Stack: [Keycloak](https://github.com/aws-samples/aws-hpc-recipes/blob/main/recipes/res/res_demo_env/assets/keycloak.yaml)
      - KeycloakSecret
      - KeycloakSecurityGroup
      - KeycloakEC2InstanceRole
      - KeycloakEC2InstanceProfile
      - KeycloakEC2Instance - setup EC2 with Keycloak installation
      - 
    - InvokeConfigureSSOLambdaRole
    - InvokeConfigureSSOHandlerFunction
    - InvokeConfigureSSOCustomResource
  - InvokeDeleteSharedStorageSecurityGroupRole
  - InvokeDeleteSharedSecurityGroupHandlerFunction - 'Deletes the shared storage security group when the stack is deleted.'
  - InvokeDeleteSharedStorageSecurityGroup
  - RESPostDeploymentConfiguationFunctionRole
  - RESPostDeploymentConfiguationFunction - update cluster-settings table with 'shared-storage.enable_file_browser': True


