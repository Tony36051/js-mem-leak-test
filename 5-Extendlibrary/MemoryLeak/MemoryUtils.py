#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psutil


def _get_children(father_pid):
    father_process = psutil.Process(father_pid)
    children_processes = father_process.children(recursive=True)
    return children_processes


def get_children_pid(father_pid):
    children_processes = _get_children(father_pid)
    return [x.pid for x in children_processes]


def get_children_mem(father_pid):
    """返回进程实际使用的内存，MB为单位"""
    processes = _get_children(father_pid)
    # rss_mem_in_mb = [float(x.memory_info().rss) / 1024.0 / 1024.0 for x in processes]
    pid_mem = {x.pid: float(x.memory_info().rss) / 1024.0 / 1024.0 for x in processes}
    return pid_mem


if __name__ == '__main__':
    # ps = _get_children(7092)
    rssmems = get_children_mem(7092)
    pids = get_children_pid(7092)
    print(pids)
    print(rssmems)
