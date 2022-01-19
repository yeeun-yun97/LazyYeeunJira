from jira import JIRA
import os
import json
import datetime
import webbrowser


'''Json'''
def saveJson(fileName):
	with open(fileName,'w',encoding='UTF-8') as f:
		f.write(json.dumps(json_object, ensure_ascii=False))

def openJson(fileName):
	with open(fileName,encoding='UTF-8') as f:
		return json.load(f)


json_object=openJson('auth.json')
JIRA_URL=json_object['jiraUrl']
JIRA_PREFIX=json_object['jiraPrefix']
USER_EMAIL=json_object['userEmail']
API_TOKEN=json_object['apiToken']
json_object=openJson('data.json')


'''jira'''
def createMeta(summary,parent,type):
	return jira.create_issue(
		project=JIRA_PREFIX, 
		parent={'key': f'{JIRA_PREFIX}-{parent}'},
		issuetype={'name': type},
		summary=summary,
		assignee=USER_EMAIL
		)

def createSubTask(summary,parent):
	return createMeta(summary,parent,'Sub-type')

def createIssue(summary,parent):
	return createMeta(summary,parent,'Story')


def getStringDate(date):
	return date.strftime('%Y-%m-%d')

def createSprint(name):
	return jira.create_sprint(
		name=name,
		board_id=1,
		startDate=getStringDate(datetime.datetime.now()),
		endDate=getStringDate(datetime.datetime.now()+datetime.timedelta(days=6))
		)

def addIssuesToSprint(arr):
	sprintId=json_object['sprintId']
	os.system(sprintId)
	jira.add_issues_to_sprint(sprint_id=sprintId, issue_keys=arr)

#connect jira
jira=JIRA(server=JIRA_URL,basic_auth=(USER_EMAIL,API_TOKEN))

'''function'''
def monday():
	json_object['weekCount']=json_object['weekCount']+1
	num=json_object['weekCount']
	SPRINT_ID=createSprint(json_object['sprintDefaultName'].format(num))

def everyday():
	json_object['dayCount']=json_object['dayCount']+1
	
	num=json_object['dayCount']
	today=getStringDate(datetime.datetime.now())
	issue0= createIssue(json_object['storyDefaultNames'][0].format(num,today),39)
	issue1= createIssue(json_object['storyDefaultNames'][1].format(num,today),45)
	issue2= createIssue(json_object['storyDefaultNames'][2].format(num,today),51)
	
	arr=[issue0.key,issue1.key,issue2.key]

#monday()
everyday()
saveJson()
webbrowser.open("{}/browse/{}".format(JIRA_URL,JIRA_PREFIX))