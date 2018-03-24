from __future__ import division

def defineNodes(nodes):
    n = input('How many nodes? ')
    for i in range(0,n):
        nodes[input("Enter unique name for node " + str(i+1) + ": ")] = {}
        
    for k in nodes.keys():
        nodes[k]['LinkedTo'] = [] # establishes node as a hub point
        nodes[k]['HubScore'] = 0 # initializes hub score to 0
        nodes[k]['AuthScore'] = 0 # initializes authority score to 0
        nodes[k]['HubScoreNorm'] = 0.0
        nodes[k]['AuthScoreNorm'] = 0.0
    
    for k in nodes.keys():
        nodes[k]['LinkedTo'] = buildHubLinks(k)
        
    return nodes

def buildHubLinks(k):
    hubs = [int(x) for x in raw_input("For Hub " + str(k) + ", enter Authorities linked to: ").split()]
    if (len(hubs) > 1) : hubs.sort()
    
    return hubs

def printNodes(nodes):
    print "List of Nodes"
    print "==========================="
    for k in nodes.keys():
        print(k, nodes[k])
    
    print ""

def printHubRankings(nodes, hubs):
    print "Hub Rankings"
    print "==========================="
    
    for h in hubs:
        print str(h) + " : " + str(nodes[h]['HubScoreNorm'])

    print ""

def printAuthorityRankings(nodes, authorities):
    print "Authority Rankings"
    print "==========================="
    
    for a in authorities:
        print str(a) + " : " + str(nodes[a]['AuthScoreNorm'])
        
    print ""
    
def initHubScores(nodes):
    for k in nodes.keys():
        if (len(nodes[k]['LinkedTo']) > 0):
            nodes[k]['HubScore'] = 1
    
    totalHubScores = 0
    for k in nodes.keys():
        totalHubScores += nodes[k]['HubScore']
    
    for k in nodes.keys():
        nodes[k]['HubScoreNorm'] = round(nodes[k]['HubScore'] / totalHubScores, 6)
    
    return nodes

def updateHubScores(nodes, hubs):
    for h in hubs:
        nodes[h]['HubScore'] = 0
        for a in nodes[h]['LinkedTo']:
            nodes[h]['HubScore'] += nodes[a]['AuthScore']
    
    totalHubScores = 0
    for k in nodes.keys():
        totalHubScores += nodes[k]['HubScore']
        
    for k in nodes.keys():
        nodes[k]['HubScoreNorm'] = round(nodes[k]['HubScore'] / totalHubScores, 6)
    
    return nodes
    
def updateAuthScores(nodes, hubs, authorities):
    for a in authorities:
        nodes[a]['AuthScore'] = 0
        for h in hubs:
            if (a in nodes[h]['LinkedTo']):
                nodes[a]['AuthScore'] += nodes[h]['HubScore']
                
    totalAuthScores = 0
    for k in nodes.keys():
        totalAuthScores += nodes[k]['AuthScore']
    
    for k in nodes.keys():
        nodes[k]['AuthScoreNorm'] = round(nodes[k]['AuthScore'] / totalAuthScores, 6)
    
    return nodes
        
def getHubs(nodes, hubs):
    for k in nodes.keys():
        if (len(nodes[k]['LinkedTo']) > 0 and k not in hubs):
            hubs.append(k)
        
    return hubs.sort()
    
def getAuthorities(nodes, auths):
    for k in nodes.keys():
        if (len(nodes[k]['LinkedTo']) > 0):
            for a in nodes[k]['LinkedTo']:
                if (a not in auths):
                    auths.append(a)
    
    return auths.sort()

def countHubs(nodes):
    count = 0
    for k in nodes.keys():
        if (len(nodes[k]['LinkedTo']) > 0):
            count += 1
    
    return count
    
def countAuthorities(nodes):
    resultList = []
    
    for k in nodes.keys():
        resultList + nodes[k]['LinkedTo']
    
    return len(set(resultList))

nodes = {}
hubs = []
authorities = []

defineNodes(nodes)
getHubs(nodes, hubs)
getAuthorities(nodes, authorities)

steps = input('Number of steps: ')
for i in range(0,steps + 1):
    if (i == 0):
        initHubScores(nodes)
        updateAuthScores(nodes, hubs, authorities)
    else:
        updateHubScores(nodes, hubs)
        updateAuthScores(nodes, hubs, authorities)
    
print "==============================="
print "Normalized Scores After Step " + str(i)
print "==============================="
printHubRankings(nodes, hubs)
printAuthorityRankings(nodes, authorities)