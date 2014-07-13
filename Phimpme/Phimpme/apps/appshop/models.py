#!/usr/bin/env python
# coding:utf-8

import thread, time, os
from django.db import models
from Phimpme.apps.orders.models import order
from django.core.context_processors import request
from django.contrib.auth.decorators import login_required, permission_required
# Create your models here.

class appshop_paramters(models.Model):
    key = models.CharField(max_length=256)
    value = models.CharField(max_length=256)


def appshop_get_value(key):
    """
    """
    if key is None :
        raise Exception('key is None')
    else :
        param = appshop_paramters.objects.get(key=key)
        if param is None:
            raise Exception('key is not defined')
        else:
           return param.value


def generate_thread(id, t):
    """
    TODO:FIXME: porting real generate interface
        call generate(app_name, app_logo, enables) instead
    """
    #time.sleep(t)
    o = order.objects.get(id=id)
    if o is None:
        raise Exceptions('order %s be not found' % (id))
    else:
        if o.order_is_rebuild == True:
            o.order_status = 3
        else:
            o.order_status = 2
        # generator script
        web_path = '/static/output_path/' + str(id) + '.apk'
        abs_path = os.path.abspath('Phimpme' + web_path)
        from gen_script import generate
        generate(order_id = id, output_path = abs_path, app_name = o.order_appname, app_logo = None, enables = eval(o.order_fetures))

        o.order_output_file = web_path
        o.save()
    thread.exit_thread()

@login_required
def appshop_generate(request, o):
    """
    """
    if order is None:
        return False
    else :
        thread.start_new_thread(generate_thread, (o.id, 30))
        return True
