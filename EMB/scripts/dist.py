#!/usr/bin/env python3

EVOMASTER_VERSION = "1.3.1-SNAPSHOT"

import os
import shutil
import platform
from shutil import copy
from shutil import copytree
from subprocess import run
from os.path import expanduser


### Environment variables ###

HOME = expanduser("~")
SCRIPT_LOCATION = os.path.dirname(os.path.realpath(__file__))
PROJ_LOCATION = os.path.abspath(os.path.join(SCRIPT_LOCATION, os.pardir))


JAVA_HOME_8 = os.environ.get('JAVA_HOME_8', '')
if JAVA_HOME_8 == '':
    print("\nERROR: JAVA_HOME_8 environment variable is not defined")
    exit(1)

JAVA_HOME_11 = os.environ.get('JAVA_HOME_11', '')
if JAVA_HOME_11 == '':
    print("\nERROR: JAVA_HOME_11 environment variable is not defined")
    exit(1)


SHELL = platform.system() == 'Windows'


### Prepare "dist" folder ###
dist = os.path.join(PROJ_LOCATION, "dist")

if os.path.exists(dist):
    shutil.rmtree(dist)

os.mkdir(dist)


def callMaven(folder, jdk_home):
    env_vars = os.environ.copy()
    env_vars["JAVA_HOME"] = jdk_home

    mvnres = run(["mvn", "clean", "install", "-DskipTests"], shell=SHELL, cwd=os.path.join(PROJ_LOCATION,folder), env=env_vars)
    mvnres = mvnres.returncode

    if mvnres != 0:
        print("\nERROR: Maven command failed")
        exit(1)

### Building Maven JDK 8 projects ###
def build_jdk_8_maven() :

    folder = "jdk_8_maven"
    callMaven(folder, JAVA_HOME_8)

    # Copy JAR files

    copy(folder+"/cs/graphql/spring-petclinic-graphql/target/petclinic-sut.jar",dist)
    copy(folder+"/em/external/graphql/spring-petclinic-graphql/target/petclinic-evomaster-runner.jar", dist)

    copy(folder+"/cs/graphql/graphql-ncs/target/graphql-ncs-sut.jar",dist)
    copy(folder+"/em/external/graphql/graphql-ncs/target/graphql-ncs-evomaster-runner.jar", dist)

    copy(folder+"/cs/graphql/graphql-scs/target/graphql-scs-sut.jar",dist)
    copy(folder+"/em/external/graphql/graphql-scs/target/graphql-scs-evomaster-runner.jar", dist)



    ind0 = os.environ.get('SUT_LOCATION_IND0', '')
    if ind0 == '':
        print("\nWARN: SUT_LOCATION_IND0 env variable is not defined")
    else:
        copy(ind0, os.path.join(dist, "ind0-sut.jar"))
        copy(folder+"/em/external/rest/ind0/target/ind0-evomaster-runner.jar", dist)

####################
def build_jdk_11_gradle() :

    env_vars = os.environ.copy()
    env_vars["JAVA_HOME"] = JAVA_HOME_11
    folder = "jdk_11_gradle"

    gradleres = run(["gradlew", "build", "-x", "test"], shell=SHELL, cwd=os.path.join(PROJ_LOCATION,folder), env=env_vars)
    gradleres = gradleres.returncode

    if gradleres != 0:
        print("\nERROR: Gradle command failed")
        exit(1)


    # Copy JAR files
    copy(folder+"/cs/graphql/patio-api/build/libs/patio-api-sut.jar", dist)
    copy(folder+"/em/external/graphql/patio-api/build/libs/patio-api-evomaster-runner.jar", dist)



#####################################################################################
### Build the different modules ###
build_jdk_8_maven()
build_jdk_11_gradle()


######################################################################################
### Copy JavaAgent library ###
copy(HOME + "/.m2/repository/org/evomaster/evomaster-client-java-instrumentation/"
   + EVOMASTER_VERSION + "/evomaster-client-java-instrumentation-"
   + EVOMASTER_VERSION + ".jar",
   os.path.join(dist, "evomaster-agent.jar"))


######################################################################################
### Create Zip file with all the SUTs and Drivers ###
zipName = "dist.zip"
if os.path.exists(zipName):
    os.remove(zipName)

print("Creating " + zipName)
shutil.make_archive(base_name=dist, format='zip', root_dir=dist+"/..", base_dir='dist')


######################################################################################
print("\n\nSUCCESS\n\n")
