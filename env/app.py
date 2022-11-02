from flask import Flask, json, request, jsonify
import os
from werkzeug.utils import secure_filename
import easyocr
import numpy as np
import re,os

app = Flask(__name__)
 
app.secret_key = "caircocoders-ednalan"
 
UPLOAD_FOLDER = r'env\static\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    else:
        print("The file does not exist") 
        return False


reg = ["^[Tt][Oo][Tt][Aa][Ll]$",
               "^[Gg][Rr][Aa][Nn][Dd]\s*[Tt][Oo][Tt][Aa][Ll]$",
              "[Ss][Uu][Bb]\s*[Tt][Oo][Tt][Aa][Ll]$",
              "[Tt][Oo][Tt][Aa][Ll]\s*[Vv][Aa][Ll][Uu][Ee]$"]
    

def find_value(pos,cords):
    total_y0 = cords[pos][0]
    total_y1 = cords[pos][1]
    k = 10
    
    flag = False
    for i in cords:
        if((i != pos) and (total_y0-k <= cords[i][0] and cords[i][0] <= total_y0+k) and (total_y1-k <= cords[i][1] and cords[i][1] <= total_y1+k)):
            val_pos = i
            flag = True
            return val_pos
        
    if(flag == False):
        return None
        
    
        
def find_pos_total(text):
    pos = 0
    flag = False
    
    for i in text:
        if(re.search(reg[0],text[i]) != None):
            pos = i
            flag = True
            return pos
            
    if(flag == False):
        for i in text:
            if(re.search(reg[1],text[i]) != None):
                pos = i
                flag = True
                return pos
            
            elif(re.search(reg[2],text[i]) != None):
                pos = i
                flag = True
                return pos
            
            elif(re.search(reg[3],text[i]) != None):
                pos = i
                flag = True
                return pos
                
    if(flag == False):
        return None


def start(file_path):
    reader = easyocr.Reader(["en"],gpu=False)
    result = reader.readtext(file_path)
    print(result)
    text = {}
    cords = {}
    x = 0
    for i in result:
        text[x] = i[1]
        cords[x] = [i[0][0][1],i[0][2][1]]
        x += 1
    index = find_pos_total(text)
    val_index = find_value(index,cords)
    if(val_index == None):
        return "Error"
    print(val_index)
    print(val_index,text[val_index])
    value = text[val_index]
    if(re.search("^\d",value) == None):
        return "Error"
    else:
        new_value = ""
        for i in range(len(value)):
            if(value[i] == "," and i == len(value)-3):
                new_value += "."
            else:
                new_value += value[i]
        print(new_value)
        return new_value



 
@app.route('/')
def main():
    return 'Homepage'

# @app.route('/')

@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
 
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False
    all_values= []
    for file in files:      
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            success = True

            total_amt = start(file_path)
            all_values.append(total_amt)
            delete_file(file_path)
            
        else:
            errors[file.filename] = 'File type is not allowed'

    if success:
        
        return json.dumps(all_values)

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return json.dumps(all_values)
    
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

    
 
if __name__ == '__main__':
    app.run(debug=True)

