#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
import random
import os
import sys
from resource_management import *

class Spark_Component(Script):

  def install(self, env):
    self.install_packages(env)

  def configure(self, env):
    import params
    env.set_params(params)

  def start(self, env):
    import params
    env.set_params(params)
    self.configure(env)

    worker_id = random.randint(1, 10000)
    pid_file = format("{app_pid_dir}/spark-yarn-org.apache.spark.deploy.worker.Worker-{worker_id}.pid")
    start_spark_cmd = """env SPARK_PID_DIR={app_pid_dir} SPARK_LOG_DIR={app_log_dir} {app_root}/sbin/start-slave.sh {worker_id} spark://{master_host}:{master_port}
"""

    process_cmd = format(start_spark_cmd.replace("\n", " "))
    print("Starting Spark slave using command: "+process_cmd)
    Execute(process_cmd,
        logoutput=True,
        wait_for_finish=False,
        pid_file=pid_file,
        poll_after = 10,
        cwd=format("{app_root}")
    )


  def stop(self, env):
    import params
    env.set_params(params)
    stop_cmd = format("{app_root}/sbin/stop-slave.sh")
    Execute(stop_cmd,
            logoutput=True,
            wait_for_finish=True,
            cwd=format("{app_root}")
    )

  def status(self, env):
    import params
    env.set_params(params)
    # check the first pid file in this directory
    for item in os.listdir(params.app_pid_dir):
        pid_file = os.path.join(params.app_pid_dir, item)
        check_process_status(pid_file)
        break

if __name__ == "__main__":
  Spark_Component().execute()
