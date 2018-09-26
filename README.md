# xlr-blazemeter-plugin

[![Build Status](https://travis-ci.org/xebialabs-community/xlr-blazemeter-plugin.svg?branch=master)](https://travis-ci.org/xebialabs-community/xlr-blazemeter-plugin)
[![License: MIT][xlr-blazemeter-plugin-license-image]][xlr-blazemeter-plugin-license-url]
[![Github All Releases][xlr-blazemeter-plugin-downloads-image]]()

[xlr-blazemeter-plugin-license-image]: https://img.shields.io/badge/License-MIT-yellow.svg
[xlr-blazemeter-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-blazemeter-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-blazemeter-plugin/total.svg

# XL Release BlazeMeter Plugin

## Preface

This document describes the functionality provide by the `xlr-blazemeter-plugin`

## Overview

This module offers a basic interface to BlazeMeter functionality.

![Test Task View](images/TestTask.png)

## XL Release Scenario

BlazeMeter markets a commercial, self-service load testing platform as a service (PaaS), which is compatible with open-source Apache JMeter, the performance testing framework from the Apache Software Foundation. BlazeMeter comes with a well documented API layer with integration into a number of testing frameworks, incl. JMeter, Gatling, Selenium and Taurus.

### Design decisions on plugin scope

The plugin now supports multiple-scenario / multiple location tests. It will monitor **all** sessions until completion. Finally, it will log the test report summary URL for more information.

## Installation

1. Copy the plugin JAR file into the `SERVER_HOME/plugins` directory of XL Release.
2. Configure your BlazeMeter URL and API Key in Shared Configuration.

## Available Tasks

### Run BlazeMeter Test Case

The **BlazeMeter: Run a Test** task type runs a preconfigured load test. It requires you to specify the following information:

* The Api Key which identifies the user 'id:secret' associated with the project / workspace.
* The Test ID to identify the test.
* The Workspace ID for the tests / reports
* The desired polling interval to check for updates

## References:
* [BlazeMeter REST APIs](https://guide.blazemeter.com/hc/en-us/articles/206732689-BlazeMeter-REST-APIs)
