# coding=utf-8
# -------------------------------------
# Author:      lWX291770
# Created:    2016年12月6日
# -------------------------------------

import win32com.client
import csv


class HttpwatchLibrary(object):
    # 读取url列表
    def get_url_list(self, urlpath):
        urllist = []
        with open(urlpath) as urltxt:
            for url in urltxt.readlines():
                urllist.append(url)
        return urllist

    # 关联已打开浏览器
    def attach_with_broswer(self, title):
        self.control = win32com.client.Dispatch('HttpWatch.Controller')
        self.plugin = self.control.AttachByTitle(title)
        self.plugin.Log.EnableFilter(False)

    # 开始记录数据
    def begin_record(self):
        self.plugin.Record()

    # 停止记录数据
    def stop_record(self):
        self.plugin.stop()

    # 把结果写入csv文件
    def write_record_to_csv(self, urllist, resultpath):
        # 遍历所有record存入列表
        records = []
        record = []
        for page in self.plugin.Log.Pages:
            if page.Title:
                summary = page.Entries.summary
                pageEvent = page.Events
                summaryTime = summary.TimingSummaries

                # 开始记录数据
                record.append(pageEvent.HTTPLoad.Value) # Total time to load page (secs)
                record.append(summary.BytesReceived) # Number of bytes received on network
                record.append(summary.BytesSent) # Number of bytes sent on network
                record.append(summary.CompressionSavedBytes) # HTTP compression saving (bytes)
                record.append(summaryTime.TTFB.Maximum) # TTFB_Maximum
                record.append(summaryTime.TTFB.Total) # TTFB_Total
                record.append(summaryTime.Receive.Total) # Receive Total
                record.append(summaryTime.Receive.Maximum) # Receive Maximum
                record.append(summaryTime.Network.Total) # SummaryTime of Network_Total
                record.append(summaryTime.Network.Maximum) # SummaryTime of Network_Maximum
                record.append(pageEvent.DOMLoad.Value) # PageEvents DOMLoad
                record.append(pageEvent.PageLoad.Value) # PageEvents PageLoad
                records.append(record)
                record = []
        print 'First Records', records

        # 在records列表的第一位插入url
        print urllist
        for i in range(len(urllist)):
            urllist[i] = urllist[i].replace('\n', '')
        map((lambda x, y: y.insert(0, x)), urllist, records)
        print 'URLLIST END'

        print resultpath
        with file(resultpath, 'wb') as resultfile:
            resultWriter = csv.writer(resultfile)
            filehead = ['url',
                        'Total time to load page (secs)',
                        'Number of bytes received on network',
                        'Number of bytes sent on network',
                        'HTTP compression saving (bytes)',
                        'TTFB_Maximum',
                        'TTFB_Total',
                        'Receive Total',
                        'Receive Maximum',
                        'SummaryTime of Network_Total',
                        'SummaryTime of Network_Maximum',
                        'PageEvents DOMLoad',
                        'PageEvents PageLoad']
            records.insert(0, filehead)
            print "records:", records
            for line in records:
                print 'line:', line
                resultWriter.writerow(line)
