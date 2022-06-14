from requests import Session
from pprint import pprint

class CloakIT(object):

	def __init__(self):
		self.endpoint = 'https://api.cloakit.pro/v1'

		self.s = Session()
		self.s.headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'User-Agent': 'Mozilla/5.0 ',
		}


	def connect(self,email,password):
		postjson = {'email':email,'password':password}
		r = self.s.post(self.endpoint + '/auth/login', json=postjson).json()
		try:
			self.s.headers['Authorization'] = 'Bearer ' + r['tokens']['access']['token']
			self.uid = r['user']['_id']
		except:
			pass
		return r
   

	def company_list(self):
		postjson = {'userId':self.uid,'filterDate':3,'timeShift':-180}
		r = self.s.post(self.endpoint + '/companies/user', json=postjson).json()
		return r


	def create_company(self, name, white_url, loadTypeWhite, offer_url, loadTypeOffer):
        """
        Create new company
            
        Params
            :loadTypeWhite - 'load' / 'redirect'
            :loadTypeOffer - 'load' / 'redirect'\

        """

		postjson = {
			"name":name,
			"white":white_url,
			"loadTypeWhite":loadTypeWhite, 
			"offer":offer_url,
			"loadTypeOffer":loadTypeOffer,
			"abtest":False,
			"probabilityEqual":True,

			"testOffers":[
				{
					"offer":"",
					"loadTypeOffer":"load",
					"probability":50
				},
				{
					"offer":"",
					"loadTypeOffer":"load",
					"probability":50
				}
			],
			"countries":[],
			"devices":[],
			"referers":"",
			"utmParameters":"",
			"countriesDisallow":False,
			"devicesDisallow":False,
			"referersDisallow":False,
			"utmParametersDisallow":False,
			"proxy":False,
			"ipv6":False,
			"premium":True,
			"blackLists":[],
			"maximumClicksByIp":False,
			"maximumClicksByIpAfter":1,
			"emptyRefererFilter":False,
			"status":"active",
			"dedicatedClicks":30,
			"userId":self.uid
		}
		
		r = self.s.post(self.endpoint + '/companies/' + self.uid, json=postjson).json()
		return r


	def delete_company(self,company_id):
		r = self.s.delete(self.endpoint + '/companies/company/' + company_id).json()
		return r


	def switch_mode(self, company_id):
		r = self.s.get(self.endpoint + '/companies/company/' + company_id).json()

		postjson = r
		if postjson['status'] == 'pause':
			postjson['status'] = 'active'
		else:
			postjson['status'] = 'pause'

		r = self.s.patch(self.endpoint + '/companies/company/' + company_id, json=postjson).json()
		return r


	def get_file(self, company_id):

		file = """
<?php
    error_reporting(0);
    $data = array(
        'companyId' => '""" + company_id +"""', 
        'referrerCF' => $_GET["referrerCF"], 
        'urlCF' => $_GET["urlCF"],
        'QUERY_STRING' => $_SERVER["QUERY_STRING"],
        'HTTP_REFERER' => $_SERVER["HTTP_REFERER"],
        'HTTP_USER_AGENT' => $_SERVER["HTTP_USER_AGENT"],
        'REMOTE_ADDR' => $_SERVER["REMOTE_ADDR"],
        'HTTP_CF_CONNECTING_IP' => $_SERVER["HTTP_CF_CONNECTING_IP"],
        'CF_CONNECTING_IP' => $_SERVER["CF_CONNECTING_IP"],
        'X_FORWARDED_FOR' => $_SERVER["X_FORWARDED_FOR"],
        'TRUE_CLIENT_IP' => $_SERVER["TRUE_CLIENT_IP"],
        );
    $curl = curl_init('http://api.clofilter.com/v1/check');
    curl_setopt($curl, CURLOPT_CUSTOMREQUEST, "POST");
    curl_setopt($curl, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, array(
        'Content-Type: application/json',
        'Content-Length: ' . strlen(json_encode($data))
    ));
    $api = json_decode(curl_exec($curl));
    curl_close($curl);
    $arrContextOptions = array('ssl' => array('verify_peer' => false, 'verify_peer_name' => false), 'http' => array('header' => 'User-Agent: ' . $_SERVER['HTTP_USER_AGENT']));
    if ($api->standartIntegration) {
        if (file_exists($api->simplePage)) {
            if ($api->type == 'load') {
                if ($api->redirectQuery) {
                    header('Location: ?' . $api->redirectQuery);
                } else {
                    require_once($api->simplePage);
                }
            }
            if ($api->type == 'redirect') {
                header('Location: ' . $api->pageWithParams);
            }
            exit;
        }
        if ($api->type == 'load') {
            if ($api->redirectQuery) {
                header('Location: ?' . $api->redirectQuery);
            } else {
                echo str_replace('<head>', '<head><base href="' . $api->simplePage . '" />', file_get_contents($api->simplePage, false, stream_context_create($arrContextOptions)));
            }
        }
        if ($api->type == 'redirect') {
            header('Location: ' . $api->pageWithParams);
        }
        if ($api->type == 'iframe') {
            echo '<iframe src="' . $api->pageWithParams . '" width="100%" height="100%" align="left"></iframe> <style> body { padding: 0; margin: 0; } iframe { margin: 0; padding: 0; border: 0; } </style>';
        }
    } else {
        if ($api->pageType == 'white') {
            echo '';
            exit;
        }
        if (file_exists($api->simplePage)) {
            if ($api->type == 'load') {
                if ($api->redirectQuery) {
                    $api->pageHTML = '<head><meta http-equiv="refresh" content="0; URL=' .$api->originPage . '?' . $api->redirectQuery . '" /></head>';
                } else {
                    $api->pageHTML = file_get_contents($api->simplePage, false, stream_context_create($arrContextOptions));
                }             
            }
            if ($api->type == 'redirect') {
                $api->pageHTML = '<head><meta http-equiv="refresh" content="0; URL=' . $api->pageWithParams . '" /></head>';
            }
        } else {
            if ($api->type == 'load') {
                if ($api->redirectQuery) {
                    $api->pageHTML = '<head><meta http-equiv="refresh" content="0; URL=' .$api->originPage . '?' . $api->redirectQuery . '" /></head>';
                } else {
                    $api->pageHTML = str_replace('<head>', '<head><base href="' . $api->simplePage . '" />', file_get_contents($api->simplePage, false, stream_context_create($arrContextOptions)));
                }
            }
            if ($api->type == 'redirect') {
                $api->pageHTML = '<head><meta http-equiv="refresh" content="0; URL=' . $api->pageWithParams . '" /></head>';
            }
            if ($api->type == 'iframe') {
                $api->pageHTML = '<iframe src="' . $api->pageWithParams . '" width="100%" height="100%" align="left"></iframe> <style> body { padding: 0; margin: 0; } iframe { margin: 0; padding: 0; border: 0; } </style>';
            }
        }
        echo 'document.open();document.write(`' . $api->pageHTML . '`);document.close();';
    }
"""
		return file


if __name__ == "__main__":

	cit = CloakIT()
	info = cit.connect(email='',password='')
	pprint(info)


	pprint(cit.company_list())

	result = cit.create_company(name='test_api', white_url='https://google.com', 
						loadTypeWhite='redirect', 	offer_url='https://rambler.com', 
						loadTypeOffer='redirect')
	
    new_company_id = result['_id']

	cit.delete_company(new_company_id)

	# ans = cit.switch_mode(company_id='629fea827fc11e9cf4fe5aa0')
	# pprint(ans)

	# file = cit.get_file('629fea827fc11e9cf4fe5aa0')
	# print(file)