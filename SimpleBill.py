import csv
import operator
from Payment import Payment
from User import User
from decimal import Decimal
import heapq
import queue

def main():
    print("test main function")

def readFromCSV():

    payments = []
    users = {}
    total_days = 0;

    with open('data/PaymentDetails.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        #print(', '.join(header))
        for row in reader:
            #print(', '.join(row))
            payments.append(Payment(row[1], row[2], float(row[3]), row[4]))

    with open('data/UserInfo.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        # print(', '.join(header))
        for row in reader:
            print(', '.join(row))
            total_days += int(row[4])
            users[row[1]] = User(row[1], int(row[4]))

    #print("days", total_days)
    return payments, users, total_days

def writeToCSV(results):


    with open('result.csv', mode='w', encoding='utf-8') as f:
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
    # print("member's total:", members)
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

    # print(" cc 's total spend total is", users['cc'].total_paid)
    # print(" mk 's total spend total is", users['mk'].total_paid)
    # print("Group total:", group_cost)
    # print("days_total", days_cost)

    per_day_spend = round(days_cost/total_days, 2)
    pre_person_spend = round(group_cost/members, 2)

    need_paid_list = {}
    need_recieve_list = {}

    pay_q = queue.PriorityQueue()
    recieve_q = queue.PriorityQueue()

    for username in users.keys():
        user = users[username]
        user.total_spend = pre_person_spend + per_day_spend * user.days
        users[username] = user
        #print("user,", username, "spend,", user.total_spend)
        if user.total_paid - user.total_spend > 0.00:
            recieve_q.put(((user.total_paid - user.total_spend) * (-1), username))
            # heapq.heappush(recieve_q, (user.total_paid - user.total_spend, username))

        if user.total_paid - user.total_spend < 0.00:
            pay_q.put(((user.total_spend - user.total_paid) * (-1), username))
            # heapq.heappush(pay_q, (user.total_spend - user.total_paid, username))
        print("UserInfo Summary: UserName", user.user, ", Days", user.days, ", Paid", user.total_paid, ", Cost", user.total_spend)

    # test calculate
    # pay_q.put((-300, 'mk'))
    # pay_q.put((-250, 'filex'))
    # pay_q.put((-100, 'xiaomeng'))
    # pay_q.put((-100, 'a1'))
    #
    # print(pay_q)
    #
    # recieve_q.put((-350, 'cc'))
    # recieve_q.put((-200, 'wr'))
    # recieve_q.put((-200, 'b1'))
    #
    # print(recieve_q)

    results = []

    while not pay_q.empty() and not recieve_q.empty():
        pay_user = pay_q.get()
        # print('pay_user', pay_user)
        recieve_user = recieve_q.get()
        # print('recieve_user', pay_user)
        result = {}
        result['UserName'] = pay_user[1]
        result['PayTo'] = recieve_user[1]
        pay_user_value = pay_user[0] * (-1)
        recieve_user_value = recieve_user[0] * (-1)
        if pay_user_value - recieve_user_value > 0:
            result['Value'] = Decimal(recieve_user_value).quantize(TWOPLACES)
            pay_q.put(((pay_user_value - recieve_user_value) * (-1), pay_user[1]))

        if pay_user_value - recieve_user_value < 0:
            result['Value'] = Decimal(pay_user_value).quantize(TWOPLACES)
            recieve_q.put(((recieve_user_value - pay_user_value) * (-1), recieve_user[1]))

        if pay_user_value - recieve_user_value == 0:
            result['Value'] = Decimal(pay_user_value).quantize(TWOPLACES)

        if result:
            results.append(result)

    while not pay_q:
        pay_user = pay_q.get()
        print("Left pay list", pay_user)

    while not recieve_q:
        recieve_user = recieve_q.get()
        print("Left recieved list", recieve_user)

    print(results)

    writeToCSV(results)