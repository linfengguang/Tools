#-*- coding=UTF-8 -*-

import sys,struct,os

class _analysis_packet(object):
    '''读取一个数据报文，打印报文头部字段内容，计算并判断校验和是否正确
    '''
    def _byte_to_hex(self,bins):
        """
        Convert a byte string to it's hex string representation e.g. for output.(网上获取代码，需要重新分析代码方法)
        """
        return ''.join(["%02X" % x for x in bins]).strip()

    def _open_packet(self,cap_filename,result_filename):
        pcap = open(cap_filename,'rb')
        result_txt = open(result_filename,'w')
        data = pcap.read()

        pcap_header = {}

        pcap_header['dmac'] = self._byte_to_hex(data[40:46])
        pcap_header['smac'] = self._byte_to_hex(data[46:52])
        pcap_header['type'] = self._byte_to_hex(data[52:54])

        pcap_header['version&header_length'] = self._byte_to_hex(data[54:55])
        pcap_header['dscp'] = self._byte_to_hex(data[55:56])
        pcap_header['total_length'] = self._byte_to_hex(data[56:58])
        pcap_header['identification'] = self._byte_to_hex(data[58:60])
        pcap_header['frag&offset'] = self._byte_to_hex(data[60:62])
        pcap_header['ttl'] = self._byte_to_hex(data[62:63])
        pcap_header['protocol'] = self._byte_to_hex(data[63:64])
        pcap_header['ip_checksum'] = self._byte_to_hex(data[64:66])
        pcap_header['sip'] = self._byte_to_hex(data[66:70])
        pcap_header['dip'] = self._byte_to_hex(data[70:74])

        pcap_header['udp_sport'] = self._byte_to_hex(data[74:76])
        pcap_header['udp_dport'] = self._byte_to_hex(data[76:78])
        pcap_header['udp_length'] = self._byte_to_hex(data[78:80])
        pcap_header['udp_checksum'] = self._byte_to_hex(data[80:82])

        print (pcap_header)

        result_txt.write('数据包头部内容：' + '\n')
        for key in pcap_header.keys():
            result_txt.write(key + " : " + repr(pcap_header[key]) + '\n')

    def _count_checksum(self,res):
        pass

    def _compare_checksum(self):
        pass

    def _output_result(self):
        pass

if __name__ == "__main__":
    print ("debugging...")
    test = _analysis_packet()
    test._open_packet('udp2.pcap','packetheader.txt')





