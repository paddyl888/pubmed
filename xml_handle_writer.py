#!/bin/usr/python


def save_xml(handle):

    data = handle.read()
    handle.close()
    out_handle = open('data.xml', 'w')
    out_handle.write(data)
    out_handle.close()
