import pandas as pd
import numpy as np
from pandas.io.json import json_normalize
import json
# import api_notification

PRIORITY_TRAINEE = 1

file = open("get_output.json", "r")
contents = file. read()
file. close()
input_json = json.loads(contents)
# df = json_normalize(input_json['receivingwindow'])

def get_table(name):
    print(name)
    return json_normalize(input_json[name])

SkillID = get_table('Skills')[['SkillID', 'Skills']]
DepartmentID = get_table('Department')
DepartmentID.columns = ['DepartmentID', 'Department']
RoleID = get_table('Role')
RoleID.columns = ['RoleID', 'Role']
QualificationID = get_table('Qualification')[['QualificationID', 'Name']]
QualificationID.columns = ['QualificationID', 'Qualification']
MemberID = get_table('TeamMembers')[['TeamMemberID', 'TeamMember']]
Priority = get_table('TeamMembers')[['TeamMemberID', 'TeamMember', 'Priority']]

df_time_train_skill = get_table('SkillsConstraintType').merge(get_table('ConstraintType')).merge(SkillID)[['Skills', 'Value', 'Name']]
df_time_train_skill = df_time_train_skill[df_time_train_skill['Name'] == 'Training Hours'].reset_index(drop=True)

df_member = get_table('TeamMembers').merge(DepartmentID, how = 'left').merge(RoleID, on ='RoleID', how = 'left')[['TeamMember', 'Department', 'Role']]
df_member.columns = ['Name', 'Department', 'Role']
df_member.loc[df_member[df_member.Department.isnull()].index, 'Role'] = 'Trainers'
df_member = df_member[~df_member.Role.isnull()].reset_index(drop=True)

DF_FULL = df_member['Name']

df_member_roster = get_table('TeamMemberRoster').merge(MemberID).sort_values('StartTime')[['TeamMember', 'StartTime', 'EndTime']].merge(DF_FULL, left_on = 'TeamMember', right_on ='Name').drop(columns= 'Name')
df_member_roster['StartTime'] = pd.to_datetime(df_member_roster['StartTime'])
df_member_roster = df_member_roster[df_member_roster['StartTime'].dt.hour == 6].reset_index(drop=True)
df_member_roster['rank'] = df_member_roster.groupby('TeamMember').cumcount() + 1
df_member_roster = df_member_roster[df_member_roster['rank'] < 10*PRIORITY_TRAINEE].reset_index(drop=True)
df_member_roster.groupby('TeamMember')['StartTime'].count()

df_manda_skill = get_table('QualificationMatrix')

df_manda_skill.columns = ['QualificationID', 'SkillID', 'IsMandatory']
df_manda_skill = df_manda_skill.merge(SkillID).merge(QualificationID)[['Qualification', 'Skills', 'IsMandatory']]

tmp1 = df_manda_skill[['Qualification']].drop_duplicates().merge(df_manda_skill[df_manda_skill.Skills == 'Intro Frontrunner and Foundations'], how = 'left')
tmp1['Skills'] = 'Intro Frontrunner and Foundations'
tmp1['IsMandatory'] = True

df_manda_skill = df_manda_skill[df_manda_skill.Skills != 'Intro Frontrunner and Foundations'].append(tmp1)
df_manda_skill['IsMandatory'] = df_manda_skill['IsMandatory'].astype(int)
df_manda_skill = df_manda_skill[df_manda_skill['IsMandatory'] == 1].reset_index(drop=True)

df_manda_skill = df_manda_skill.merge(df_time_train_skill, on = 'Skills', how = 'left')

df_role_time = df_manda_skill.groupby('Qualification').Value.sum().reset_index()

df_member_detail = df_member.merge(df_role_time, left_on = 'Role', right_on = 'Qualification', how = 'left')

df_skills = get_table('Skills')[['Skills', 'ParentSkills', 'Equipment']]

df_skill_require = df_member[df_member.Role!='Trainers'].merge(df_manda_skill[['Qualification', 'Skills', 'IsMandatory', 'Value']], left_on = 'Role', right_on = 'Qualification', how='left')[['Department', 'Role', 'Name', 'Skills']]
df_skill_require[df_skill_require.Skills == 'Intro Frontrunner and Foundations']

df_member[df_member.Role!='Trainers'].Role.unique()

df_manda_skill[['Qualification', 'Skills', 'IsMandatory', 'Value']].drop_duplicates()

df_member[df_member.Role!='Trainers'].merge(df_manda_skill[['Qualification', 'Skills', 'IsMandatory', 'Value']], left_on = 'Role', right_on = 'Qualification', how='left')[['Department', 'Role', 'Name', 'Skills']].drop_duplicates()

df_role_quantity = pd.read_excel('Trainer_Plus_2.xlsx', sheet_name='Department Role Quantity')
df_role_quantity['id_dept'] = df_role_quantity.index
df_role_quantity.Department = df_role_quantity.Department.str.strip()
df_role_quantity = df_role_quantity[['Department', 'id_dept']].merge(get_table('DepartmentRoleQuantity').merge(DepartmentID)[['Department', 'HeadCount']])
df_role_quantity

df_skill_require  = df_skill_require.merge(df_role_quantity, on = 'Department', how ='left')
df_skill_require[df_skill_require.Skills == 'Intro Frontrunner and Foundations'].sort_values(['Role', 'Department']).merge(df_member_detail[['Name', 'Value']], on ='Name')

df_member_roster.merge(df_member_detail, left_on = 'TeamMember', right_on ='Name').groupby(['Department', 'StartTime']).Name.nunique()
begin_time = df_member_roster['StartTime'].min()
df_member_roster['date_diff'] = (df_member_roster['StartTime'] - begin_time).dt.days
df_member_roster['begin_time'] = 12*df_member_roster.date_diff
df_member_roster['end_time'] = 12*df_member_roster.date_diff + 11

df_trainer_skills = get_table('TrainerSkills').merge(MemberID).merge(SkillID)[['TeamMember', 'Skills', 'MaxTrainees']]
df_trainer_skills.columns = ['Trainer', 'Skills', 'MaxTrainees']

df_trainer_roster = df_trainer_skills.merge(df_member_roster, left_on = 'Trainer', right_on = 'TeamMember')

df_member_trainer = df_trainer_roster[['Trainer']].drop_duplicates().reset_index(drop=True)
df_member_trainer['id_trainer'] = df_member_trainer.index

df_trainer_roster = df_trainer_roster.merge(df_member_trainer)

df_member_trainer = df_member_trainer.merge(df_trainer_skills.groupby('Trainer')[['Skills']].count().reset_index())
df_member_trainer.columns = ['Trainer', 'id_trainer', 'score']

df_member_trainer

dic_time_mem = {}
for i in df_member_roster.iterrows():
    _member = i[1]['TeamMember']
    _begin_time = i[1]['begin_time']
    _end_time = i[1]['end_time']
    _tmp_arr = list(range(_begin_time, _end_time + 1))
    if(_member in dic_time_mem):
        dic_time_mem[_member] += _tmp_arr
    else:
        dic_time_mem[_member] = _tmp_arr      

def get_intersection_time(mem1, mem2):
    return list(set(dic_time_mem[mem1])&set(dic_time_mem[mem2]))

from ortools.sat.python import cp_model

# CPLEX

import pandas as pd
import cplex
from datetime import timedelta

# api_notification.noti("Formulating...")
df_trainee_detail = df_member_detail[~df_member_detail.Value.isnull()].sort_values(['Value','Role', 'Department']).reset_index(drop=True)

df_trainee_detail['id_trainee'] = df_trainee_detail.index

df1 = df_skill_require[df_skill_require.Skills == 'Intro Frontrunner and Foundations'].sort_values(['Role', 'Department']).merge(df_trainee_detail[['Name', 'Value', 'id_trainee']], on ='Name').sort_values('id_trainee').reset_index(drop=True)

df2 = df_trainer_roster[df_trainer_roster['Skills'] == 'Intro Frontrunner and Foundations'].reset_index(drop=True)
df2_trainer_capacity = df2.groupby('date_diff')[['Trainer']].nunique().reset_index()

df1

df_member_trainer

df_id_trainer = df_member_trainer.copy()
df_id_trainee = df1.copy()

df1.to_csv('trainee_id.csv', index=False)
df_member_trainer.to_csv('trainer_id.csv', index=False)

df_utilization = get_table('TrainerUtilization').merge(MemberID)[['TeamMember', 'Utilization']]
df_utilization.columns = ['Trainer', 'utilization']
df_utilization = df_utilization.merge(df_id_trainer)[['id_trainer', 'utilization']]

TIME_CONSTRAINT = df_time_train_skill[df_time_train_skill.Skills == 'Intro Frontrunner and Foundations'].iloc[0]['Value']
df1 = df1.merge(Priority[Priority.Priority == PRIORITY_TRAINEE], left_on = 'Name', right_on = 'TeamMember')[df1.columns]

dic_var = {}


trainer_hour_list = {}


check_c_ij = {}
name_check_c_ij = []

model = cp_model.CpModel()

for t in df_member_trainer.iterrows():
    _name_trainer = t[1]['Trainer']
    _id_trainer = t[1]['id_trainer']
    _list_time = list(set(dic_time_mem[_name_trainer]))
    trainer_hour_list[_id_trainer] = {}
    check_c_ij[_id_trainer] = {}
    for j in _list_time:
        _datediff = int(np.floor(j/12.))
        _hours = int(j - _datediff*12)
        
        dic_var[f"t_{_id_trainer}_{_datediff}_{_hours}"] = model.NewBoolVar(f"t_{_id_trainer}_{_datediff}_{_hours}")
#         dic_var[f"t_{_id_trainer}_{_datediff}_{_hours}"] = f"t_{_id_trainer}_{_datediff}_{_hours}"
        _check_hour = dic_var[f"t_{_id_trainer}_{_datediff}_{_hours}"]
        
        name_check_c_ij.append(_check_hour)
        if(_datediff in check_c_ij[_id_trainer]):
            check_c_ij[_id_trainer][_datediff].append(_check_hour)
        else:
            check_c_ij[_id_trainer][_datediff] = []
            check_c_ij[_id_trainer][_datediff].append(_check_hour)
        if(_datediff in trainer_hour_list[_id_trainer]):
            trainer_hour_list[_id_trainer][_datediff][_hours] = []
        else:
            trainer_hour_list[_id_trainer][_datediff] = {}
            trainer_hour_list[_id_trainer][_datediff][_hours] = []


trainee_day_list = {}

hour_list = []
check_x_ij = []
for i in range(0,df_member_roster.date_diff.max()+1):
    hour_list.append([])
    check_x_ij.append([])
    for j in range(0,12):
        hour_list[i].append([])
    for j in range(0,9):
        check_x_ij[i].append([])

name_check_x_ij = []
for i in df1.iterrows():
    _name_trainee = i[1]['Name']
    _id_trainee = i[1]['id_trainee']
    _id_dept = i[1]['id_dept']
    _value_train = i[1]['Value']
    _tmp_roster = df_member_roster[df_member_roster['TeamMember'] == _name_trainee].reset_index()
    trainee_day_list[_id_trainee] = {}
    for j in _tmp_roster.iterrows():
        _datediff = j[1]['date_diff']
        dic_var[f"c_{_id_trainee}_{_datediff}"] = model.NewBoolVar(f"c_{_id_trainee}_{_datediff}")
#         dic_var[f"c_{_id_trainee}_{_datediff}"] = f"c_{_id_trainee}_{_datediff}"
        _check_date = dic_var[f"c_{_id_trainee}_{_datediff}"]
        check_x_ij[_datediff][_id_dept].append(_check_date)
        name_check_x_ij.append(_check_date)
        trainee_day_list[_id_trainee][_datediff] = []

df1


# # w_ti = []
name_wti = []

# # for t in range(len(df_member_trainer)):
# #     _id_trainer = t
# #     for i in range(len(df1)):
# #         _id_trainee = i
# #         varname = f"w_{_id_trainer}_{_id_trainee}"
# #         name_wti.append(varname)       
count_num_trainer_per_trainee = {}
for i in list(df1.id_trainee):
    _id_trainee = i
    count_num_trainer_per_trainee[_id_trainee] = []
    for t in range(len(df_member_trainer)):
        _id_trainer = t
        dic_var[f"w_{_id_trainer}_{_id_trainee}"] = model.NewBoolVar(f"w_{_id_trainer}_{_id_trainee}")
#         dic_var[f"w_{_id_trainer}_{_id_trainee}"] = f"w_{_id_trainer}_{_id_trainee}"
        varname = dic_var[f"w_{_id_trainer}_{_id_trainee}"]
        count_num_trainer_per_trainee[_id_trainee].append(varname)
        name_wti.append(varname)       


x_itjk = {}
name_var_x_itjk = {}
name_xitjk = []
obj_xitjk = []

trainee_trainer_cross = {}

for i in df1.iterrows():
    _name_trainee = i[1]['Name']
    _id_trainee = i[1]['id_trainee']
    _id_dept = i[1]['id_dept']
    _value_train = i[1]['Value']
    x_itjk[_id_trainee] = []
    name_var_x_itjk[_id_trainee] = []

    trainee_trainer_cross[_id_trainee] = {}
    for t in df_member_trainer.iterrows():
        _name_trainer = t[1]['Trainer']
        _id_trainer = t[1]['id_trainer']
        _score_trainer = t[1]['score']
        trainee_trainer_cross[_id_trainee][_id_trainer] = []
        _list_inter_time = get_intersection_time(_name_trainee, _name_trainer)
        count_obj = 0
        for j in np.sort(_list_inter_time):
            count_obj+=1
            _datediff = int(np.floor(j/12.))
            _hours = int(j - _datediff*12)
            
            dic_var[f"x_{_id_trainee}_{_id_trainer}_{_datediff}_{_hours}"] = model.NewBoolVar(f"x_{_id_trainee}_{_id_trainer}_{_datediff}_{_hours}")
#             dic_var[f"x_{_id_trainee}_{_id_trainer}_{_datediff}_{_hours}"] = f"x_{_id_trainee}_{_id_trainer}_{_datediff}_{_hours}"
            varname = dic_var[f"x_{_id_trainee}_{_id_trainer}_{_datediff}_{_hours}"]
            name_xitjk.append(varname)
            # obj_xitjk.append(count_obj)
            obj_xitjk.append(np.log(_datediff*12 + _hours +  1)*0.1 + count_obj + np.log(_value_train+1)*0.01)

            x_itjk[_id_trainee].append(varname)
            name_var_x_itjk[_id_trainee].append(f"x_{_id_trainee}_{_id_trainer}_{_datediff}_{_hours}")
            trainer_hour_list[_id_trainer][_datediff][_hours].append(varname)
            trainee_day_list[_id_trainee][_datediff].append(varname)
            trainee_trainer_cross[_id_trainee][_id_trainer].append(varname)



objective_terms = []
objective_terms.append(sum([name_xitjk[i]*int(obj_xitjk[i]*1000) for i in range(len(name_xitjk))]))
objective_terms.append(sum(name_wti)*10000)
model.Minimize(sum(objective_terms))


for i in x_itjk:
    model.Add(sum(var for var in x_itjk[i]) - int(TIME_CONSTRAINT) == 0)

skill_trainers = df2[['id_trainer', 'MaxTrainees']].drop_duplicates().reset_index(drop=True)
for i in trainer_hour_list:
    print(i)
    print(skill_trainers)
    if(len(skill_trainers[skill_trainers.id_trainer == i])>0):
        _cap_trainer = float(skill_trainers[skill_trainers.id_trainer == i].iloc[0]['MaxTrainees'])
    else:
        _cap_trainer = 0
    print("CAP TRAINER:",_cap_trainer)

    for j in trainer_hour_list[i]:
        for k in trainer_hour_list[i][j]:
            model.Add(sum(trainer_hour_list[i][j][k]) <= int(_cap_trainer))

for i in check_c_ij:
    utili = float(df_utilization[df_utilization.id_trainer == i].iloc[0]['utilization'])
    for j in check_c_ij[i]:
        model.Add(sum(check_c_ij[i][j]) <= int(12*utili))
        
for i in range(len(check_x_ij)):
    for j in range(len(check_x_ij[i])):
        if(len(check_x_ij[i][j]) > 0):
            max_cap = df_role_quantity[df_role_quantity.id_dept == j].iloc[0,2]
            model.Add(sum(check_x_ij[i][j]) <= int(max_cap))

for i in x_itjk:
    tmp = pd.DataFrame([name_var_x_itjk[i], x_itjk[i]]).T
    tmp.columns = ['name_x_itjk', 'x_itjk']
    tmp[['id_trainer', 'datediff', 'hour']] = tmp['name_x_itjk'].str.split('_', expand=True)[[2,3,4]]
    tmp1 = tmp.groupby(['datediff', 'hour']).agg({'x_itjk':list}).reset_index()
    tmp2 = tmp.groupby(['datediff']).agg({'x_itjk':list}).reset_index()
    for j in tmp2.iterrows():
        _tmp_datediff = j[1]['datediff']
        tmp_check = dic_var[f"c_{i}_{_tmp_datediff}"]
        _tmp_xijk = j[1]['x_itjk']
        _trainer_tmp_xijk = tmp1[tmp1.datediff == _tmp_datediff]
        # check >= x_ijk[..]
        for k in _trainer_tmp_xijk.iterrows():
            model.Add(sum(k[1]['x_itjk'])<=tmp_check)
        model.Add(sum(_tmp_xijk) >= tmp_check)

for i in list(df1.id_trainee):
    model.Add(sum(count_num_trainer_per_trainee[i]) == 1)

for i in list(df1.id_trainee):
    for j in range(len(df_member_trainer)):
        _id_trainer = j
        _id_trainee = i
        varname = dic_var[f"w_{_id_trainer}_{_id_trainee}"]
        for x in trainee_trainer_cross[_id_trainee][_id_trainer]:
            model.Add(varname>=x)

solver = cp_model.CpSolver()
solver.parameters.log_search_progress = True
solver.parameters.num_search_workers = -1
status = solver.Solve(model)
# status = solver.SearchForAllSolutions(model)

status
