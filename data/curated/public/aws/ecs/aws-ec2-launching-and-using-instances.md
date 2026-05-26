---
doc_id: "aws-ec2-launching-and-using-instances"
title: "Amazon EC2 Launching and Using Instances"
source_type: "public"
vendor: "aws"
service: "ec2"
doc_type: "vendor_documentation"
category: "cloud"
tags:
  - "aws"
  - "ec2"
  - "infrastructure"
url: "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/LaunchingAndUsingInstances.md"
---


# Launch an Amazon EC2 instance
<a name="LaunchingAndUsingInstances"></a>

An instance is a virtual server in the AWS Cloud. You launch an instance from an Amazon Machine Image (AMI). The AMI provides the operating system, application server, and applications for your instance.

When you create your AWS account, you can get started with Amazon EC2 for free using the [AWS Free Tier](https://aws.amazon.com/free/). Your Free Tier benefits depend on when you created your AWS account. If your created your AWS account before July 15, 2025 and it's less than 12 months old, you can use the Free Tier to launch and use a `t2.micro` instance for free (in Regions where `t2.micro` is unavailable, you can use a `t3.micro` instance under the Free Tier). You incur charges for your instance or usage that counts against your Free Tier limits while the instance is running, even if it remains idle. For more information, see [Amazon EC2 pricing](https://aws.amazon.com/ec2/pricing/). If you created your AWS account on or after July 15, 2025, you can use `t3.micro`, `t3.small`, `t4g.micro`, `t4g.small`, `c7i-flex.large`, and `m7i-flex.large` instance types for 6 months or until your credits are used up. For more information, see [Free Tier benefits before and after July 15, 2025](ec2-free-tier-usage.md#ec2-free-tier-comparison).

When you launch your instance, you can launch your instance in a subnet that is associated with one of the following resources:
+ An Availability Zone – This option is the default.
+ A Local Zone – To launch an instance in a Local Zone, you must opt in to the Local Zone, and then create a subnet in the zone. For more information, see [Get started with Local Zones](https://docs.aws.amazon.com/local-zones/latest/ug/getting-started.html).
+ A Wavelength Zone – To launch an instance in a Wavelength Zone, you must opt in to the Wavelength Zone, and then create a subnet in the zone. For information about how to launch an instance in a Wavelength Zone, see [Get started with AWS Wavelength](https://docs.aws.amazon.com/wavelength/latest/developerguide/get-started-wavelength.html).
+ An Outpost – To launch an instance in an Outpost, you must create an Outpost. For information about how to create an Outpost, see [Get started with AWS Outposts](https://docs.aws.amazon.com/outposts/latest/userguide/get-started-outposts.html).

After you launch your instance, you can connect to it and use it. To begin, the instance state is `pending`. When the instance state is `running`, the instance has started booting. There might be a short time before you can connect to the instance. Note that bare metal instance types might take longer to launch.

Depending on how you plan to connect to your instance, you might want to make certain configurations while launching your instance. These configurations could include specifying inbound security group rules for certain traffic or associating an instance profile role. For more information on the connection methods you can use to connect and their requirements, see [Connect to your EC2 instance](connect.md).

The instance receives a public DNS name that you can use to contact the instance from the internet. The instance also receives a private DNS name that other instances within the same VPC can use to contact the instance.

When you're finished with an instance, to avoid incurring unnecessary costs, be sure to terminate it. For more information, see [Terminate Amazon EC2 instances](terminating-instances.md).

If you need to launch a large number of instances, use multiple instance types, or use multiple purchasing options such as On-Demand Instance, Reserved Instance, and Spot Instance, consider using EC2 Fleet. For more information, see [EC2 Fleet and Spot Fleet](Fleets.md).

If you want to automate the lifecycle of your instances, including automatic scaling, health checks, and replacement of unhealthy instances, consider using [Amazon EC2 Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html).

The following methods are some of the ways that you can launch an instance.


| Method | Tool | Documentation | 
| --- | --- | --- | 
| Use the launch instance wizard to specify the launch parameters. | Amazon EC2 console | [Launch an EC2 instance using the launch instance wizard in the console](ec2-launch-instance-wizard.md) | 
| Create a launch template and launch the instance from the launch template. | Amazon EC2 console | [Launch EC2 instances using a launch template](launch-instances-from-launch-template.md) | 
| Use an existing instance as the base. | Amazon EC2 console | [Launch an EC2 instance using details from an existing instance](launch-more-like-this.md) | 
| Use an AMI that you purchased from the AWS Marketplace. | Amazon EC2 console | [Launch an Amazon EC2 instance from an AWS Marketplace AMI](launch-marketplace-console.md) | 
| Use an AMI that you specify. | AWS CLI | [Launching, listing, and deleting Amazon EC2 instances in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-services-ec2-instances.html) | 
| Use an AMI that you specify. | AWS Tools for Windows PowerShell | [Launch an Amazon EC2 Instance Using Windows PowerShell](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-ec2-launch.html) | 
| Use EC2 Fleet to provision capacity across different EC2 instance types and Availability Zones, and across On-Demand Instance, Reserved Instance, and Spot Instance purchasing options.  | AWS CLI | [EC2 Fleet and Spot Fleet](Fleets.md) | 
| Use a CloudFormation template to specify an instance. | AWS CloudFormation | [AWS::EC2::Instance](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-instance.html) in the *AWS CloudFormation User Guide* | 
| Use a language-specific AWS SDK to launch an instance. | AWS SDK | [AWS SDK for .NET](https://docs.aws.amazon.com/goto/DotNetSDKV3/ec2-2016-11-15/RunInstances)<br />[AWS SDK for C\+\+](https://docs.aws.amazon.com/goto/SdkForCpp/ec2-2016-11-15/RunInstances)<br />[AWS SDK for Go](https://docs.aws.amazon.com/goto/SdkForGoV1/ec2-2016-11-15/RunInstances)<br />[AWS SDK for Java](https://docs.aws.amazon.com/goto/SdkForJava/ec2-2016-11-15/RunInstances)<br />[AWS SDK for JavaScript](https://docs.aws.amazon.com/goto/AWSJavaScriptSDK/ec2-2016-11-15/RunInstances)<br />[AWS SDK for PHP V3](https://docs.aws.amazon.com/goto/SdkForPHPV3/ec2-2016-11-15/RunInstances)<br />[AWS SDK for Python](https://docs.aws.amazon.com/goto/boto3/ec2-2016-11-15/RunInstances)<br />[AWS SDK for Ruby V3](https://docs.aws.amazon.com/goto/SdkForRubyV3/ec2-2016-11-15/RunInstances) | 