from . import app
from google.cloud import vision
from flask import Flask, request, jsonify, render_template
import logging, os, json

@app.route('/', methods=['GET'])
def index():
    return render_template(
        'barcodetest_gv.html'
    )

@app.route('/read-barcode', methods=['POST'])
def read_barcode():
    app_logger = logging.getLogger('app_logger')

    # 画像データを受け取る
    image_data = request.files['image-file']

    # Vision API クライアントを作成
    client = vision.ImageAnnotatorClient()

    # 画像を Vision API に送信
    image = vision.Image(content=image_data.read())
    response = client.text_detection(image=image)
    # response = client.document_text_detection(image=image)
    app_logger.info(f'response=[{response}]')

    # バーコード情報リスト
    barcodes = []

    # 認識されたテキストを取得
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # バーコードかどうか確認
            if block.block_type == 'BARCODE':
                # data = {}
                # data['format'] = barcode.format
                # data['raw_value'] = barcode.raw_value
                barcodes.append(block)

    # 結果をJSON形式で返す
    if len(barcodes) > 0:
        return jsonify({'barcodes': barcodes}), 200
    else:
        return jsonify({'message': 'No barcodes found'}), 404
