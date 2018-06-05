from flask import Flask, render_template, request
import os

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/explore', methods=['POST'])
def explore():
    #if request.method == 'POST':
     #   f = request.files['file']
      #  #f.save(se cure_filename(f.filename))
       # return 'file uploaded successfully'
    #return "error"
    target = os.path.join(APP_ROOT,"files/")
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        if(filename.lower().endswith(('xlsx'))) :
            destination = "/".join([target, filename])
            print(destination)
            file.save(destination)
        elif ((filename.lower().endswith(('xlsx')))==False):
            return render_template('index.html',echec="Error",msg="the file extension is not valid, chose a xlsx data file.")

        else:
            return render_template('index.html',echec="Error",msg="please, you should upload a file")



    return render_template('explore.html',filename=filename)


@app.route('/user')
def user():

    return render_template('user.html')


if __name__ == '__main__':
    app.run(debug=True)