#!/usr/bin/env python
# -*- coding: utf-8 -*-
from openpyxl import Workbook

from MemoryUtils import get_children_pid, get_children_mem


class MemUsageExcel(object):
    def __init__(self):
        '''创建报表
        '''
        self.wb = Workbook()
        self.line_no = 0
        self.chrome_driver_pid = 0
        self.chrome_pids = []

    def record_column_title(self, chrome_driver_pid):
        '''写入列标题
        '''
        self.chrome_pids = get_children_pid(chrome_driver_pid)
        column_title = self.chrome_pids[::] + ['usedJSHeapSize', 'totalJSHeapSize']
        column_title.insert(0, "pid")
        self.line_no = 0
        self.chrome_driver_pid = chrome_driver_pid
        self.wb.active.append(column_title)

    def record_memory_info(self, usedJSHeapSize=0, totalJSHeapSize=0):
        '''写入当前传入的进程的内存占用
        '''
        self.line_no += 1
        pid_mem = get_children_mem(self.chrome_driver_pid)
        chrome_rss = [pid_mem.get(x, 0) for x in self.chrome_pids] + [usedJSHeapSize, totalJSHeapSize]
        chrome_rss.insert(0, self.line_no)
        self.wb.active.append(chrome_rss)

    def save_report(self, save_path):
        '''保存报表，后缀名已经被我焊死了，就是.xlsx，加后缀也没用的
        '''
        self.wb.save(save_path)
        self.wb.close()
