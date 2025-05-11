import curses
from classes import User, Admin, Project, UserAndProjects, Task, UserAndTasks, Funcs, db
import validator_collection
def main(stdscr):
    db.connect()
    db.create_tables([User, Project, UserAndProjects, Task, UserAndTasks])
    admin = Admin()
    user = None
    while True:
        inp = Funcs.getinp(stdscr,'[L] log in / [S] sign up',1)
        if inp == 'L' or inp == 'l' or inp == 'S' or inp == 's':
            break
    while True:
        if inp == 'S' or inp == 's':
            username = Funcs.getinp(stdscr,'Username :')
            password = Funcs.getinp(stdscr,'Password :')
            first_name = Funcs.getinp(stdscr,'First Name :')
            last_name = Funcs.getinp(stdscr,'Last Name :')
            email = Funcs.getinp(stdscr,'Email :')
            department = Funcs.getinp(stdscr,'Department :')
            try:
                assert validator_collection.is_email(email)
                user = User(username = username,password = password,first_name = first_name,last_name = last_name,email = email,department = department)
                user.save()
                break
            except:
                pass
        else:
            username = Funcs.getinp(stdscr,'Username :')
            password = Funcs.getinp(stdscr,'Password :')
            if username == admin.username and password == admin.password:
                user = admin
                break
            else :
                try:
                    user = User.get(User.username == username)
                    assert  user.password == password
                    break
                except:
                    user = None
    while True:
        while True:
            inp = Funcs.getinp(stdscr,'[N] create new project / [P] view all projects / [T] view all tasks / [F] find a project or task / [E] exit',1)
            if inp == 'N' or inp == 'n' or inp == 'P' or inp == 'p' or inp == 'T' or inp == 't' or inp == 'F' or inp == 'f'  or inp == 'E' or inp == 'e':
                break
        if inp == 'N' or inp == 'n':#TODO just make a project
            ...
        elif inp == 'P' or inp == 'p':#TODO select a project , edit it and veiw related tasks
            ...
        elif inp == 'T' or inp == 't':#TODO select a task , edit it
            ...
        elif inp == 'F' or inp == 'f':#TODO look up projects/tasks that you arent involved in
            ...
        else:
            break





if __name__ == '__main__':
    curses.wrapper(main)