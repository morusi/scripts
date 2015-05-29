# coding=utf-8
#import MySQLdb
import commands
import datetime, time
import sys, getopt
import os
import re

_PATH = os.path.abspath('.')

def usage():
    print '''usage: python %s/%s [--init|--increment|--full_backup]
    --init              dump no row information and restore tables structure
    --full_backup       dump tables where CREATEDATA < today
    --increment        dump tables where CREATEDATA between yesterday and today
    ''' %(_PATH, __file__)

def print_color_strings(_strings):
    print "\033[1;31;40m%s\033[0m" %(_strings)

def GetNeedDataBaseName(HOST, usER, PASSWD, DB_Regex, PORT=3306):
    try:
        conn = MySQLdb.connect(host=HOST, user=usER, passwd=PASSWD, port=PORT)
        cur = conn.cursor()
        sql = "show databases"
        cur.execute(sql)
        result = []
        for row in cur.fetchall():
            for r in row:
                if re.match(DB_Regex, r):
                    result.append(r)
        cur.close()
        conn.close()
        return result
    except MySQLdb.Error,e:
        print e.args[0], e.args[1]
        sys.exit(2)

def DataBaseIsExist(HOST, usER, PASSWD, DB_NAME, PORT=3306):
    try:
        conn = MySQLdb.connect(host=HOST, user=usER, passwd=PASSWD, port=PORT)
        cur = conn.cursor()
        sql = '''show databases where `Database` = \'%s\'''' %(DB_NAME)
        r = cur.execute(sql)
        cur.close()
        conn.close()
        if r:
            return True
        else:
            return False
    except MySQLdb.Error,e:
        print e.args[0], e.args[1]
        sys.exit(2)    

try:
    opts, args = getopt.getopt(sys.argv[1:], "ih", ["init", "increment","full_backup"])
except getopt.GetoptError:
    usage()
    sys.exit(1)

if not opts:
    usage()
    sys.exit(1)

source_db = { 
    'obt_ios_gz01' : {
        'DB01' : 
        {
            'prefix' : '',
            'Host' : 'rdsbq0z51a90fa67kth4n.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_global', ],
        },

        'DB02' : 
        {
            'prefix' : '',
            'Host' : 'rdsbq0z51a90fa67kth4n.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat', 'wcat_log', 'wcat_coop', 'wcat_ua00', 'wcat_ua01', 'wcat_ua02', 'wcat_ua03', 'wcat_us00', 'wcat_us01', 'wcat_us02', 'wcat_us03'],
        },
    },

    'obt_ios_gz02' : {
        'DB01' : 
        {
            'prefix' : '',
            'Host' : 'rdse9c1hrd6i81xm4ett4.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_global', ],
        },

        'DB02' : 
        {
            'prefix' : '',
            'Host' : 'rdse9c1hrd6i81xm4ett4.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat', 'wcat_log', 'wcat_coop', 'wcat_ua00', 'wcat_ua01', 'wcat_ua02', 'wcat_ua03', 'wcat_us00', 'wcat_us01', 'wcat_us02', 'wcat_us03'],
        },
    },

    'android01_gz01' : {
        'DB01' : 
        {
            'prefix' : '',
            'Host' : 'rdsjwodehvn9ga6uwj28s.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_global', 'wcat', 'wcat_coop', 'wcat_ua00', 'wcat_ua01', 'wcat_us00', 'wcat_us01',],
        },

        'DB02' : 
        {
            'prefix' : '',
            'Host' : 'rdsw18xv26kf8i72s4t2r.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_log', 'wcat_ua02', 'wcat_ua03', 'wcat_us02', 'wcat_us03'],
        },
    },

    'android01_gz02' : {
        'DB01' : 
        {
            'prefix' : '',
            'Host' : 'rdskmsrjtu5f1q9eoi4ww.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_global', 'wcat', 'wcat_coop', 'wcat_ua00', 'wcat_ua01', 'wcat_us00', 'wcat_us01',],
        },

        'DB02' : 
        {
            'prefix' : '',
            'Host' : 'rdsfu43wal6kq9uma34rb.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_log', 'wcat_ua02', 'wcat_ua03', 'wcat_us02', 'wcat_us03'],
        },
    },

    'android02_gz01' : {
        'DB01' : 
        {
            'prefix' : '',
            'Host' : 'rdsckq6zxo6zfc0afz0sa.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_global', 'wcat', 'wcat_coop', 'wcat_ua00', 'wcat_ua01', 'wcat_us00', 'wcat_us01',],
        },

        'DB02' : 
        {
            'prefix' : '',
            'Host' : 'rdsc6soqzjdc64m5ul7or.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_log', 'wcat_ua02', 'wcat_ua03', 'wcat_us02', 'wcat_us03'],
        },
    },

    'android02_gz02' : {
        'DB01' : 
        {
            'prefix' : '',
            'Host' : 'rdstm1dlo1126k7uwbrhr.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_global', 'wcat', 'wcat_coop', 'wcat_ua00', 'wcat_ua01', 'wcat_us00', 'wcat_us01',],
        },

        'DB02' : 
        {
            'prefix' : '',
            'Host' : 'rdsn60l8op29d0vroityn.mysql.rds.aliyuncs.com',
            'user' : 'wcat',
            'Passwd' : 'gumichina0120',
            'database_list' : [ 'wcat_log', 'wcat_ua02', 'wcat_ua03', 'wcat_us02', 'wcat_us03'],
        },
    },
}

analystic_db = {
    'Host' : 'rds5kwrkhygzmwe0favmy.mysql.rds.aliyuncs.com',
    'user' : 'wcat',
    'Passwd' : 'Gumichina0521'
}

tables_dic = {
    'wcat' :
    [
    #"guestuser",
    "user",
    #"deviceidhistory",
    "goldhistory",
    "inappbillingstatus",
    #"apppurchasestatus",
    #"userweapon",
    "pvpbattlehistory",
    ],

    'wcat_log' :
    [
#    "useraccesslog",
    "usercardlog",
    "usercitylog",
    "usergachalog",
    "useritemlog",
#    "userquestlog",
    "userweaponlog",
    "usercoopquestlog",
    "userlevellog",
    "usermanipulationlog",
    "usermoneylog",
    "usersoullog",
    "userviplog",
    "userloginstamplog",
    "userrespkglog",
    ],

    'wcat_coop' :
    [
    "userclearstatuscoopquest",
    "usercoopcampaign",
    "userlobby",
    "usercoopquest",
    ],

    'wcat_global' :
    [
    #platformuser GNA服：初始化表结构的时候需要更新索引platformId, platformUserId, gamezoneSeq, guestId，线上库对应索引为：platformId, platformUserId, gamezoneSeq
    #"platformuser",
    #"accountdevice",
    "useraccount",
    #"activehistory",
    "globalgiftcode",
    ],

    'wcat_ua00' :
    [
    #"userstatus",
    "userachievement",
    "usercard",
    "usercardskilltree",
    "usercityenvironment",
    #"userequipment",
    "userblackmarketboughthistory",
    "userblackmarketrefreshtimes",
    ],

    'wcat_us00' :
    [
    "userachievementactivitycount",
    "usercitybuilding",
    "userclearstatusarea",
    ],
}



_today = datetime.date.today()
_yesterday = _today + datetime.timedelta(days=-1)
DUMP_DIR = '/D:'


for zone_id in source_db:
    for _db_id in source_db[zone_id]:
        for _d_name in source_db[zone_id][_db_id]['database_list']:
            if re.match(r'.*ua\d+$', _d_name) and not _d_name.endswith('00'):
                tables_dic[_d_name] = tables_dic['wcat_ua00']
        for (_database, _tables) in tables_dic.items():
            print _database + "\n  tables:", _tables 

        sys.exit(0)