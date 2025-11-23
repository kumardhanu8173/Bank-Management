from pathlib import Path
import json
import random
import string


class Bank:
    database='datbase.json'
    data=[]

    try: 
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("Sorry we are facing some issues: ")

    except Exception as err:
        print(f"An error occured as {err}")

    @classmethod
    def __update(cls):
        with open(cls.database,'w') as fs:
            fs.write(json.dumps(cls.data))
    
    @staticmethod
    def __accountno():
        alpha=random.choices(string.ascii_letters,k=5)
        digits=random.choices(string.digits,k=4)
        id=alpha+digits
        random.shuffle(id)
        return "".join(id)
    
    def create_account(self):
        d={
            "name":input("Please enter your name: "),
            "email":input("Please enter your email: "),
            "phone no.":int(input("Enter your phone number: ")),
            "pin":int(input("Enter your pin: ")),
            "Account no.":Bank.__accountno(),
            "Balance": 0
                            
        }
        print(f"Please remember your account number: {d['Account no.']}")

        if len(str(d['pin']))!=4:
            print("Please review your pin!")
        
        elif len(str(d['phone no.']))!=10:
            print("Please review your phone number!")

        else:
            Bank.data.append(d)
            Bank.__update()


    def deposite_money(self):
        accNo = input("Enter your account no.: ")
        pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        print(user_data)
        if not user_data:
            print("user not found")
        else:
            amount = int(input("Enter amount to be deposited: "))
            if amount <= 0:
                print("Invalid amount")
            elif amount > 10000:
                print("Greater than 10000")
            else:
                user_data[0]['Balance'] += amount
                Bank.__update()
                print("Amount credited")

    def withdraw_money(self):
        accNo = input("Enter your account no.: ")
        pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        print(user_data)
        if not user_data:
            print("user not found")
        else:
            amount = int(input("Enter amount to be withdrawn: "))
            if amount <= 0:
                print("Invalid amount")
            elif amount > 10000:
                print("Greater than 10000")
            else:
                user_data[0]['Balance']-=amount
                Bank.__update()
                print("Amount Debited")

    def details(self):
        accNo = input("Enter your account no.: ")
        pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            print("User not found!")
        else:
            for i in user_data[0]:
                print(f"{i}: {user_data[0][i]}")
     
    def update_details(self):
        accNo = input("Enter your account no.: ")
        pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            print("User not found!")
        else:
            print("You cannot change account number!")
            print("Now update your details and skip it if you dont want to")
            new_data={
                'name':input("Enter your new name: "),
                'email':input("Enter your new email:"),
                'phone no.':(input("Enter your new phone no.:")),
                'pin':(input("Enter your new pin:"))
            }

            new_data["Account no."]=user_data[0]["Account no."]
            new_data["Balance"]=user_data[0]["Balance"]
            #Handle the skipped values:

            for i in new_data:
                if new_data[i]=="":
                    new_data[i]=user_data[0][i]
            

            #We have to update new data to database:

            for i in user_data[0]:
                if user_data[0][i]==new_data[i]:
                    continue
                else:
                    if new_data[i].isnumeric():
                        user_data[0][i]=int(new_data[i])

                        

                    else:
                        user_data[0][i]=new_data[i]
              
            Bank.__update()
            print(user_data)  
            print("Details updated!")

    def delete_account(self):
        accNo = input("Enter your account no.: ")
        pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account no.'] == accNo and i['pin'] == pin]
        if not user_data:
            print("User not found!")
        else:
            for i in user_data:
                if i["Account no."] == accNo and i["pin"] == pin:
                    Bank.data.remove(i)
                    Bank.__update()

        print("Account deleted!")
            


user=Bank()
print("Press 1 for creating an account.")
print("Press 2 to deposite money.")
print("Press 3 to withdraw money.")
print("Press 4 for account details.")
print("Press 5 for updating the details.")
print("Press 6 to deactivate your account.")

check=int(input("Enter your coice: "))

if check==1:
    user.create_account()

if check==2:
    user.deposite_money()

if check==3:
    user.withdraw_money()

if check==4:
    user.details()

if check==5:
    user.update_details()

if check==6:
    user.delete_account()