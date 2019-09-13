import csv
import operator
from Payment import Payment
from User import User
from decimal import Decimal

def main():
    print("test main function")

def readFromCSV():

    payments = []
    users = {}
    total_days = 0;

    with open('data/payments.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        print(', '.join(header))
        for row in reader:
            print(', '.join(row))
            payments.append(Payment(row[1], row[2], float(row[3]), row[4]))

    with open('data/user.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        # print(', '.join(header))
        for row in reader:
            print(', '.join(row))
            total_days += int(row[4])
            users[row[1]] = User(row[1], int(row[4]))

    print("days", total_days)
    return payments, users, total_days

def writeToCSV(results):


    with open('result.csv', mode='w') as f:
        fieldnames = ['UserName', 'PayTo', 'Value']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)

if __name__ == "__main__":
    main()
    TWOPLACES = Decimal(10) ** -2

    payments, users, total_days = readFromCSV()
    members = len(users)
    print("member's total:", members)
    group_cost = 0
    days_cost = 0

    for payment in payments:
        if payment.user in users.keys():
            user = users[payment.user]
            user.total_paid += payment.paid_value
            users[payment.user] = user
        else:
            print("user :", payment.user, "is not existed")

        if payment.share_type == "Group":
            group_cost += payment.paid_value
        else:
            days_cost += payment.paid_value

    print(" cc 's total spend total is", users['cc'].total_paid)
    print(" mk 's total spend total is", users['mk'].total_paid)
    print("Group total:", group_cost)
    print("days_total", days_cost)

    per_day_spend = round(days_cost/total_days, 2)
    pre_person_spend = round(group_cost/members, 2)

    need_paid_list = {}
    need_recieve_list = {}

    pay_q = Q.PriorityQueue()

    for username in users.keys():
        user = users[username]
        user.total_spend = pre_person_spend + per_day_spend * user.days
        users[username] = user
        print("user,", username, "spend,", user.total_spend)
        if user.total_paid - user.total_spend > 0.00:
            need_recieve_list[username] = user.total_paid - user.total_spend

        if user.total_paid - user.total_spend < 0.00:
            need_paid_list[username] = user.total_spend - user.total_paid

    # test calculate
    need_paid_list = {'mk':200, 'filex': 150, 'xxx': 100, 'a1':100}
    need_recieve_list = {'cc': 400, 'wr': 100, 'xiaomeng': 50}


    need_paid_list = sorted(need_paid_list.items(), key=operator.itemgetter(1), reverse=True)
    need_recieve_list = sorted(need_recieve_list.items(), key=operator.itemgetter(1), reverse=True)

    print(need_paid_list)
    print(need_recieve_list)

    results = []

    for user, pay_value in need_paid_list.items():
        delta = pay_value
        for payto, recieve_value in need_recieve_list.copy().items():
            result = {}
            print('recieve_value,',recieve_value)
            if delta - recieve_value >= 0:
                result['UserName'] = user
                result['PayTo'] = payto
                result['Value'] = Decimal(recieve_value).quantize(TWOPLACES)
                delta -= recieve_value
                del need_recieve_list[payto]
                results.append(result)
                if delta == 0:
                    break
            else:
                result['UserName'] = user
                result['PayTo'] = payto
                result['Value'] = Decimal(delta).quantize(TWOPLACES)
                need_recieve_list[payto] = recieve_value - delta
                need_recieve_list = dict(sorted(need_recieve_list.items(), key=operator.itemgetter(1), reverse=True))
                results.append(result)
                break

    print(results)

    writeToCSV(results)