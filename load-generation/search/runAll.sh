#!/bin/sh

# CloudSuite1.0 Benchmark Suite
# Copyright (c) 2011, Parallel Systems Architecture Lab, EPFL
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#   * Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#   * Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in 
#     the documentation and/or other materials provided with the distribution.
#
#   * Neither the name of the Parallel Systems Architecture Laboratory, 
#     EPFL nor the names of its contributors may be used to endorse or 
#     promote products derived from this software without specific prior 
#     written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# PARALLEL SYSTEMS ARCHITECTURE LABORATORY, EPFL BE LIABLE FOR ANY 
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE 
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER 
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN 
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Stavros Volos, Vukasin Stefanovic

CLASSPATH=$FABAN_HOME/lib/fabanagents.jar:$FABAN_HOME/lib/fabancommon.jar:$FABAN_HOME/lib/fabandriver.jar:$JAVA_HOME/lib/tools.jar:$FABAN_HOME/search/build/lib/search.jar
export CLASSPATH

java  -Djava.security.policy=config/security/driver.policy com.sun.faban.common.RegistryImpl & pid=$!
sleep 3
java -Xmx10g -Xms10g -Djava.security.policy=config/security/driver.policy com.sun.faban.driver.engine.AgentImpl SearchDriver 1 localhost & pid1=$! 
sleep 3


ssh n129 java -classpath $FABAN_HOME/lib/fabanagents.jar:$FABAN_HOME/lib/fabancommon.jar:$FABAN_HOME/lib/fabandriver.jar:$JAVA_HOME/lib/tools.jar:$FABAN_HOME/search/build/lib/search.jar -Xmx10g -Xms10g -Djava.security.policy=$FABAN_HOME/search/config/security/driver.policy com.sun.faban.driver.engine.AgentImpl SearchDriver 2 n136 & ssh n136 pid2=$! 
ssh n129 sleep 3

ssh n121 java -classpath $FABAN_HOME/lib/fabanagents.jar:$FABAN_HOME/lib/fabancommon.jar:$FABAN_HOME/lib/fabandriver.jar:$JAVA_HOME/lib/tools.jar:$FABAN_HOME/search/build/lib/search.jar -Xmx10g -Xms10g -Djava.security.policy=$FABAN_HOME/search/config/security/driver.policy com.sun.faban.driver.engine.AgentImpl SearchDriver 4 n136 & ssh n121 pid4=$! 
ssh n121 sleep 3
ssh n130 java -classpath $FABAN_HOME/lib/fabanagents.jar:$FABAN_HOME/lib/fabancommon.jar:$FABAN_HOME/lib/fabandriver.jar:$JAVA_HOME/lib/tools.jar:$FABAN_HOME/search/build/lib/search.jar -Xmx10g -Xms10g -Djava.security.policy=$FABAN_HOME/search/config/security/driver.policy com.sun.faban.driver.engine.AgentImpl SearchDriver 5 n136 & ssh n130 pid5=$! 
ssh n130 sleep 3
ssh n131 java -classpath $FABAN_HOME/lib/fabanagents.jar:$FABAN_HOME/lib/fabancommon.jar:$FABAN_HOME/lib/fabandriver.jar:$JAVA_HOME/lib/tools.jar:$FABAN_HOME/search/build/lib/search.jar -Xmx10g -Xms10g -Djava.security.policy=$FABAN_HOME/search/config/security/driver.policy com.sun.faban.driver.engine.AgentImpl SearchDriver 6 n136 & ssh n131 pid6=$! 
ssh n131 sleep 3

java -Xmx10g -Xms10g -Djava.security.policy=config/security/driver.policy -Dbenchmark.config=deploy/run.xml com.sun.faban.driver.engine.MasterImpl


kill $pid
kill $pid1
ssh n129 kill -9 `ssh n129 jps | grep AgentImpl | cut -d " " -f 1`
ssh n121 kill -9 `ssh n121 jps | grep AgentImpl | cut -d " " -f 1`
ssh n130 kill -9 `ssh n130 jps | grep AgentImpl | cut -d " " -f 1`
ssh n131 kill -9 `ssh n131 jps | grep AgentImpl | cut -d " " -f 1`
