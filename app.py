from flask import Flask, render_template, Response, flash
import oracledb, json
from forms import InsertForm, UpdateForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '0cec7269e18377df34adfe2ca569ff2a'

@app.route('/')
def index():
    depts, cur, con = getAllDepts()
    return(render_template('index.html', depts=depts, cur=cur, con=con))

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    form = InsertForm()
    rows = []
    if form.validate_on_submit():
        curs = insertDept(form.deptid.data, form.deptname.data, form.city.data)
        for row in curs:
            rows.append(row)
        flash('Department creation in progress for '+str(form.deptid.data), 'success')
    return(render_template('insert.html', form=form, rows=rows))

@app.route('/update', methods=['GET', 'POST'])
def update():
    form = UpdateForm()
    previous_record = []
    rows = []
    if form.validate_on_submit():
        dept_list = getDept(form.deptid.data)
        if len(dept_list)>0:
            previous_record = dept_list
            curs = updateDept(form.deptid.data, form.deptname.data, form.city.data)
            for row in curs:
                rows.append(row)
            flash('Department update in progress for '+str(form.deptid.data), 'success')
        else:
            flash('Department Does not exist! '+str(form.deptid.data), 'fail')
    return(render_template('update.html', form=form, previous_record=previous_record, new_record=rows))

# Credentials change with every system
v_username = "SYS"
v_password = "123"
v_host = "localhost"
v_sid = "xe"
v_port = 1521
v_mode = oracledb.AUTH_MODE_SYSDBA 


def get_connection():
    conn = oracledb.connect(
            user=v_username, 
            password=v_password, 
            host=v_host, 
            sid=v_sid, 
            port=v_port, 
            mode=oracledb.AUTH_MODE_SYSDBA
        )
    return conn

def get_cursor(conn):
    return conn.cursor()

def execute_query(query, curs, insert_update_flag = False):
    curs.execute(query)
    if insert_update_flag:
        curs.execute("commit")
    return curs


def getAllDepts():
    dept_list = []
    conn = get_connection()
    curs = get_cursor(conn)
    curs = execute_query(
        "SELECT * FROM depts", 
        curs
    )
    for row in curs:
        dept_list.append(row)
    curs.close()
    conn.close()
    print(dept_list)
    return dept_list, curs, conn

def getDept(dept_id):
    dept_list = []
    conn = get_connection()
    curs = get_cursor(conn)
    query = "SELECT * FROM depts WHERE deptid=\'" + dept_id + "\'"
    curs = execute_query(
        query, 
        curs
    )
    for row in curs:
        dept_list.append(row)
    curs.close()
    conn.close()
    return dept_list

def updateDept(dept_id, dept_name, dept_location):
    conn = get_connection()
    curs = get_cursor(conn)
    query = "UPDATE depts SET dname = \'"+ dept_name + "\', city = \'"+ dept_location + "\' WHERE deptid=\'" + dept_id + "\'"
    curs = execute_query(
        query, 
        curs,
        True
    )
    curs = execute_query(
        "SELECT * FROM depts WHERE deptid = \'"+dept_id+"\'",
        curs
    )
    for row in curs:
        print(row)
    curs.close()
    conn.close()
    return row

def insertDept(dept_id, dept_name, dept_location):
    conn = get_connection()
    curs = get_cursor(conn)
    query = "insert into depts values(\'"+ dept_id +"\', \'"+ dept_name + "\', \'"+ dept_location + "\')"
    print(query)
    curs = execute_query(
        query, 
        curs,
        True
    )
    curs = execute_query(
        "SELECT * FROM depts WHERE deptid = \'"+dept_id+"\'",
        curs
    )
    for row in curs:
        print(row)
    curs.close()
    conn.close()
    return row

if __name__=='__main__':
    app.run(debug=True, port = 5501)