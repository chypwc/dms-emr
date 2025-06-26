#!/bin/bash
set -e

# Unzip .gz files into /data (mounted volume, writable)
gunzip -c /data/order_products__prior.csv.gz > /data/order_products__prior.csv
gunzip -c /data/order_products__train.csv.gz > /data/order_products__train.csv
