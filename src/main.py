from edas import hitung_edas

data = [
    [80, 70, 90],
    [60, 85, 75],
    [75, 80, 85]
]

bobot = [0.4, 0.3, 0.3]
tipe = ["benefit", "cost", "benefit"]

hasil = hitung_edas(data, bobot, tipe)

for key, value in hasil.items():
    print(f"{key.upper()}: {value}")