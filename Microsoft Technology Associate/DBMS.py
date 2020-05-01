# Title: DBMS
# Author: Ananya G M, K Nitesh Srivats
# Date: 01/06/2018

import pandas as pd
import os


def get_path():
    logs_path = os.getcwd()
    database_path = ""
    form_path = ""
    new_database_path = ""
    ieee_path = ""

    path = os.path.join(logs_path, 'Database Main.xlsx')

    for i in range(len(path)):
        if path[i] == '\\':
            database_path += '/'
        else:
            database_path += path[i]

    path = os.path.join(logs_path, 'Form.csv')

    for i in range(len(path)):
        if path[i] == '\\':
            form_path += '/'
        else:
            form_path += path[i]

    path = os.path.join(logs_path, 'MTA-BMS.xlsx')

    for i in range(len(path)):
        if path[i] == '\\':
            new_database_path += '/'
        else:
            new_database_path += path[i]

    path = os.path.join(logs_path, 'members.xlsx')

    for i in range(len(path)):
        if path[i] == '\\':
            ieee_path += '/'
        else:
            ieee_path += path[i]

    return database_path, form_path, new_database_path, ieee_path


def mail_counter(choice):
    database_path, form_path, new_database_path, ieee_path = get_path()

    form = pd.read_csv(form_path)
    data = pd.read_excel(database_path)

    for i in range(len(data)):
        if data["Payment ID"].iloc[i] not in form["Payment ID"].tolist() \
                and data["Mail Count"].iloc[i] < 2:

            if data["Amount"].iloc[i] != 15000 and choice == 1:
                data["Mail Count"].iloc[i] += 1
            elif data["Amount"].iloc[i] == 15000 and choice == 2:
                data["Mail Count"].iloc[i] += 1

    data.to_excel(database_path, index=False)


def update_from_db():
    database_path, form_path, new_database_path, ieee_path = get_path()
    data = pd.read_excel(database_path)

    try:
        new = pd.read_csv(new_database_path)
    except FileNotFoundError:
        new = pd.read_excel(new_database_path)

    new = new.rename(columns={"Customer Email": "Username",
                              "Customer Phone": "Phone number",
                              "Payment Id": "Payment ID"})

    for i in range(len(new)):
        if new["Payment ID"].iloc[i] not in data["Payment ID"].tolist():
            data = data.append(new.iloc[i])

    data.fillna(0, inplace=True)
    data.to_excel(database_path, index=False)


def update_from_form():
    database_path, form_path, new_database_path, ieee_path = get_path()
    data = pd.read_excel(database_path)
    data.fillna(0, inplace=True)

    try:
        form = pd.read_csv(form_path)
    except FileNotFoundError:
        form = pd.read_excel(form_path)
    form.fillna(0, inplace=True)
    form.drop(['Are you an IEEE member?'], axis=1, inplace=True)

    for i in range(len(form)):
        for j in range(len(data)):
            if form["Payment ID"].iloc[i] == data["Payment ID"].iloc[j] \
                    and data["Name"].iloc[j] == 0:

                data["Name"].iloc[j] = form["Name"].iloc[i]
                data["Date of birth"].iloc[j] = form["Date of birth"].iloc[i]
                data["IEEE Membership ID"].iloc[j] = form["IEEE Membership ID"].iloc[i]
                data["College"].iloc[j] = form["College"].iloc[i]
                data["Branch"].iloc[j] = form["Branch"].iloc[i]
                data["Year of study"].iloc[j] = form["Year of study"].iloc[i]
                data["Timestamp"].iloc[j] = form["Timestamp"].iloc[i]
                data["Username"].iloc[j] = form["Username"].iloc[i]
                data["Phone number"].iloc[j] = form["Phone number"].iloc[i]
                break

            elif (form["Payment ID"].iloc[i] == data["Payment ID"].iloc[j] and
                  data["Amount"].iloc[j] == 15000) or \
                    form["Payment ID"].iloc[i] == 0:

                data = data.append(form.iloc[i])
                break 

    data.to_excel(database_path, index=False)


def display_data(choice):
    database_path, form_path, new_database_path, ieee_path = get_path()
    data = pd.read_excel(database_path)
    display = pd.DataFrame(columns=['Name', "Email", "Phone Number", 'ID'])

    for i in range(len(data)):
        if data["Amount"].iloc[i] != 15000 and choice == 1:
            display = display.append(
                pd.DataFrame([[data["Name"].iloc[i],
                               data["Username"].iloc[i],
                               data["Phone number"].iloc[i],
                               data["IEEE Membership ID"].iloc[i]]],
                             columns=['Name', "Email", "Phone Number", 'ID']
                             ))
        elif data["Amount"].iloc[i] == 15000 and choice == 2:
            display = display.append(
                pd.DataFrame([[data["Name"].iloc[i],
                               data["Username"].iloc[i],
                               data["Phone number"].iloc[i],
                               data["Payment ID"].iloc[i]]],
                             columns=['Name', "Email", "Phone Number", 'ID', ]))
    display = display.sort_values(["ID"], ascending=False)
    print(display)


def membership():
    database_path, form_path, new_database_path, ieee_path = get_path()
    data = pd.read_excel(database_path)
    ieee = pd.read_excel(ieee_path)
    check = pd.DataFrame(columns=['Name', 'ID', 'Name Given'])

    for i in range(len(data)):
        if data["IEEE Membership ID"].iloc[i] != 0:
            flag = 0
            for j in range(len(ieee)):
                if ieee["IEEE Membership Number"].iloc[j] == \
                        data["IEEE Membership ID"].iloc[i]:
                    name = ieee["First Name"].iloc[j] + ' ' + ieee["Last Name"].iloc[j]
                    check = check.append(
                        pd.DataFrame([[name,
                                       data["IEEE Membership ID"].iloc[i],
                                       data["Name"].iloc[i]]],
                                     columns=['Name', 'ID', 'Name Given']
                                     ))
                    flag = 1
                    break
            if flag == 0:
                check = check.append(
                    pd.DataFrame([[0,
                                   data["IEEE Membership ID"].iloc[i],
                                   data["Name"].iloc[i]]],
                                 columns=['Name', 'ID', 'Name Given']))
    logs_path = os.getcwd()
    write_path = ""
    path = os.path.join(logs_path, 'Check Membership.xlsx')

    for i in range(len(path)):
        if path[i] == '\\':
            write_path += '/'
        else:
            write_path += path[i]
    check.to_excel(write_path, index=False)


def main():
    while True:
        # os.system('cls')
        # clear for linux
        multi = -1
        while multi < 0 or multi > 5:
            multi = eval(input("1. Update from Database.\n"
                               "2. Update from Form.\n"
                               "3. Check memberships.\n"
                               "4. Display.\n"
                               "0. Exit."))
        if multi == 1:
            update_from_db()
        elif multi == 2:
            update_from_form()
        elif multi == 3:
            membership()
        elif multi == 4:
            choice = -1
            while choice != 2 and choice != 1:
                choice = eval(input("\n1. Individual.\n2. Group."))
                display_data(choice)
        else:
            return


if __name__ == "__main__":
    main()
