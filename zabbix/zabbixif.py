if len(sys.argv) <= 2 or sys.argv[1].lower() == '-h':
        showmenu()
        exit(0)
    elif sys.argv[1][1:].lower() == "ch" and sys.argv[3][1:].lower() == "g" and sys.argv[5][1:].lower() == "t":
        #host creat    
        hosts = []
        hosts = sys.argv[2].split(',') #get in put hosts
        templates = {} 
        templatesvalues = ''
        alltemplates = test.template_get() #get zabbix server all templates
        groups = {}
        groupsvalues =''
        allgroups =test.hostgroup_get() # get zabbix server all groups
        for i in sys.argv[4].split(','):
            # get input  goups
            for j in  allgroups:
                if i.lower() == j.get('name').lower():
                    groups[j.get('name')] = j.get('groupid')
                    groupsvalues += "\ngroup id:" + j.get('groupid') + " group name: " + j.get('name')

        for i in sys.argv[6].split(','):
            #get input templates
            for j in alltemplates:
                if i == j.get('name'):
                    templates[j.get('name')] = j.get('templateid') 
                    templatesvalues += "\ntemplate id:" + j.get('templateid') + "  template name:" + j.get('name')
        iscreate = raw_input(" hosts name:" + hosts[0] + " hosts ip:" + hosts[1] + templatesvalues + groupsvalues + '\n' + "please input (Y/N):").lower()
        if iscreate == 'y':
            # is it create?
            print "plase wait creating"
            hostname = hosts[0]
            hostip = hosts[1]
            groupid = groups.values()
            templateid = templates.values()
            print test.host_create(hostname,hostip,groupid,templateid)
        # else:
        #     print sys.argv[2][1:].lower() , sys.argv[3][1:].lower() , sys.argv[5][1:].lower() 
        #     for i in range(0,len(sys.argv)):
        #         print  str(i) + " : " + sys.argv[i]