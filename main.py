import os
import sys

from backward_chaining import BackwardChaining
from forward_chaining import ForwardChaining
from retrieve_data import *
import ssl,smtplib

# biến khởi tạo
validate = Validate()

data = RetrieveData()
data.getfc()
data.getbc()
luat_lui = data.groupbc()
luat_tien = data.groupfc()


# 1. Câu hỏi về giới tính
def genderQuestion():
    AllSymLst = [data.resulttrieutrung[0], data.resulttrieutrung[11],
                 data.resulttrieutrung[12], data.resulttrieutrung[17]]

    NewAllSymLst = []
    for i in AllSymLst:
        NewAllSymLst.append(i["idtrieuchung"])

    while (1):
        if (len(list_symptom_of_person) == len(AllSymLst)):
            break
        if (len(list_symptom_of_person) == 0):
            print(f'-->Chatbot: {person.name} có triệu trứng nào ở dưới đây không (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều)')
        else:
            print(f'-->Chatbot: {person.name} có triệu trứng nào nữa ở dưới đây không (Nhập số thứ tự của triệu chứng để chọn. Có thể lựa chọn nhiều)')

        count = 1
        for i in AllSymLst:
            if (i not in list_symptom_of_person):
                print(f'{count}. {i["noidung"]} \n')
            count += 1

        print("0. Tôi không có triệu chứng nào ở trên\n -------------Câu trả lời của bạn--------------")
        answer = validate.validate_input_number_form(input())
        print(f'-->{person.name}: Câu trả lời của tôi là {answer}')

        if (answer == '0'):
            break
        elif (int(answer) < 0 or int(answer) > 4):
            print('-->Chatbot: Vui lòng nhập 1 số từ 0 tới 4')
            continue
        else:
            list_symptom_of_person.append(AllSymLst[int(answer)-1])
        print(
            f'-->Chatbot: Danh sách mã các triệu chứng {person.name} đang mắc:')
        print([i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person

# 2. Câu hỏi về sự kiện
def eventQuestion():
    Location_StomachAcheSymLst = [data.resulttrieutrung[1]]
    while (1):
        check = {'idtrieuchung': 'S01', 'noidung': 'Đau bụng'}
        if (check in list_symptom_of_person):
            print(f'-->Chatbot: {person.name} đang có triệu chứng ĐAU BỤNG- một trong số các triệu chứng của các bệnh về dạ dày.\n Để có chuẩn đoán chính xác, hãy cho tôi biết chi tiết thêm về vị trí đau')
            print('1. Đau bụng vùng thượng vị (sau rốn)')
            print('0. Vị trí khác')
            print('---------------Câu trả lời của bạn---------------')
            answer = validate.validate_input_number_form(input())
            # print("Người dùng: Lựa chọn của tôi ", answer)
            print(f'-->{person.name}: Lựa chọn của tôi {answer}')
            if (int(answer) < 0 or int(answer) > 1):
                print('-->Chatbot: Vui lòng nhập số từ 0 -> 1')
                continue
            elif (answer == '0'):
                break
            else:
                list_symptom_of_person.append(Location_StomachAcheSymLst[0])
                break
        else:
            break

    print(f'-->Chatbot: Danh sách mã các triệu chứng {person.name} đang mắc:',
          [i['idtrieuchung'] for i in list_symptom_of_person])
    return list_symptom_of_person

# 3. Câu hỏi về tính chất sự kiện
def eventCharacteristicsQuestion():
    NewFrequency_StomachAcheSymLst = []
    # for i in Frequency_StomachAcheSymLst:
    #     NewFrequency_StomachAcheSymLst.append(i.code)
    Frequency_StomachAcheSymLst = [
        data.resulttrieutrung[2],
        data.resulttrieutrung[3],
        data.resulttrieutrung[4],
        data.resulttrieutrung[5],
        data.resulttrieutrung[6],
        data.resulttrieutrung[7]
    ]
    while (1):
        check = {'idtrieuchung': 'S01', 'noidung': 'Đau bụng'}
        if (check in list_symptom_of_person):

            print(
                f'-->Chatbot: Tiếp theo tôi muốn biết chi tiết hơn về tần suất đau bụng của {person.name}. (Lựa chọn vị trí đau bằng cách nhập số thứ tự)')
            count = 1
            for i in Frequency_StomachAcheSymLst:
                if (i not in list_symptom_of_person):
                    print(f'{count}. {i["noidung"]}')
                count += 1
            print('0. Bỏ qua')
            print('---------------------Câu trả lời của bạn---------------------')
            answer = validate.validate_input_number_form(input())
            print(f'-->{person.name}: Câu trả lời của tôi là {answer}')
            if (int(answer) < 0 or int(answer) > len(Frequency_StomachAcheSymLst)):
                print("-->Chatbot: Vui lòng nhập số trong khoảng 0 -> 6")
                continue
            elif (answer == '0'):
                break
            else:
                list_symptom_of_person.append(
                    Frequency_StomachAcheSymLst[int(answer)-1])
                print(
                    f'-->Chatbot: Danh sách mã các triệu chứng {person.name} đang mắc:', [i['idtrieuchung'] for i in list_symptom_of_person])
        else:
            break
    return list_symptom_of_person

#4. Câu hỏi về thời tiết
def weatherQuestion():
    

#5. Câu hỏi về vóc dáng
def bodyQuestion():
    

#6. Câu hỏi về màu da
def skinColorQuestion():
    

#7. Câu hỏi về tone da
def skinToneQuestion():
    

#8. phần suy diễn tiến
def forward_chaining(rule, fact, goal, file_name,person):
    fc = ForwardChaining(rule, fact, None, file_name)

    list_predicted_disease = [i for i in fc.facts if i[0] == "D"]
    print(
        f'-->Chatbot: Chúng tôi dự đoán {person.name} có thể bị bệnh :', end=" ")
    for i in list_predicted_disease:
        temp = data.get_benh_by_id(i)
        print(temp['tenBenh'], end=', ')
    print()
    
    print(
        f'-->Chatbot: Trên đây là chuẩn đoán sơ bộ của chúng tôi. Tiếp theo, chúng tôi sẽ hỏi {person.name} một số câu hỏi để đưa ra kết quả chính xác.', end=" ")
    return list_predicted_disease

#9. phần suy diễn lùi
def backward_chaining(luat_lui,list_symptom_of_person,list_predicted_disease,file_name ):
    predictD=list_predicted_disease
    rule=luat_lui
    all_rule=data.gettrieuchung()
    fact_real=list_symptom_of_person_id
    benh=0
    for g in predictD:
        goal=g
        D=data.get_benh_by_id(goal) #Chứa thông tin của bệnh có id == goal
        print(f"Chúng tôi đã có các triệu chứng ban đầu và có thể bạn mắc bệnh {D['tenBenh']}({goal}) , sau đây chúng tôi muốn hỏi bạn một vài câu hỏi để tìm hiểu về bệnh bạn đang mắc phải")
        all_s_in_D=all_rule[goal]
        all_s_in_D=sorted(set(all_s_in_D)-set(fact_real))
        d=searchindexrule(rule,goal)
        
        b=BackwardChaining(rule,fact_real,goal,file_name) # kết luận trong trường hợp các luât jtruwowsc đã suy ra đk luôn
        
        if b.result1==True:# đoạn đầu
            print("Bạn mắc bệnh {}- {}và chúng tôi sẽ gửi thêm thông tin về bệnh này cho bạn qua mail".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loikhuyen']=D['loikhuyen'].replace("/n","\n")
            print(f"{D['loikhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
            return goal,fact_real
        
        while(len(all_s_in_D)>0):
            s=data.get_trieuchung_by_id(all_s_in_D[0])
            question=f"Bạn có bị triệu chứng {s['noidung']}({all_s_in_D[0]}) không?"
            print(question)
            answer = validate.validate_binary_answer(input())
            
            print(f"answer: {answer}")
            if answer== True :
                fact_real.append(all_s_in_D[0])
                b=BackwardChaining(rule,fact_real,goal,file_name)
                list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,1)
                d=sorted(set(d)-set(lsD))
                all_s_in_D=sorted(set(list_no_result)-set(fact_real))
                if b.result1==True:
                    benh=1
                    break
            if answer==False :
                list_no_result,lsD=get_s_in_d(all_s_in_D[0],goal,rule,d,0) #S01 S02 S03 S04 S05
                d=sorted(set(d)-set(lsD))
                all_s_in_D=sorted(set(list_no_result)-set(fact_real))
            if len(d)==0: 
                print(f"Có vẻ như không có đề xuất về trang phục nào phù hợp với bạn {goal}-{D['tenBenh']}")
                break
        if benh==1:
            print("Bạn mắc bệnh {}- {} , và chúng tôi sẽ gửi thêm thông tin về bệnh này cho bạn qua mail".format(goal,D['tenBenh']))
            print(f"Lời khuyên")
            D['loikhuyen']=D['loikhuyen'].replace("/n","\n")
            print(f"{D['loikhuyen']}")
            print("Cám ơn bạn đã sử dụng chat bot của chúng tôi")
            
            return goal,fact_real
            break
    if benh==0:
        print(f"Bạn không bị bệnh nào cả")
        return None, fact_real