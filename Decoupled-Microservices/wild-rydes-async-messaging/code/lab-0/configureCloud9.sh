#!/bin/bash
sudo yum update -y

# Install cf-lint
pip install cfn-lint --use-feature=2020-resolver

#cleanup
#rm -fr ~/environment/wild-rydes-async-messaging/.git
mkdir ~/environment/wild-rydes-async-messaging
mv ~/environment/code/lab-* ~/environment/wild-rydes-async-messaging/
rm -fr ~/environment/code/