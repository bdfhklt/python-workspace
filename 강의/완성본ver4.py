import re,pickle,os,sys

class Customer:
    custlist=[]
    page = -1
    
    def insertData(self): 
        customer={'name':'','sex':'','email':'','birthyear':''}
        customer['name']=str(input("이름을 입력하세요 : "))
            
        while True:
                customer['sex']=str(input("성별(M/m 또는 F/f)을 입력하세요 : "))
                customer['sex']=customer['sex'].upper()
                if customer['sex'] in ('M','F'):
                    break
                else:
                    print('M/m 또는 F/f 중 입력해주세요')

        while True: 
            regex = re.compile('^[a-z][a-z0-9]{4,10}@[a-zA-Z]{2,6}[.][a-zA-Z]{2,3}$')
            while True:
                customer['email']=input("이메일을 입력하세요 : ") 
                golbang = regex.search(customer['email'])
                if golbang:
                    break
                else:
                    print('"@"를 포함한 정확한 이메일을 써주세요')

            check=0
            for i in self.custlist:
                if i['email']==customer['email']:
                    check=1
            
            if check==0:
                break
            print('중복되는 이메일이 있습니다.')   

        while True:
            customer['birthyear']=input("출생년도 4자리를 입력해주세요 : ")
            
            if len(customer['birthyear']) == 4 and customer['birthyear'].isdigit():
                break

        print(customer)
        self.custlist.append(customer)
        print(self.custlist)
        self.page = len(self.custlist)-1 
        print(self.page)   
        
    def curSearch(self):
        if self.page >= 0:
            print("현재 페이지는 {}쪽 입니다".format(self.page + 1)) 
            print(self.custlist[self.page])
        else:
            print("입력된 정보가 없습니다.") 

    def preSearch(self):
        if self.page <= 0:
            print('첫 번 째 페이지이므로 이전 페이지 이동이 불가합니다')
            print(self.page)
        else:
            self.page -= 1
            print("현재 페이지는 {}쪽 입니다".format(self.page + 1))
            print(self.custlist[self.page])

    def nextSearch(self):
        if self.page >= len(self.custlist)-1:
            print('마지막 페이지이므로 다음 페이지 이동이 불가합니다')
            print(self.page)
        else:
            self.page += 1
            print("현재 페이지는 {}쪽 입니다".format(self.page + 1))
            print(self.custlist[self.page])

    def deleteData(self):
        choice1 = input('삭제하려는 고객 정보의 이메일을 입력하세요.')
        delok = 0
        for i in range(0,len(self.custlist)):
            while self.custlist[i]['email'] == choice1:
                print('{} 고객님의 정보가 삭제되었습니다.'.format(self.custlist[i]['name']))
                del self.custlist[i]
                print(self.custlist)
                self.page=len(self.custlist)-1   
                print(self.page)  
                delok = 1
                break
            
            if delok == 1:
                break

        if delok == 0:
                print('등록되지 않은 이메일입니다.')

    def updateData(self): 
        while True:
            choice1=input('수정하시려는 고객 정보의 이메일을 입력하세요 : ')
            idx=-1
            for i in range(0,len(self.custlist)):
                if self.custlist[i]['email'] == choice1:
                    idx=i
            if idx==-1:
                print('등록되지 않은 이메일입니다.')       
                break
                        
            choice2=input('''
            다음 중 수정하실 정보를 골라주세요 
                    name, sex, birthyear
            (수정할 정보가 없으면 'exit' 입력)
            ''')
            if choice2 in ('name','sex','birthyear'):
                self.custlist[idx][choice2]=input('수정할 {}을 입력하세요 :'.format(choice2))
                break
            elif choice2 =='exit':
                break
            else:
                print('존재하지 않는 정보입니다.')
                break

    def quit(self):
        print("프로그램을 종료합니다.")
        self.saveData()
        sys.exit()

    def saveData(self):
        with open('./customer/data.pkl','wb') as f:
            pickle.dump(self.custlist,f)
       
    def loadData(self):
        #파일 크기가 0보다 클 경우에  읽어옴.
        #if os.path.getsize('./customer/data.pkl')>0: 
        #파일이 존재할 경우에 읽어옴.
        if os.path.exists('./customer/data.pkl'):    
            with open('./customer/data.pkl','rb') as f:
                self.custlist=pickle.load(f)
                self.page=len(self.custlist)-1

    def fullSearch(self):
        print("- 전체 고객 리스트 -")
        for i in self.custlist:
            print(i)

    def firstinput(self):
            choice=input('''
                다음 중에서 하실 일을 골라주세요 :
                I - 고객 정보 입력
                C - 현재 고객 정보 조회
                P - 이전 고객 정보 조회
                N - 다음 고객 정보 조회
                F - 전체 고객 정보 조회
                U - 고객 정보 수정
                D - 고객 정보 삭제
                S - 저장
                Q - 프로그램 종료
                ''').upper()  
            return choice

    def exe(self,choice):
            if choice=='I':
                self.insertData()
                
            elif choice=='C':
                self.curSearch()
            
            elif choice=='P':
                self.preSearch()

            elif choice=='N':
                self.nextSearch()

            elif choice=='F':
                self.fullSearch()

            elif choice=='U':
                self.updateData()
            
            elif choice=='D':
                self.deleteData()

            elif choice=='S':
                self.saveData()    
            
            elif choice=='Q':
                self.quit()

    def __init__(self):
        self.loadData()
        while True:
            self.exe(self.firstinput())
                
Customer()
