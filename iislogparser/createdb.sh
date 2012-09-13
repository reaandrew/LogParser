#!/usr/bin/env bash

echo name of script is $0
echo first argument is $1
echo second argument is $2

filename="/tmp/$RANDOM.js"
dbName="$1"
colName="$2"

echo "db.$colName.ensureIndex({'c_ip':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_bytes':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_cookie':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_host':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_method':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_referer':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_uri_query':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_uri_stem':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_user_agent':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_username':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'cs_version':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'day':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'hour':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'minute':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'month':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'sc_bytes':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'s_computername':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'sc_status':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'sc_substatus':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'sc_win32_status':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'second':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'s_ip':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'s_port':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'s_sitename':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'time_taken':1})"  >> "$filename"
echo "db.$colName.ensureIndex({'year':1})"  >> "$filename"

mongo "$dbName" "$filename"
