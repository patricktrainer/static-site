# How to install docker in Amazon Linux

Created: Jun 13, 2020 12:14 AM
URL: https://www.lewuathe.com/how-to-install-docker-in-amazon-linux.html

![How%20to%20install%20docker%20in%20Amazon%20Linux%208f9de0854c8c438fbc26ad58e24a317b/catch.png](How%20to%20install%20docker%20in%20Amazon%20Linux%208f9de0854c8c438fbc26ad58e24a317b/catch.png)

The usage of Docker is growing more and more. Our daily development tends to depend on the container platform highly. But I found AWS Linux I recently launched does not have Docker engine as default. It is a frustrating situation even I just want to use Docker in AWS environment. Here is the process to install Docker engine in your AWS Linux. That article is written mainly for avoiding my memory lost :)

FYI: The AMI I used in this experiment is `ami-0f9ae750e8274075b`. Amazon Linux 2.

# Install Docker Engine

```
$ sudo yum update -y

$ sudo yum install -y docker

$ sudo service docker start
Starting cgconfig service:                                 [  OK  ]
Starting Docker:                                           [  OK  ]

```

# Add User Group

But you need to prepend `sudo` every time you run docker command. Please don’t forget to add `ec2-user` to `docker` group.

```
$ sudo usermod -a -G docker ec2-user

```

After you log in the instance again, you should be able to run docker command without any difficulty.

Thanks