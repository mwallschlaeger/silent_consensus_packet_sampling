#!/bin/bash

OLD=$1
NEW=$2

tshark -r $OLD -w $NEW -F libpcap
