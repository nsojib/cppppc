from flask import Flask, render_template, request
import os
from flask import Response
import json
from flask import Flask, request, send_from_directory
import glob
import time

app = Flask(__name__,)

@app.route('/')
def draw():
   return render_template('index.html')

@app.route('/create')
def create_file():
   print('creating problem file') 
   pid=101
   pname='Kadums Love'
   pcat='basic'
   pinfo='Once upon a time there was a man named Kadum'
   pinput=[1,3,9]
   poutput=[44,55,11]
   success=save_a_problem(pid, pname, pcat, pinfo, pinput, poutput)
   return success

@app.route('/setaproblem', methods=['POST','GET'])
def setaproblem():
   files=glob.glob("problems/*", recursive=True)
   pid=len(files)+1
   success='False'
   if request.method == 'POST':
      data = request.form
      pname=data['pname']
      pcat=data['pcat']
      pinfo=data['pinfo']
      pinput=data['pinput']
      poutput=data['poutput']
      success=save_a_problem(pid, pname, pcat, pinfo, pinput, poutput)

   return render_template('info.html', title='success', info=success )

def save_a_problem(pid, pname, pcat, pinfo, pinput, poutput, setter='root'):
   problem={} 
   problem['id']=pid
   problem['name']=pname
   problem['cat']=pcat
   problem['info']=pinfo
   problem['input']=pinput
   problem['output']=poutput
   problem['setter']=setter
   fname='problems/'+str(time.time())+'.json'
   fname='problems/'+pcat+'_'+str(pid)+'.json'
   fname='problems/'+str(pid)+'.json'
   with open(fname, "w") as write_file:
      json.dump(problem, write_file, indent=4)
   return fname


@app.route('/login',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      uname=result['uname']
      pw=result['pass']
      if uname=='sojib' and pw=='sojib':
         return render_template('profile.html', uname=uname)
      return render_template('index.html')

def load_problems():
   problems=[]
   files=glob.glob("problems/*", recursive=True)
   for file in files: 
      with open(file) as f:
         problem= json.load(f)
         problems.append(problem)
   return problems

@app.route('/problemsadmin')
def problemsadmin():
   print('problem lists')
   problems=load_problems()
   datas={}
   for problem in problems:
      cat=problem['cat']
      if cat not in datas:
         datas[cat]=[]

      datas[cat].append({'id':problem['id'], 'name':problem['name']})
   
   s=''
   
   html_s = "<br><strong>Note:</strong> Edit Problems<br>"+ "<div class='panel-group' id='accordion'>"
   html_b = ""
   html_e = "</div>"
   for label,data in datas.items():
      s+=label+'_'+str(data)+'<br>'
      html_b += get_p_body(label, data, isexpand=False);
   
   s=html_s+html_b+html_e 
   return render_template('info.html', title='success', info=s )


@app.route('/problems')
def problems():
   print('problem lists')
   problems=load_problems()
   datas={}
   for problem in problems:
      cat=problem['cat']
      if cat not in datas:
         datas[cat]=[]

      datas[cat].append({'id':problem['id'], 'name':problem['name']})
   
   s=''
   
   html_s = "<br><strong>Note:</strong> Practice example for C Course!<br>"+ "<div class='panel-group' id='accordion'>"
   html_b = ""
   html_e = "</div>"
   for label,data in datas.items():
      s+=label+'_'+str(data)+'<br>'
      html_b += get_p_body(label, data, isexpand=False);
   
   s=html_s+html_b+html_e 
   return render_template('info.html', title='Problem List', info=s )

def get_p_body(label, plist, isexpand=False):
   special = "";
   if isexpand:
      special = " in"
   
   
   lb_b = ""
   lb_name = "Label: " + label
   lb_s = """<div class='panel panel-default'> 
   <div class='panel-heading'> 
   <h4 class='panel-title'> 
   <a data-toggle='collapse' data-parent='#accordion' href='#collapse""" + label + """'> """ + lb_name + """</a> 
   </h4> 
    </div> 
   <div id='collapse""" + label + """' class='panel-collapse collapse""" + special + """'> 
   <div class='panel-body'> 
   <div class='list-group'>"""
   
   lb_e = "</div> </div> </div> </div>"

   for data in plist:
      id=str( data['id'] )
      name=data['name']
      lb_b += "<a href='/page/" +id + "' class='list-group-item'> <h4>#" + id + ": " + name + "</h4></a>"


   return lb_s + lb_b + lb_e


@app.route('/problemsetter')
def problem():
   return render_template('setproblem.html')

# @app.route('/<path:path>')
# def send_js(path):
#     return send_from_directory('', path)


@app.route('/page/<pid>')
def page(pid): 
   fname='problems/'+str(pid)+'.json'
   if not os.path.isfile(fname):
      return render_template('info.html', title='failed', info='problem id '+str(pid)+' not found!')

   with open(fname) as f:
         problem= json.load(f)

   pid=problem['id']
   uname='sojib'
   title=problem['name']
   info=problem['info']
   input=problem['input']
   output=problem['output']
   return render_template('page_template.html', pid=pid, uname=uname, title=title, info=info, input=input, output=output)





if __name__ == '__main__': 
	# app.run(debug=True)
   app.run(host='0.0.0.0')
	