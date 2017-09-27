#!/bin/bash
export SOLR_Language_Dir=data/lang
export SOLR_HOME=data

solr start -V -f -m 512m -s $SOLR_HOME -Dsolr.allow.unsafe.resourceloading=true -Dsolr.languageDir=$SOLR_Language_Dir
#bin/solr start -V -f -m 512m -s $SOLR_HOME -Dsolr.allow.unsafe.resourceloading=true -Dsolr.languageDir=$SOLR_HOME/lang
