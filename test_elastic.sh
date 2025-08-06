#!/bin/bash

curl -X POST "https://172.200.58.63:9200/_search" \
  -H "Authorization: ApiKey bDhLS3haY0J5emY3NTkxU0s5ekQ6OW4tTkduaUpHb0VFQkhPLVh3blV1dw==" \
  -H "Content-Type: application/json" \
  --data '{"query":{"match_all":{}},"size":1}' \
  --cacert /home/shtlp_0020/Downloads/elastic.crt
