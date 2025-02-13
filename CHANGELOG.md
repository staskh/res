# Change Log
This file is used to list changes made in each release of Research and Engineering Studio (RES).

2024.12
------

**ENHANCEMENTS**

- Added the ability to activate/deactivate SSH access to the RES environment.
- Added the ability for Active Directory (AD) parameters to now be optional when deploying RES. Parameters can be changed at any time after deployment.
- Added the ability to use Amazon Cognito users to log into RES and deploy Linux Virtual Desktop Infrastructure (VDI) sessions.
- Added the ability to deploy RES infrastructure hosts with RHEL 8 or RHEL 9 in addition to the default Amazon Linux 2 OS.

**CHANGES**

- The listing of filesystems to onboard is now done through RES’s AWS Proxy Lambda function.
- The DynamoDB table creation and default values population for RES has been moved to static CloudFormation stacks.
- The option to Create Software Stack from an existing session has been removed as it was not working as intended.

**BUG FIXES**

- Resolved an issue where the storage root parameter is now properly defined for Ubuntu VDIs allowing access to the DCV upload/download icon in the session UI.
- Resolved an issue with VDI auto stop feature in private VPC configuration. 
- Resolved an issue with failing to launch VDIs for graphic enhanced instance types.
- Resolved an issue where infrastructure AMI building would fail due to an error in the dependencies file.
- Resolved an issue with the PublicAccessConfig parameter in the bootstrap stack causing an error in deployments using restricted Service Control Policies (SCP).

2024.10
------

**ENHANCEMENTS**

- Added the ability to automatically stop or terminate idle sessions to save costs.
- Added the ability to assign projects their own home file system.
- Added the ability for the admins to toggle file browser access on or off for the entire environment.
- Added the ability for the admins to customize DCV permissions for session owners to allow or disallow functions such as copying and pasting from a virtual session.

**CHANGES**

- Added RES base stack to deploy resources required for RES deployment.
- The S3 bucket BlockPublicAccess parameter now defaults to your account level S3 bucket setting.

**BUG FIXES**

- Resolved an issue where Infrastructure AMI building would error out due to a relative directory structure issue.
- Resolved an issue where users were unable to connect to VDI instances running AL2 from the EC2 console.

2024.08
------

**ENHANCEMENTS**

- Added support for mounting S3 buckets and accessing that storage from Linux desktop sessions.
- Added support to create and customize permission profiles
- Added the ability to customize the types of instances available to a RES environment from the UI.
- Added the ability to delete software stacks from UI.
- Added support for the Europe (Stockholm) region.

**CHANGES**

- CentOS 7 and RHEL 7 are no longer supported operating systems for RES desktop sessions.
- Removed the RES metrics stack from the RES installer as it was not in use.

**BUG FIXES**

- Resolved an issue where the Windows software stack AMIs were out of date in Europe (London) region.
- Resolved an issue where Linux virtual desktops may become stuck in the "RESUMING" state on reboot.
- Resolved an issue where RES fails to sync AD users whose SAMAccountName attributes includes capital letters or special characters.
- Resolved an issue that prevented groups with empty spaces or more than 20 characters in their names from successfully being assigned to projects.
- Resolved an issue with VDI sharing where the list of users included only members inside project groups and not individual users that were part of a project.
- Resolved an issue where a VDI sharing sessions could not be deleted after it was shared.
- Resolved an issue where a VDI would not launch in a specified subnet even though a valid subnet ID was provided.

2024.06
------

**BUG FIXES**

- Resolved an issue where permission boundaries were not correctly applied to virtual desktop infrastructure (VDI) policies
- Resolved an issue where RES fails to sync AD users if there are no users in the AD
- Fixed pagination when reading large numbers of RES users from Amazon DynamoDB
- Resolved an issue where RES fails to sync an AD user whose SAMAccountName attribute includes capital letters or special characters
- Resolved an issue where Linux desktop sessions can become stuck in the "RESUMING" state on reboot
- Resolved an issue where RHEL 8 and RHEL 9 desktop sessions end up in an error state if the DisableADJoin input parameter is set to True
- Resolved an issue where Lustre file systems fail to mount when using RHEL 9.4

**ENHANCEMENTS**

- Project owner and project member roles can now be assigned to users and groups a in project. Project owners have the ability to manage user and group access to a project
- Added support for launching virtual desktop sessions with Ubuntu 22.04.3
- The ServiceAccountPassword input parameter now only accepts a secret ARN

2024.04.02
------

**BUG FIXES**

- Fixed a bug where RES Users were given the option to create FSx for Lustre file systems through the UI. RES only supports mounting existing file systems. To create an FSx for Lustre file system see https://docs.aws.amazon.com/fsx/latest/LustreGuide/getting-started.html#getting-started-step1
- Resolved an issue with the IAMPermissionBoundary parameter that prevented the use of GovCloud ARNs.
- Resolved an issue that caused failures when deleting a RES environment in GovCloud.
- Resolved an issue preventing RES installation for accounts with GuardDuty Runtime Monitoring for AWS Fargate enabled.

**ENHANCEMENTS**

- Added support for onboarding FSx for Lustre file systems onto RHEL 9 kernel version 5.14.0-362*.

2024.04.01
------

**BUG FIXES**

- Fixed an issue where Admin users outside the sudoers group were not granted sudo permissions on Linux virtual desktops when DisableADJoin was set to True.
- Resolved an issue that prevented RES infrastructure hosts and Linux virtual desktops from automatically recovering after unexpected reboots during instance warm-up.

2024.04
------

**ENHANCEMENTS**

- Add support for RES Ready AMI.
  - Improve VDI boot times by installing all necessary software in the AMI instead of installing it at EC2 instance launch. This also allows VDIs to run in private subnets with no internet access.
- Add QUIC support for VDIs.
  - The QUIC protocol has better streaming performance in high latency environments. Administrators can toggle this for all VDIs under Session Management → Desktop Settings → General → QUIC.
- Add support for custom VDI Instance launch parameters.
  - Launch parameters include additional IAM policies, security groups and launch scripts. Add these configurations under Advanced Options when creating or editing a project. The settings will apply to all VDIs launched for that project.
- Add support for IAM Permission boundaries.
  - Customers can now specify a permission boundary that will be added to all IAM roles created by the RES environment.
- Add support for deploying RES in an isolated VPC.
- Add support for encrypting communications between RES and AD via LDAPS.
- Add FSx Lustre as a storage option in RES.
- Add support for the Israel (Tel Aviv) region.
- Remove required creation of additional VPC during installation.
- Reduce idle costs.
  - Reduced instance size of some infrastructure instances to reduce base cost of running RES.

**BUG FIXES**

- Add support to auto renew Let’s Encrypt certificates.

2024.01.01
------

**BUG FIXES**

- Upgraded CDK Lambda runtime to nodejs18.x

2024.01
------

**ENHANCEMENTS**

- Add support for snapshots that enable migration between versions of RES.
  - The migration process involves taking a snapshot, deploying the new version (e.g. 2024.01) and applying the snapshot from the previous version (e.g. 2023.11) on the new version. Allows for admins to confirm the new version works before transferring users.
- Add support for private subnets.
  - Enable deployments of RES infrastructure hosts in private subnets with internet access.
  - RES infrastructure hosts refer to the Cluster Manager, Bastion Host, VDC Gateway, VDC Controller, and VDC Broker.
- Deprecation of the analytics stack.
  - Removed required OpenSearch dependency.
  - Reduces RES environment deployment and deletion time by approximately 30 minutes.
- Add support for use of custom Amazon Linux 2 EC2 AMI for RES infrastructure hosts.
  - Enable specifying an AL2 EC2 AMI use for RES infrastructure hosts for users that require specific software or updates installed on their hosts.
  - RES infrastructure hosts refer to the Cluster Manager, Bastion Host, VDC Gateway, VDC Controller, and VDC Broker.
- Add support for ldap_id_mapping “True” in SSSD.
  - Previously the AD sync code required the groups and users to have POSIX attributes uidNumber and gidNumber in order to sync with RES. This conflicted with the IDs generated by SSSD, potentially causing RES users to not be able to access filesystems if they were using SSSD with other systems (e.g. ParallelCluster) .
- Add support for four new regions Asia Pacific (Tokyo), Asia Pacific (Seoul), Canada (Central), Europe (Milan).
- Add ability to add users to projects. Previously only groups could be added to project permissions.

**BUG FIXES**

- Added validation for FSx ONTAP filesystem creation
- Narrowed installation IAM permissions
- Skipped deletion of batteries included related resources
- VDI no longer tries to mount filesystems after removing filesystem from project
