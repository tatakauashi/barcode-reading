from google.cloud import vision
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/read-barcode', methods=['POST'])
def read_barcode():
  # 画像データを受け取る
  image_data = request.files['image']

  # Vision API クライアントを作成
  client = vision.ImageAnnotatorClient()

  # 画像を Vision API に送信
  image = vision.Image(content=image_data.read())
  response = client.text_detection(image=image)

  # バーコード情報リスト
  barcodes = []

  # 認識されたテキストを取得
  for text_annotation in response.text_annotations:
    # バーコードかどうか確認
    if text_annotation.description.startswith('Barcode:'):
      # バーコード内容を取得
      barcode_value = text_annotation.description[8:]
      # バーコード情報に追加
      barcodes.append(barcode_value)

  # 結果をJSON形式で返す
  return jsonify({'barcodes': barcodes})

# if __name__ == '__main__':
#   app.run(debug=True)
