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
    start_spark_cmd = """env SPARK_LOG_DIR={app_log_dir} SPARK_MASTER_PORT={master_port} SPARK_MASTER_WEBUI_PORT={webui_port} {app_root}/sbin/start-master.sh
"""

    process_cmd = format(start_spark_cmd.replace("\n", " "))
    print("Starting Spark master using command: "+process_cmd)
    Execute(process_cmd,
        logoutput=True,
        wait_for_finish=False,
        pid_file=params.pid_file,
        poll_after = 10,
        cwd=format("{app_root}")
    )


  def stop(self, env):
    import params
    env.set_params(params)
    stop_cmd = format("{app_root}/sbin/stop-master.sh --port {master_port}")
    Execute(stop_cmd,
            logoutput=True,
            wait_for_finish=True,
            cwd=format("{app_root}")
    )

  def status(self, env):
    import params
    env.set_params(params)

if __name__ == "__main__":
  Spark_Component().execute()
