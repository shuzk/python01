#!/bin/bash
mysql -uroot -pmysql -h 127.0.0.1 meiduo_mall < ./areas.sql
mysql -uroot -pmysql -h 127.0.0.1 meiduo_mall < ./goods_data.sql
