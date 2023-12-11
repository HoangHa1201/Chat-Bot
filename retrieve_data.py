import re

import mysql.connector
import json
myDatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234567890",
    database="BTL_TRI_THUC"  
)

class RetrieveData:
    """
    Truy vấn và xử lý dữ liệu
    """
    def __init__(self):
        self.eventList = []
        self.eventCharacteristicList = []
        self.bodyList = []
        self.skinColorList = []
        self.skinToneList = []
        self.forwardChainingList = []
        self.backwardChainingList = []

    def retrieveEvent(self):
        """
        Lấy dữ liệu sự kiện
        """
        dbbenh = myDatabase.cursor()
        dbbenh.execute("SELECT * FROM chtdttt.benh;")
        benh = dbbenh.fetchall()
        dirbenh = {}
        for i in benh:
            dirbenh['idbenh'] = i[0]
            dirbenh['tenBenh'] = i[1]
            dirbenh["nguyennhan"] = i[2]
            dirbenh['loikhuyen'] = i[3]
            self.resultbenh.append(dirbenh)
            dirbenh = {}

    def retrieveEventCharacteristic(self):
        """
        Lấy dữ liệu từ bảng trieuchung
        """
        dbtrieuchung = myDatabase.cursor()
        dbtrieuchung.execute("SELECT * FROM chtdttt.trieuchung;")
        trieuchung = dbtrieuchung.fetchall()
        dirtrieuchung = {}
        # resulttrieuchung=[]
        for i in trieuchung:
            dirtrieuchung['idtrieuchung'] = i[0]
            dirtrieuchung['noidung'] = i[1]
            self.resulttrieutrung.append(dirtrieuchung)
            dirtrieuchung = {}

    def retrieveBody(self):
        
    
    def retrieveSkinColor(self):
        
    
    def retrieveSkinTone(self):
        

    # not use
    def getForwardChaining(self):
        """
        Nhóm các bệnh cùng 1 triệu chứng
        """
        dbfc = myDatabase.cursor()
        dbfc.execute(
            "select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='1'")
        fc = dbfc.fetchall()
        s = []
        d = []
        for i in range(len(fc)):
            s.append(fc[i][2])
            d.append(fc[i][3])

        tt = s[0]
        benh = []
        dicfc = {}
        for i in range(len(s)):
            if s[i] == tt:
                benh.append(d[i])
            else:
                dicfc['trieuchung'] = tt
                dicfc['benh'] = benh
                tt = s[i]
                self.resultfc.append(dicfc)
                benh = []
                benh.append(d[i])
                dicfc = {}

    def getBackwardChaining(self):
        """
        Nhóm các triệu chứng cùng 1 bệnh
        """
        dbbc = myDatabase.cursor()
        dbbc.execute("select idsuydien, luat.idluat, idtrieuchung, idbenh, trangthai from suydien, luat where suydien.idluat=luat.idluat and trangThai='0' order by idbenh")
        fc = dbbc.fetchall()
        rule = []
        s = []
        d = []
        for i in range(len(fc)):
            rule.append(fc[i][1])
            s.append(fc[i][2])
            d.append(fc[i][3])
        # print(rule)
        vtrule = rule[0]
        tt = []
        benh = None
        # result=[]
        dicbc = {}
        for i in range(len(rule)):
            if rule[i] == vtrule:
                tt.append(s[i])
                benh = d[i]
            else:
                dicbc['rule'] = vtrule
                dicbc['benh'] = benh
                dicbc['trieuchung'] = tt
                vtrule = rule[i]
                self.resultbc.append(dicbc)
                benh = d[i]
                tt = []
                tt.append(s[i])
                dicbc = {}

class Validate:
    def __init__(self) -> None:
        pass

    def validate_binary_answer(self, value):
        acceptance_answer_lst = ['1', 'y', 'yes', 'co', 'có']
        decline_answer_lst = ['0', 'n', 'no', 'khong', 'không']
        value = value+''
        while (1):
            if (value) in acceptance_answer_lst:
                return True
            elif value in decline_answer_lst:
                return False
            else:
                print(
                    "-->Chatbot: Câu trả lời không hợp lệ. Vui lòng nhập lại câu trả lời")
                value = input()

class TreeForFC(object):
    def __init__(self, id, left=None, right=None):
        self.id = id
        self.left = left
        self.right = right

class Symptom:
    def __init__(self, code, detail):
        self.code = code
        self.detail = detail

def printTree(node, level=0):
    if node != None:
        printTree(node.left, level + 1)
        print(' ' * 10 * level + '-> ' + str(node.value))
        printTree(node.right, level + 1)
        

def searchindexrule(rule,goal):
    """
    Tìm vị trí các rule có bệnh là goal
    """
    index=[]
    for r in range(len(rule)):
        if rule[r][0]==goal:
            index.append(r)
    return index

def get_s_in_d(answer,goal,rule,d,flag):
    """
    Lấy các triệu chứng theo sự suy diễn để giảm thiểu câu hỏi
    và  đánh dấu các luật đã được duyệt qua để bỏ qua những luật có cùng cùng câu hỏi vào
    """
    result=[]
    index=[]
    if flag==1:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)
                        # result=set()
    else:
        for i in range(len(rule)):
            if (rule[i][0]==goal) and (answer in rule[i]): index.append(i)
            if (rule[i][0]==goal) and (answer not in rule[i]) and (i in d):
                for j in rule[i]:
                    if j[0]=='S':
                        result.append(j)        

    return sorted(set(result)),index


'''
db = ConvertData()
db.convertbenh()  # bang benh
db.converttrieuchung()  # bang trieu chung
db.getfc()
db.getbc()
luat_lui = db.groupbc()
luat_tien = db.groupfc()
print(db.resultbenh)

'''