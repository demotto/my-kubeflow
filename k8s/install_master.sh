#!/bin/bash

master=`kubectl get nodes -o wide  | awk '$3=="master"{print $6}'`
token=`kubeadm token create`
ca_cert_hash=`openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'`

echo $master $token $ca_cert_hash
