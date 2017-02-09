import requests
import unittest
import json

class ATSTestCase(unittest.TestCase):
    def setUp(self):
        self.ats_server='http://54.169.61.44'
    
    def _check_status(self, expected_response, params=None):
        ats_check_url = self.ats_server + '/_astats' if params is None else self.ats_server + '/_astats' + '?' + params
        response = requests.get(ats_check_url)
        #print response
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.text), json.loads(expected_response))
    
    def test_check_ats_switch_status(self):
        headers={'Content-type':'application/json'}
        
        switch_ats_on_url = self.ats_server + '/traffic/switch_config/traffic_on/on'
        switch_ats_off_url = self.ats_server + '/traffic/switch_config/traffic_on/off'
        
        inservice, outOfService = (10,990)
        status_body={"ats":{},"system":{"inf.name":"bond0","inf.speed":20001,"proc.net.dev":"bond0:36668711486876569 134158018858    0    0    0     0          0  10692755 1083682802464555 605401997059    0    0    0     0       0          0","proc.loadavg":"3.40 3.51 3.40 2/1026 561","notAvailable":"%s"}}
        status_body = json.dumps(status_body)
        
        post_ats_status_json_url = self.ats_server + '/traffic/ats_json_config/%s/%s' %(inservice, outOfService)
        
        ats_status_json_response = requests.post(post_ats_status_json_url, data=status_body, headers=headers)
        self.assertEqual(ats_status_json_response.status_code, 200)
        
        # swith ATS on
        requests.get(switch_ats_on_url)
        expected_response = status_body %(inservice)
        self._check_status(expected_response)
        
        # swith ATS off
        requests.get(switch_ats_off_url)
        expected_response = status_body %(outOfService)
        self._check_status(expected_response)
        
    def test_check_ats_switch_status_with_query_params(self):
        headers={'Content-type':'application/json'}
        
        switch_ats_on_url = self.ats_server + '/traffic/switch_config/traffic_on/on'
        switch_ats_off_url = self.ats_server + '/traffic/switch_config/traffic_on/off'
        
        inservice, outOfService = (10,990)
        status_body={"ats":{},"system":{"inf.name":"bond0","inf.speed":200121,"proc.net.dev":"bond0:3666871148332aaaa6876569 134158018858    0    0    0     0          0  10692755 1083682802464555 605401997059    0    0    0     0       0          0","proc.loadavg":"3.40 3.51 3.40 2/1026 561","notAvailable":"%s"}}
        status_body = json.dumps(status_body)
        
        post_ats_status_json_url = self.ats_server + '/traffic/ats_json_config/%s/%s?ab=1&cd=aaaaa' %(inservice, outOfService)
        
        ats_status_json_response = requests.post(post_ats_status_json_url, data=status_body, headers=headers)
        self.assertEqual(ats_status_json_response.status_code, 200)
        
        # swith ATS on
        requests.get(switch_ats_on_url)
        expected_response = status_body %(inservice)
        self._check_status(expected_response)
        
        # swith ATS off
        requests.get(switch_ats_off_url)
        expected_response = status_body %(outOfService)
        self._check_status(expected_response)
        
    def test_check_ats_switch_status_with_more_element_in_json_body(self):
        headers={'Content-type':'application/json'}
        
        switch_ats_on_url = self.ats_server + '/traffic/switch_config/traffic_on/on'
        switch_ats_off_url = self.ats_server + '/traffic/switch_config/traffic_on/off'
        
        inservice, outOfService = (10,990)
        status_body={"ats":{},"system":{"more1":"abc","abd":11111111, "inf.name":"bond0","inf.speed":200121,"proc.net.dev":"bond0:3666871148332aaaa6876569 134158018858    0    0    0     0          0  10692755 1083682802464555 605401997059    0    0    0     0       0          0","proc.loadavg":"3.40 3.51 3.40 2/1026 561","notAvailable":"%s"}}
        status_body = json.dumps(status_body)
        
        post_ats_status_json_url = self.ats_server + '/traffic/ats_json_config/%s/%s?ab=1&cd=aaaaa' %(inservice, outOfService)
        
        ats_status_json_response = requests.post(post_ats_status_json_url, data=status_body, headers=headers)
        self.assertEqual(ats_status_json_response.status_code, 200)
        
        # swith ATS on
        requests.get(switch_ats_on_url)
        expected_response = status_body %(inservice)
        self._check_status(expected_response)
        
        # swith ATS off
        requests.get(switch_ats_off_url)
        expected_response = status_body %(outOfService)
        self._check_status(expected_response)
    
    def test_get_traffic_details(self):
        traffic_details_url = self.ats_server + '/traffic/details?a=1&jj=22j'
        print requests.get(traffic_details_url).text
 
if __name__ == "__main__":
    unittest.main()
