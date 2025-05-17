import curses
import datetime
from re import search
from classes import User, Admin, Project, UserAndProjects, Task, UserAndTasks, Funcs, db
import validator_collection
def main(stdscr):
    db.connect()
    db.create_tables([User, Project, UserAndProjects, Task, UserAndTasks])
    admin = Admin()
    user = None
    now = datetime.datetime.today()
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
                assert username.lower() != 'admin'
                user = User.create(username = username,password = password,first_name = first_name,last_name = last_name,email = email,department = department)
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
        if inp == 'N' or inp == 'n':
            Funcs.addProject(stdscr,user)
        elif inp == 'P' or inp == 'p':
            project = Funcs.selectProject(stdscr,user)
            while True:
                try:
                    string = f'name: {project.name}\nmanager: {project.manager}\ndepartment: {project.department}\npeople:'
                    people = list(UserAndProjects.select().where(UserAndProjects.project == project))
                    for _ in people:
                        string += f' {_.user.username}'
                    string += '\n[E] edit project and add new tasks / [B] go back'
                    key = Funcs.getinp(stdscr,string,1)
                except:
                    break
                if key == 'E' or key == 'e':
                    Funcs.editProject(stdscr,user,project)
                elif key == 'B' or key == 'b':
                    break
        elif inp == 'T' or inp == 't':
            task = Funcs.selectTask(stdscr,user)
            while True:
                try:
                    string = f'name: {task.name}\ncreated date: {task.created_date}\ndeadline: {task.deadline}\nstatus: {task.status}\ndescription: {task.description}\nproject: {task.project.name}\npeople:'
                    people = list(UserAndTasks.select().where(UserAndTasks.task == task))
                    for _ in people:
                        string += f' {_.user.username}'
                    string += '\n[E] edit task / [B] go back'
                    key = Funcs.getinp(stdscr,string,1)
                except:
                    break
                if key == 'B' or key =='b':
                    break
                elif key == 'E' or key =='e':
                    Funcs.editTask(stdscr,task,user)
        elif inp == 'F' or inp == 'f':
            while True:
                key = Funcs.getinp(stdscr,'what do you want to search for: [T] task / [P] project / [U] user',1)
                if key == 'T' or key == 't' or key == 'P' or key == 'p' or key == 'U' or key == 'u':
                    break
            if key == 'T' or key == 't':
                search = Funcs.getinp(stdscr,'task name :')
                tasks = list(Task.select())
                stdscr.clear()
                for _ in tasks:
                    if search in _.name:
                        stdscr.addstr(_.name + '\n')
                stdscr.addstr('[B] go back')
                stdscr.refresh()
                while key != 'B' and key != 'b':
                    key = stdscr.getkey()
            elif key == 'P' or key == 'p':
                
                search = Funcs.getinp(stdscr,'project name :')
                projects = list(Project.select())
                stdscr.clear()
                for _ in projects:
                    if search in _.name:
                        stdscr.addstr(_.name + '\n')
                stdscr.addstr('[B] go back')
                stdscr.refresh()
                while key != 'B' and key != 'b':
                    key = stdscr.getkey()
            elif key == 'U' or key == 'u':
                
                search = Funcs.getinp(stdscr,'username :')
                if search == 'admin':
                    stdscr.clear()
                    stdscr.addstr(f'{admin.username}\'s number: {admin.call_number}')
                    stdscr.refresh()
                    while key != 'B' and key != 'b':
                        key = stdscr.getkey()
                else:
                    users = list(User.select())
                    stdscr.clear()
                    for _ in users:
                        if search in _.username:
                            stdscr.addstr(_.username + '\n')
                    stdscr.addstr('[B] go back')
                    stdscr.refresh()
                    key = None
                    while key != 'B' and key != 'b':
                        key = stdscr.getkey()
        else:
            break





if __name__ == '__main__':
    curses.wrapper(main)