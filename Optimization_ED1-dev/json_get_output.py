def solve():    
    import pandas as pd
    import numpy as np

    # skill12 = round(pd.read_csv('output_v1/skill12.csv'))
    # skill3 = round(pd.read_csv('output_v1/skill3.csv'))
    # skillk = round(pd.read_csv('output_v1/other_skill.csv'))

    import glob
    file_name = glob.glob("output_v1/priority_*.csv")
    prev = pd.DataFrame()
    for i in file_name:
        _prev = round(pd.read_csv(i))
        prev = pd.concat([prev, _prev])

    

    # skill_full = pd.concat([skill12, skill3, skillk])

    skill_full = prev.reset_index(drop=True)

    # check_full_skill = pd.read_csv('../trainee_detail.csv')

    # check_full_skill

    # check = skill_full.copy()

    # check[['id_trainee', 'id_trainer', 'datediff', 'hour']] = check['variable'].str.split('_', expand=True)[[1,2,3,4]].astype(int)

    # tmp = check.groupby('id_trainee').hour.count().reset_index()
    # tmp.columns = ['id_trainee', 'num_hour_real']

    # tmp2 = check_full_skill.merge(tmp, how = 'outer')

    df_member_trainee = pd.read_csv('trainee_id.csv')
    df_member_trainee
    df_member_trainer = pd.read_csv('trainer_id.csv')
    df_member_trainer



    # skill3 = a


    list_skill = list(skill_full['Skill'].unique())
    print(list_skill)
    for i in range(len(list_skill)):
        NUM = i
        skill3 = skill_full.copy()
        skill3 = skill_full[(skill_full.type == 'x')&(skill_full.value == 1)&(skill_full.Skill == list_skill[NUM])].reset_index(drop=True)
        SKILL = list_skill[NUM]
        print(f"SKILL {i}:", SKILL)
    #     skill3 = skill3[(skill3.type == 'x')&(skill3.value == 1)].reset_index(drop=True)
    #     SKILL = 'EMV'
        skill3

        skill3 = skill3[skill3.type =='x']

        skill3['value'].unique()

        ## Logic check

        skill3[['id_trainee', 'id_trainer', 'datediff', 'hour']] = skill3['variable'].str.split('_', expand=True)[[1,2,3,4]].astype(int)

        skill3

        print("check trung gio", skill3.groupby(['id_trainee', 'datediff', 'hour']).count().max().max())

        #1trainee is trained by 1 trainer only for 1 skill
        print(skill3.groupby(['id_trainee']).id_trainer.nunique().value_counts())

        #number of trainees a trainer trains per hour
        skill3.groupby(['id_trainer','datediff','hour']).id_trainee.nunique().reset_index().sort_values('id_trainee',ascending=False)

        skill3 = skill3.merge(df_member_trainee,on='id_trainee',how='left')[['id_trainee','Department','id_trainer','datediff','hour']]

        print(skill3)

        #number of max member from department per day
        print(skill3.groupby(['Department','datediff']).id_trainee.nunique().reset_index().groupby('Department').id_trainee.max().reset_index())

        # number of trainees trained this skill
        print(skill3['id_trainee'].nunique())



        begin_time = '2020-08-31 06:00:00'

        begin_time = pd.to_datetime(begin_time)
        begin_time

        ## Output Trainee File

        skill = skill3.copy()
        skill

        skill = skill.sort_values(['id_trainee', 'id_trainer', 'datediff', 'hour']).reset_index(drop=True)

        skill.head(10)



        skill['shift_1'] = skill.groupby(['id_trainee', 'id_trainer', 'datediff'])['hour'].shift()
        skill['shift_2'] = skill.groupby(['id_trainee', 'id_trainer', 'datediff'])['hour'].shift(-1)

        tmp_begin = skill[(skill.shift_1.isnull())|(skill.hour - skill.shift_1 > 1)].reset_index(drop=True)
        tmp_end = skill[(skill.shift_2.isnull())|(skill.shift_2 - skill.hour > 1)].reset_index(drop=True)

        tmp_end

        tmp_begin['end_hour'] = tmp_end['hour']

        output_trainee = tmp_begin.copy()

        output_trainee.drop(columns=['shift_1', 'shift_2'], inplace = True)

        output_trainee

        output_trainee['begin_time'] = begin_time

        from datetime import timedelta
        output_trainee['Start Date'] = output_trainee.begin_time + output_trainee.datediff.apply(lambda x: pd.Timedelta(x, unit='D')) + output_trainee.hour.apply(lambda x: pd.Timedelta(x, unit='H'))
        output_trainee['End Date'] = output_trainee.begin_time + output_trainee.datediff.apply(lambda x: pd.Timedelta(x, unit='D')) + output_trainee.end_hour.apply(lambda x: pd.Timedelta(x, unit='H'))
        output_trainee['End Date'] = output_trainee['End Date'] + pd.Timedelta(1, unit='H')
        output_trainee['Skill'] = SKILL

        output_trainee = output_trainee.merge(df_member_trainee,on='id_trainee',how='left').merge(df_member_trainer,on='id_trainer',how='left').rename(columns={'Name':'Team Member'})[['Team Member','Start Date','End Date','Skill','Trainer']]

        output_trainee.sort_values(['Team Member', 'Start Date'])

        output_trainee['Team Member'].nunique()



        output_trainee.to_csv(f'export_folder/skill{NUM}_trainee.csv',index=False)

        ## Output trainer file

        skill = skill3.copy()

        skill= skill[['id_trainer', 'datediff', 'hour']].drop_duplicates().sort_values(['id_trainer', 'datediff', 'hour']).reset_index(drop=True)

        skill['shift_1'] = skill.groupby(['id_trainer', 'datediff'])['hour'].shift()
        skill['shift_2'] = skill.groupby(['id_trainer', 'datediff'])['hour'].shift(-1)

        skill.head(20)

        tmp_begin = skill[(skill.shift_1.isnull())|(skill.hour - skill.shift_1 > 1)].reset_index(drop=True)
        tmp_end = skill[(skill.shift_2.isnull())|(skill.shift_2 - skill.hour > 1)].reset_index(drop=True)
        tmp_begin['end_hour'] = tmp_end['hour']

        output_trainer = tmp_begin.copy()

        output_trainer.drop(columns=['shift_1', 'shift_2'], inplace = True)

        output_trainer

        output_trainer['begin_time'] = begin_time

        from datetime import timedelta
        output_trainer['Start Date'] = output_trainer.begin_time + output_trainer.datediff.apply(lambda x: pd.Timedelta(x, unit='D')) + output_trainer.hour.apply(lambda x: pd.Timedelta(x, unit='H'))
        output_trainer['End Date'] = output_trainer.begin_time + output_trainer.datediff.apply(lambda x: pd.Timedelta(x, unit='D')) + output_trainer.end_hour.apply(lambda x: pd.Timedelta(x, unit='H'))
        output_trainer['End Date'] = output_trainer['End Date'] + pd.Timedelta(1, unit='H')
        output_trainer['Skill'] = SKILL

        output_trainer = output_trainer[['id_trainer','Start Date','End Date','Skill']]

        output_trainer = output_trainer.merge(df_member_trainer,on='id_trainer',how='left').rename(columns={'Trainer':'Team Member'})[['Team Member','Start Date','End Date','Skill']]

        output_trainer.sort_values(['Team Member', 'Start Date'])



        output_trainer.to_csv(f'export_folder/skill{NUM}_trainer.csv',index=False)



    output_trainee









    df_trainer = None
    df_trainee = None
    for i in range(len(list_skill)):
        if(i == 0):
            df_trainer = pd.read_csv(f'export_folder/skill{i}_trainer.csv')
            df_trainee = pd.read_csv(f'export_folder/skill{i}_trainee.csv')
        else:
            df_trainer = pd.concat([df_trainer, pd.read_csv(f'export_folder/skill{i}_trainer.csv')])
            df_trainee = pd.concat([df_trainee, pd.read_csv(f'export_folder/skill{i}_trainee.csv')])

    df_trainer.reset_index(drop=True).to_csv('export_folder/trainer.csv', index = False)
    df_trainee.reset_index(drop=True).to_csv('export_folder/trainee.csv', index = False)
        

    output_json = {}


    from pandas.io.json import json_normalize
    import json
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

    df_trainee

    df_trainee.columns = ['TeamMember', 'StartDate', 'EndDate', 'Skill', 'Trainer']

    df_trainee

    TrainerID = MemberID.copy()

    TrainerID

    # trainee_json = 
    TrainerID = MemberID.copy()
    TrainerID.columns = ['TrainerID', 'Trainer']
    trainee_json = df_trainee.merge(MemberID, how = 'left').merge(SkillID, left_on = 'Skill', right_on = 'Skills').merge(TrainerID)[['TeamMemberID', 'SkillID', 'TrainerID', 'StartDate', 'EndDate']]

    trainee_json.columns = ["Team_Member", "Task_ID", "Trainer_ID", "Start_Date", "End_Date"]

    trainee_json = trainee_json.to_dict('records')

    df_trainer.columns = ['TeamMember', 'StartDate', 'EndDate', 'Skills']
    trainer_json = df_trainer.merge(MemberID).merge(SkillID)[['TeamMemberID', 'StartDate', 'EndDate', 'SkillID']]


    trainer_json.columns = ["Team_Member", "Start_Date", "End_Date", "Task_ID"]

    trainer_json = trainer_json.to_dict('records')

    output_json['Trainee'] = trainee_json
    output_json['Trainer'] = trainer_json

    with open('export_folder/output_json.json', 'w') as outfile:
        json.dump(output_json, outfile)
    return True

def post_result():
    import json
    import requests
    import joblib
    scenario_id = joblib.load('scenario_id.pkl')
    # url = 'https://trainerplusapi.blueskycreations.com.au/api/traininghours'
    url = f'https://trainerplusapi.blueskycreations.com.au/api/traininghours?scenario_id={scenario_id}&=#'
    print(url)
    json_header = {
        # "Content-Type" :"application/json", 
        "apikey" :"N!k3!Bl^ESKY!INT@DGRVHB", 
    }
    file = open("export_folder/output_json.json", "r")
    contents = file. read()
    file. close()
    input_json = json.loads(contents)

    body = input_json

    print(body)
    x = requests.post(url, headers = json_header, json = body)
    print(x)
    print("DONE")
    return True
# solve()
# post_result()