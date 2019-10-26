#!/bin/bash

master=`kubectl get nodes -o wide  | awk '$3=="master"{print $6}'`
token=`kubeadm token create`
ca_cert_hash=`openssl x509 -pubkey -in /etc/kubernetes/pki/ca.crt | openssl rsa -pubin -outform der 2>/dev/null | openssl dgst -sha256 -hex | sed 's/^.* //'`


CMD="kubeadm join $master:6443 --token $token --discovery-token-ca-cert-hash sha256:$ca_cert_hash"
echo $CMD
