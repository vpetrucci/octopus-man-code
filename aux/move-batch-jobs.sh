#!/bin/bash

  pid1=`ps ax | grep cpu2006 | awk '{print $1}' `
  for i in $pid1; do taskset -c -p $* $i; done

  pid2=`ps ax | grep run-apps | awk '{print $1}' `
  for i in $pid2; do taskset -c -p $* $i; done
