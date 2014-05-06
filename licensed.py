#!/usr/bin/python

try:
  from lxml import etree
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
        except ImportError:
          print("Failed to import ElementTree from any known place")

import hashlib
import json

class mklicense(object):

	def __init__(self,target, assigner, assignee):
		self.target = target
		self.assigner = assigner
		self.assignee = assignee

	def simpleAction(self, action):
		return simpleAction(target=self.target, assigner=self.assigner, assignee=self.assignee, action=action)

	def simpleGeographic(self, geography, operator="http://www.w3.org/ns/odrl/2/eq"):
		return simpleGeographic(target=self.target, assigner=self.assigner, assignee=self.assignee, geography=geography, operator=operator)

	def simpleTimePeriod(self, timeperiod, operator="http://www.w3.org/ns/odrl/2/lt"):
		return simpleTimePeriod(target=self.target, assigner=self.assigner, assignee=self.assignee, timeperiod=timeperiod, operator=operator)

	def simpleChannel(self, channel, operator="http://www.w3.org/ns/odrl/2/eq"):
		return simpleChannel(target=self.target, assigner=self.assigner, assignee=self.assignee, channel=channel, operator=operator)

	def simpleDutyToPay(self, action, rightoperand, rightoperandunit, payee, operator="http://www.w3.org/ns/odrl/2/eq"):
		return simpleDutyToPay(target=self.target, assigner=self.assigner, assignee=self.assignee, action=action, rightoperand=rightoperand, rightoperandunit=rightoperandunit, payee=payee, operator=operator)

class odrl(object):

	def __init__(self):
		self.odrl = {}

	def json(self):
		return json.dumps(self.odrl)

	def xml(self):
		return etree.tostring(self.xml_etree())

	def xml_etree_permissions_prohibitions(self, type):
		permissions_prohibitions = []
		if type+"s" in self.odrl:
			for p in self.odrl[type+"s"]:
				permission_prohibition = etree.Element("{http://www.w3.org/ns/odrl/2/}" + type,
					nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
				asset = etree.Element("{http://www.w3.org/ns/odrl/2/}asset",
					nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
				asset.set('uid', p['target'])
				asset.set('relation', 'http://www.w3.org/ns/odrl/2/target')
				permission_prohibition.append(asset)

				action = etree.Element("{http://www.w3.org/ns/odrl/2/}action",
					nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
				action.set('name', p['action'])
				permission_prohibition.append(action)

				if "constraints" in p:
					for c in p["constraints"]:
						constraint = etree.Element("{http://www.w3.org/ns/odrl/2/}constraint",
							nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
						constraint.set('name', c['constraint'])
						constraint.set('operator', c['operator'])
						constraint.set('rightOperand', c['rightoperand'])
						if "rightoperanddatatype" in c:
							constraint.set('dataType', c['rightoperanddatatype'])
						if "rightoperandunit" in c:
							constraint.set('unit', c['rightoperandunit'])
						if "status" in c:
							constraint.set('status', c['status'])
						permission_prohibition.append(constraint)

				if "assigner" in p:
					assigner = etree.Element("{http://www.w3.org/ns/odrl/2/}party",
						nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
					assigner.set('function', 'http://www.w3.org/ns/odrl/2/assigner')
					assigner.set('uid', p['assigner'])
					permission_prohibition.append(assigner)

				if "assignee" in p:
					assignee = etree.Element("{http://www.w3.org/ns/odrl/2/}party",
						nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
					assignee.set('function', 'http://www.w3.org/ns/odrl/2/assignee')
					assignee.set('uid', p['assignee'])
					if "assignee_scope" in p:
						assignee.set('scope', p['assignee_scope'])
					permission_prohibition.append(assignee)

				if "duties" in p:
					for d in p["duties"]:
						duty = etree.Element("{http://www.w3.org/ns/odrl/2/}duty",
							nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
						if "target" in d:
							asset = etree.Element("{http://www.w3.org/ns/odrl/2/}asset",
								nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
							asset.set('uid', d['target'])
							asset.set('relation', 'http://www.w3.org/ns/odrl/2/target')
							duty.append(asset)

						action = etree.Element("{http://www.w3.org/ns/odrl/2/}action",
							nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
						action.set('name', d['action'])
						duty.append(action)

						if "constraints" in d:
							for c in d["constraints"]:
								constraint = etree.Element("{http://www.w3.org/ns/odrl/2/}constraint",
									nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
								constraint.set('name', c['constraint'])
								constraint.set('operator', c['operator'])
								constraint.set('rightOperand', c['rightoperand'])
								if "rightoperanddatatype" in c:
									constraint.set('dataType', c['rightoperanddatatype'])
								if "rightoperandunit" in c:
									constraint.set('unit', c['rightoperandunit'])
								if "status" in c:
									constraint.set('status', c['status'])
								duty.append(constraint)

						if "attributedparty" in d:
							attributedparty = etree.Element("{http://www.w3.org/ns/odrl/2/}party",
								nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
							attributedparty.set('function', 'http://www.w3.org/ns/odrl/2/attributedParty')
							attributedparty.set('uid', d['attributedparty'])
							permission_prohibition.append(attributedparty)

						if "consentingparty" in d:
							consentingparty = etree.Element("{http://www.w3.org/ns/odrl/2/}party",
								nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
							consentingparty.set('function', 'http://www.w3.org/ns/odrl/2/consentingParty')
							consentingparty.set('uid', d['consentingparty'])
							permission_prohibition.append(consentingparty)

						if "informedparty" in d:
							informedparty = etree.Element("{http://www.w3.org/ns/odrl/2/}party",
								nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
							informedparty.set('function', 'http://www.w3.org/ns/odrl/2/informedParty')
							informedparty.set('uid', d['informedparty'])
							permission_prohibition.append(informedparty)

						if "payeeparty" in d:
							payeeparty = etree.Element("{http://www.w3.org/ns/odrl/2/}party",
								nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
							payeeparty.set('function', 'http://www.w3.org/ns/odrl/2/payeeParty')
							payeeparty.set('uid', d['payeeparty'])
							permission_prohibition.append(payeeparty)

						if "trackingparty" in d:
							trackingparty = etree.Element("{http://www.w3.org/ns/odrl/2/}party",
								nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
							trackingparty.set('function', 'http://www.w3.org/ns/odrl/2/trackingParty')
							trackingparty.set('uid', d['trackingparty'])
							permission_prohibition.append(trackingparty)

						permission_prohibition.append(duty)

				permissions_prohibitions.append(permission_prohibition)

		return permissions_prohibitions

	def xml_etree(self):
		policy = etree.Element("{http://www.w3.org/ns/odrl/2/}policy",
			nsmap={'o': 'http://www.w3.org/ns/odrl/2/'})
		policy.set('uid', self.odrl['policyid'])
		policy.set('policytype', self.odrl['policytype'])

		for permission in self.xml_etree_permissions_prohibitions(type="permission"):
			policy.append(permission)

		for prohibition in self.xml_etree_permissions_prohibitions(type="prohibition"):
			policy.append(prohibition)

		return policy

class rightsml(odrl):

	def __init__(self):
		super(rightsml, self).__init__()
		self.odrl['policytype'] = 'http://www.w3.org/ns/odrl/2/set'

class simpleAction(rightsml):

	def __init__(self,target, assigner, assignee, action):
		super(simpleAction, self).__init__()
		self.odrl['permissions'] = [{'target' : target, 'assigner' : assigner, 'assignee' : assignee, 'action' : action}]
		hashedparams = hashlib.md5(self.json())
		self.odrl['policyid'] = 'http://example.com/RightsML/policy/' + hashedparams.hexdigest()

class simpleConstraint(simpleAction):

	def __init__(self, target, assigner, assignee, constraint, rightoperand, operator):
		super(simpleConstraint, self).__init__(target=target, assigner=assigner, assignee=assignee, action='http://www.w3.org/ns/odrl/2/distribute')
		self.odrl['permissions'][0]['constraints'] = [{'rightoperand' : rightoperand, 'constraint' : constraint, 'operator' : operator}]
		hashedparams = hashlib.md5(self.json())
		self.odrl['policyid'] = 'http://example.com/RightsML/policy/' + hashedparams.hexdigest()
	
class simpleTimePeriod(simpleConstraint):

	def __init__(self,target, assigner, assignee, timeperiod, operator):
		super(simpleTimePeriod, self).__init__(target=target, assigner=assigner, assignee=assignee, constraint='http://www.w3.org/ns/odrl/2/dateTime', operator=operator, rightoperand=timeperiod)
	
class simpleGeographic(simpleConstraint):

	def __init__(self,target, assigner, assignee, geography, operator):
		super(simpleGeographic, self).__init__(target=target, assigner=assigner, assignee=assignee, constraint='http://www.w3.org/ns/odrl/2/dateTime', operator=operator, rightoperand=geography)

class simpleChannel(simpleConstraint):

	def __init__(self,target, assigner, assignee, channel, operator):
		super(simpleChannel, self).__init__(target=target, assigner=assigner, assignee=assignee, constraint='http://www.w3.org/ns/odrl/2/purpose', operator=operator, rightoperand=channel)

class simpleDuty(simpleAction):

	def __init__(self, target, assigner, assignee, duty, constraint, action, rightoperand, operator, rightoperandunit, party, partytype):
		super(simpleDuty, self).__init__(target=target, assigner=assigner, assignee=assignee, action='http://www.w3.org/ns/odrl/2/distribute')
		self.odrl['permissions'][0]['duties']= [{'action' : action, partytype : party, 'constraints': [{'rightoperand' : rightoperand, 'constraint' : constraint, 'operator' : operator, 'rightoperandunit' : rightoperandunit}]}]
		hashedparams = hashlib.md5(self.json())
		self.odrl['policyid'] = 'http://example.com/RightsML/policy/' + hashedparams.hexdigest()

class simpleDutyToPay(simpleDuty):

	def __init__(self,target, assigner, assignee, action, rightoperand, rightoperandunit, payee, operator='http://www.w3.org/ns/odrl/2/eq'):
		super(simpleDutyToPay, self).__init__(target=target, assigner=assigner, assignee=assignee, duty='http://www.w3.org/ns/odrl/2/pay', constraint='http://www.w3.org/ns/odrl/2/payAmount', action=action, operator=operator, rightoperand=rightoperand, rightoperandunit=rightoperandunit, party=payee, partytype="payeeparty")

