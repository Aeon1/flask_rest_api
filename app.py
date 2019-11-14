from flask import Flask,jsonify,request,render_template,Response
import psycopg2
import json

token ='Basic Sm9lbC5yaXZlcmE6Sm9lbFJfMjAxNw=='
app = Flask(__name__)
app.debug = False
def db(type,query,parametros):
    #abrir conexcion con postgres
    conn = psycopg2.connect(database='flask',user='postgres',password='rivera1556', host='flask.cvihq7dsqvir.us-east-2.rds-preview.amazonaws.com')
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    try: 
        if type == 'insert':
            try:
                cur.executemany(query,parametros)
                return jsonify(Respuesta={'success':'Operacion exitosa'})
            except:
                return jsonify(Respuesta={'error':'Ocurrio un error'})
        elif type == 'select':
            
            try:
                cur.execute(query)
                return jsonify(Respuesta=cur.fetchall())
            except:
                return jsonify(Respuesta={'error':'Ocurrio un error'})
        elif type == 'update':
            try:
                cur.execute(query)
                return jsonify(Respuesta={'success':'Operacion exitosa'})
            except:
                return jsonify(Respuesta={'error':'Ocurrio un error'})
        elif type == 'delete':
            try:
                cur.execute(query)
                return jsonify(Respuesta={'success':'Operacion exitosa'})
            except:
                return jsonify(Respuesta={'error':'Ocurrio un error'})

    except:
        return jsonify(Respuesta={'error':'Ocurrio un error'})
    
    

@app.route('/')
def index():
    return render_template('index.html')
    #return "funciona"
@app.route('/agregar',methods = ['POST'])
def insertar():    
    if request.headers['Authorization'] == token:
        data = request.json
        datos=[]
        for c in data:
            datos.append((c['nombre'],c['fecha_nacimiento'],c['puesto']))
        return db('insert' ,"""insert into personas(nombre,fecha_nacimiento,puesto) 
                values (%s,%s,%s)""",datos)
    else:
        return jsonify(Respuesta={'error':'Token invalido'})

@app.route('/ver',methods = ['GET'])
def mostrar():
    if request.headers['Authorization'] == token:
        limite = request.args.get('limit')
        iden = request.args.get('id')
        nombre = request.args.get('nombre')
        puesto = request.args.get('puesto')
        total=''
        if limite:
            total = "limit({})".format(limite)
        datos={}
        if iden:
            datos["id"] = int(request.args.get('id'))
        if nombre:
            datos["nombre"] = request.args.get('nombre')
        if puesto:
            datos["puesto"] = request.args.get('puesto')
        datos=json.dumps(datos)
        return db('select',"""with datos as (SELECT to_json(p.*) as jsons FROM personas p)
                select jsons from datos where jsons::jsonb @> '{}'::jsonb {}""".format(datos,total),'')
    else:
        return jsonify(Respuesta={'error':'Token invalido'})

@app.route('/modificar',methods = ['PUT'])
def modificar():
    if request.headers['Authorization'] == token:
        datos = request.json
        dat=''
        idx=''
        for x in datos[0]:    
            if x=='id':
                idx=datos[0][x]
            else:
                if dat!='':
                    dat +=", "
                dat += "{}='{}'".format(x,datos[0][x])
        return db('update',"update personas set {} where id = {}".format(dat,idx),'')
    else:
        return jsonify(Respuesta={'error':'Token invalido'})

@app.route('/eliminar',methods = ['DELETE'])
def eliminar():
    idx = request.args.get('id')
    print(idx)
    return db('delete',"delete from personas where id = {}".format(idx),'')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)