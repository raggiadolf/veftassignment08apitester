import requests
import json
import sys

if len(sys.argv) < 4:
	print "Proper usage: " + sys.argv[0] + " 'portno' 'admintoken' 'usertoken'"
	sys.exit()

class Company(object):
	def __init__(self, name, descr, pl):
		self.name = name
		self.description = descr
		self.punchcard_lifetime = pl

	def __str__(self):
		return str(self.__dict__)

	def __eq__(self, other):
		return self.__dict__ == other.__dict__


haskolabudin = Company(u'Haskolabudin', u'10-11 in disguise', 7)
port = sys.argv[1]
url = 'http://localhost:' + port
ADMIN_TOKEN = sys.argv[2]
USER_TOKEN = sys.argv[3]

def checkEmptyCompanyDocument(url):
	r = requests.get(url)
	assert len(r.json()) is 0, "Does not return an empty list when empty using /api/companies"
	print "Responds correctly when sending GET to /api/companies with empty database"

def insertCompany(url, payload):
	token = {'admin_token' : ADMIN_TOKEN}
	bad_r_auth = requests.post(url, json=payload.__dict__)
	assert bad_r_auth.status_code == 401, "Does not return 401 when user is not authenticated using /api/companies"
	print "Responds correctly with 401 when posting to /api/companies without proper authentication"

	badCompany = {'name' : 'teogkaffi', 'description' : 'teogkaffi'}
	bad_r_pre = requests.post(url, json=badCompany)
	assert bad_r_pre.status_code == 412, "Does not return 412 when payload is invalid using /api/companies"
	print "Responds correctly with 412 when posting to /api/company/ with invalid payload"
	
	ok_r = requests.post(url, json=payload.__dict__, headers=token)
	assert ok_r.status_code == 201, "Does not return 201 after creating a company using /api/companies"
	print "Responds correctly with 201 when posting successfully to /api/companies"
	assert len(ok_r.json()) is not 0, "Does not return a json object after creating a company using /api/companies"
	print "Responds correctly with an object after posting successfully to /api/companies"

	getc_r = requests.get(url + '/' + ok_r.json()['company_id'])
	assert getc_r.status_code == 200, "Does not return 200 after querying for a valid company from /api/companies/:company_id"
	print "Responds correctly with 200 after querying for a valid company from /api/companies/" + ok_r.json()['company_id']

	cname = getc_r.json()[0]['name']
	cdescr = getc_r.json()[0]['description']
	cpl = getc_r.json()[0]['punchcard_lifetime']
	newComp = Company(cname, cdescr, cpl)

	assert newComp == haskolabudin, "Does not return a valid company from /api/companies/:company_id"
	print "Responds with the correct object after posting a valid company to /api/companies/" + ok_r.json()['company_id']
	return ok_r.json()

def checkCompanyDocumentWithOneDocument(url):
	r = requests.get(url)
	assert len(r.json()) is 1, "Does not return the correct amount of documents using /api/documents. Should be: 1, is: " + str(len(r.json()))
	print "Responds with the correct amount of documents from GET to /api/documents"

def checkPunchcard(url):
	token = {'token' : USER_TOKEN}
	badToken = {'token' : 'badtoken'}
	bad_r_auth = requests.post(url, headers=badToken)
	assert bad_r_auth.status_code == 401, "Does not return 401 if the user does not have a valid token using /punchcard/:company_id"
	print "Responds correctly with 401 when posting to /punchcard/:company_id with an invalid token"

	ok_r = requests.post(url, headers=token)
	assert ok_r.status_code == 201, "Does not return 201 if the punchcard was posted successfully using /punchcard/" + url.rpartition('/')[2]
	print "Responds correctly with 201 after successfully posting a punchcard to /punchcard/:company_id"
	assert len(ok_r.json()) is not 0, "Does not return an id if the punchcard was posted successfully using /punchcard/" + url.rpartition('/')[2]
	print "Responds correctly with a json object after successfully posting to /punchcard/:company_id"
	bad_r_samep = requests.post(url, headers=token)
	assert bad_r_samep.status_code == 409, "Does not return 409 if the same punchcard is posted twice using /punchcard/" + url.rpartition('/')[2]
	print "Responds correctly with 409 if the same punchcard is posted twice using /punchcard/:company_id"

checkEmptyCompanyDocument(url + '/api/companies')
companyID = insertCompany(url + '/api/companies', haskolabudin)
checkCompanyDocumentWithOneDocument(url + '/api/companies')
checkPunchcard(url + '/punchcard/' + companyID['company_id'])




