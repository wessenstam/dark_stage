#!/bin/bash
# Script to kill the container
pid_super=$(ps  -e | grep supervisord | tr -s " " ";"|cut -d ";" -f 2)
kill -9 $pid_super