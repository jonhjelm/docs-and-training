#!/bin/bash

#if [[ -v REMOTE_HOST ]]
#then
#cat spyne_flask.nginx_template | sed "s|REMOTE_HOST|$REMOTE_HOST|" > /etc/nginx/sites-enabled/spyne_flask.nginx
#fi

#cat spyne_flask.nginx_template | sed "s|REMOTE_HOST|srv.hetcomp.org|" > /etc/nginx/sites-enabled/spyne_flask.nginx
#cp spyne_flask.nginx_template /etc/nginx/sites-enabled/spyne_flask.nginx

#/etc/init.d/nginx start
#echo here
python CalculatorService.py |& tee -a /var/log/CalculatorService.py

