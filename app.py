import os
from flask import Flask, render_template, request, session, send_from_directory, render_template_string


app = Flask(__name__, template_folder="template")

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024

links=[]

@app.route('/', methods=["POST", "GET"])
def upload():
    if request.method=="POST":
      file = request.files['uploadedFile']
      if file and file.filename:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        print ("saved to"+filepath)
      link=request.form["uploadLink"]
      if link:
          links.append(link)
    return render_template("UploadFile.html")

@app.route ('/uploaded')
def uploaded():
    folder=os.listdir(app.config["UPLOAD_FOLDER"])
    fileList=[f for f in folder if os.path.isfile(os.path.join(app.config["UPLOAD_FOLDER"],f))]
    return render_template_string("""<h1> there is {{num}} files
    <ul>
    {%for file in folder %}
      <li>{{file}} - 
        <a href="{{url_for('findFile', filename=file)}}">download</a>
    {%endfor%}
    </ul>
    <h1>here are links: </h1>
    <ul>
    {%for l in links%}
      <li>{{l}}</li>
    {%endfor%}
    </ul>
    """, folder=fileList, num=len(fileList))

@app.route("/download/<filename>")
def findFile(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

