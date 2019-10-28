#!/bin/bash

mkdir -p /data1/k8s_nfs/katib-mysql
mkdir -p /data1/k8s_nfs/metadata-mysql
mkdir -p /data1/k8s_nfs/minio-pv
mkdir -p /data1/k8s_nfs/mysql-pv
base_dir=`pwd`
kubectl apply -f ${base_dir}/pv.yaml
