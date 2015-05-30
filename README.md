Spark on YARN via Slider
========

Spark on Slider - Slider package for deploying Spark as a service on a YARN cluster.

Getting Started
========

Follow the instructions for getting started with Slider:
http://slider.incubator.apache.org/docs/getting_started.html

Be sure to add the `$SLIDER_HOME/bin` directory to your path.

Also, make sure your `conf/slider-client.xml` file sets the ResourceManager address so you don't have to
include the `--manager` parameter with every slider command.

```
  <property>
    <name>yarn.resourcemanager.address</name>
    <value>localhost:8032</value>
  </property>
```

Throughout these instructions, `$PROJECT_HOME` refers to the directory where you cloned this project.

**1) Download a Spark distribution archive (tgz)**

Download the latest Spark distribution from: https://spark.apache.org/downloads.html

Once downloaded, move the distribution archive to `$PROJECT_HOME/package/files/spark.tgz`

The distribution archive must be named `spark.tgz` as the `metainfo.xml` file references this path.

**2) Create the spark-on-yarn.zip deployment package**

Create the Slider package using zip:

```
zip -r spark-on-yarn.zip metainfo.xml package/
```

**3) Install the package on HDFS**

```
slider install-package --replacepkg --name spark --package $PROJECT_HOME/spark-on-yarn.zip
```

**4) Configure environment specific settings**

Edit the `$PROJECT_HOME/appConfig-default.json`. At a minimum, you'll need to update the following settings
to match your environment:

```
    "site.global.app_root": "${AGENT_WORK_ROOT}/app/install/spark-1.3.1-bin-hadoop2.6",
```

Review the other settings in this file to verify they are correct for your environment.

**5) Configure the number of Spark worker nodes to deploy**

Edit `yarn.component.instances` in `resources-default.json` to set the number of Spark worker nodes to deploy across your cluster.

**6) Deploy Spark on YARN**

```
slider create spark --template $PROJECT_HOME/appConfig-default.json \
  --resources $PROJECT_HOME/resources-default.json
```

**7) Get the location of the Spark Master and the Spark Master Web UI from the YARN registry**

```
slider registry --getconf quicklinks --name spark --format json
```

NOTE: The registry command requires using Java 7 as there's a bug in Slider that prevents the registry command
from working correctly, see: https://issues.apache.org/jira/browse/SLIDER-878

**8) Use the master location returned in the previous step to submit spark jobs, for example:

spark-shell --master spark://c6401.ambari.apache.org:51636

Acknowledgements
========
This work started from the Solr-on-Slider package at https://github.com/LucidWorks/solr-slider and the HBase-on-Slider package.

TODO
========
Better health monitoring and status reporting for the master and slave processes
