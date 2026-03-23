from flask import Flask, request, jsonify, send_from_directory
from edas import hitung_edas

app = Flask(__name__, static_folder="dist", static_url_path="")

@app.route("/")
def serve():
	return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
	return send_from_directory(app.static_folder, path)

@app.route("/api/edas", methods=["POST"])
def edas_api():
	try:
		data = request.get_json()

		matrix = data.get("data")
		bobot = data.get("bobot")
		tipe = data.get("tipe")

		if matrix is None or bobot is None or tipe is None:
			return jsonify({
				"error": "data, bobot, dan tipe wajib diisi"
			}), 400
		
		hasil = hitung_edas(matrix, bobot, tipe)

		return jsonify({
			"status": "success",
			"result": hasil
		})
	
	except Exception as e:
		return jsonify({
			"status": "error",
			"message": str(e)
		}), 500
	
if __name__ == "__main__":
	app.run(debug=True)