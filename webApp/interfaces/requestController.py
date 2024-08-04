from flask import jsonify, request, json, Response
from webApp import app, vision
from config import config
import os


def acceptImage(file, type_img):
    orig_filename = file.filename
    hash_name = f'temp.png'
    os.makedirs(config['WEB_APP']['data_path'], exist_ok=True)
    filename = os.path.join(config['WEB_APP']['data_path'], hash_name)
    file.save(filename)



    

@app.route("/upload_image", methods=['POST'])
def upload_image():
    try:
        type_img = request.args.get("type")
        for file in request.files.getlist("files"):
            acceptImage(file, type_img=type_img)
            vision.read_images(type=type_img)
        return jsonify({'Loaded': True})
    except:
        return jsonify({'Loaded': False})


@app.route("/list_image_type", methods=['GET'])
def list_image_type():
    return jsonify({
        "src": list(vision.src.keys()),
        "edited": list(vision.edited.keys())
    })

@app.route('/proccess_pic')
def proc_pic():
    type_img = request.args.get('type')
    part = request.args.get("part")
    return Response(vision.preview(type_img, part), mimetype='image/jpeg')

@app.route("/crop_img", methods=['POST'])
def crop_img():
    data = json.loads(request.data)
    type_img = data['type']
    del data['type']
    vision.crop(type_img, data)
    return {}

@app.route("/eval", methods=['POST'])
def evaluate():
    data = json.loads(request.data)
    vision.generate_mask(data)
    vision.find_conts(data)
    vision.calc_area(data)

    res = {
        "type": data['type'],
        "result": vision.result
    }
    return jsonify(res)
