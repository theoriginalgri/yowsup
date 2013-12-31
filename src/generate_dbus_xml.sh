#!/bin/bash

qdbus com.yowsup /com/yowsup init 123

qdbus com.yowsup /com/yowsup Introspect > com.yowsup.initializer.xml
qdbus com.yowsup /com/yowsup/123/methods Introspect > com.yowsup.methods.xml
qdbus com.yowsup /com/yowsup/123/signals Introspect > com.yowsup.signals.xml

