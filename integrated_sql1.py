from flask import Flask,request,jsonify
import json
import pymysql

app=Flask(__name__)

def db_connection():
    conn=None
    try:
        conn=pymysql.connect(
        host="sql12.freesqldatabase.com",
        database = 'sql12675979',
        user= 'sql12675979',
        password='Rf1SP8BSqG',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor

        )
    except pymysql.Error as e :
        print(e)

    return conn

@app.route('/book',methods=['GET','POST'])

def books():
    conn=db_connection()
    cursor=conn.cursor()

    if request.method=="GET":
        cursor.execute("select * from book")
        books=None
        books=[
            dict(id=row['id'], author=row['author'],language=row['language'],title=row['title'])
            for row in cursor.fetchall()
        ]
        if books is not None:
            return jsonify(books),200

    if request.method=='POST':
        #
        new_author=request.form['author']
        new_lang=request.form['language']
        new_title=request.form['title']
        # Assuming your SQL query is something like this:
        sql1 = "INSERT INTO book (author, language, title) VALUES (%s, %s, %s)"

# Make sure to provide a tuple as the second argument to execute:
        cursor.execute(sql1, (new_author, new_lang, new_title))

        conn.commit()
        return f"Book with id :{cursor.lastrowid} created successfully",201

@app.route("/book/<int:id>",methods=["GET","PUT","DELETE"]) 
def single_book(id):
    conn=db_connection()
    cur=conn.cursor()
    if request.method=="GET":
        sql=f"""
select * from book where id ={id}
"""     
        cur.execute("select * from book where id=%s",(id,))
        rows= cur.fetchall()
        book=None
        for r in rows:
            book =r
        #cursor=cur.execute(sql)
        # book=[
        #     dict(id=row[0],author=row[1],language=row[2],title=row[3])
        #     for row in cursor.fetchall()
        # ]
        if book is not None:
            return jsonify(book),201
        else:
            return "Something Wrong",404
    if request.method=='PUT':
        sql=''' update book set title =%s,author=%s,language=%s where id=%s'''
        author=request.form['author']
        title=request.form['title']
        language=request.form['language']
        updated_book={
            "id":id,
            "author":author,
            "language":language,
            "title":title,
        }
        cur.execute(sql,(title,author,language,id))
        conn.commit()
        return jsonify(updated_book)
    if request.method=="DELETE":
        sql=''' delete from book where id=%s'''
        cur.execute(sql,(id,))
        conn.commit()
        return f"The book with id {id} has been deleted",200
if __name__=="__main__":
    app.run()
