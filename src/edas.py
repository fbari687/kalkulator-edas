def hitung_rata_rata(data):
    jumlah_alternatif = len(data)
    jumlah_kriteria = len(data[0])

    avg = []
    for j in range(jumlah_kriteria):
        total = 0
        for i in range(jumlah_alternatif):
            total += data[i][j]
        avg.append(total / jumlah_alternatif)

    return avg


def hitung_pda_nda(data, avg, tipe):
    jumlah_alternatif = len(data)
    jumlah_kriteria = len(data[0])

    pda = []
    nda = []

    for i in range(jumlah_alternatif):
        pda_row = []
        nda_row = []

        for j in range(jumlah_kriteria):
            nilai = data[i][j]

            if avg[j] == 0:
                pda_val = 0
                nda_val = 0

            elif tipe[j] == "benefit":
                if nilai > avg[j]:
                    pda_val = (nilai - avg[j]) / avg[j]
                    nda_val = 0
                else:
                    pda_val = 0
                    nda_val = (avg[j] - nilai) / avg[j]

            elif tipe[j] == "cost":
                if nilai < avg[j]:
                    pda_val = (avg[j] - nilai) / avg[j]
                    nda_val = 0
                else:
                    pda_val = 0
                    nda_val = (nilai - avg[j]) / avg[j]

            else:
                raise ValueError(f"Tipe kriteria tidak valid: {tipe[j]}")

            pda_row.append(pda_val)
            nda_row.append(nda_val)

        pda.append(pda_row)
        nda.append(nda_row)

    return pda, nda


def hitung_sp_sn(pda, nda, bobot):
    sp = []
    sn = []

    for i in range(len(pda)):
        total_sp = 0
        total_sn = 0

        for j in range(len(pda[0])):
            total_sp += bobot[j] * pda[i][j]
            total_sn += bobot[j] * nda[i][j]

        sp.append(total_sp)
        sn.append(total_sn)

    return sp, sn


def hitung_normalisasi(sp, sn):
    max_sp = max(sp) if max(sp) != 0 else 1
    max_sn = max(sn) if max(sn) != 0 else 1

    nsp = []
    nsn = []

    for i in range(len(sp)):
        nsp.append(sp[i] / max_sp)
        nsn.append(1 - (sn[i] / max_sn))

    return nsp, nsn


def hitung_as(nsp, nsn):
    as_score = []

    for i in range(len(nsp)):
        score = (nsp[i] + nsn[i]) / 2
        as_score.append(score)

    return as_score


def hitung_ranking(as_score):
    ranking = sorted(
        [(i, as_score[i]) for i in range(len(as_score))],
        key=lambda x: x[1],
        reverse=True
    )
    return ranking

def validasi_input(data, bobot, tipe):
    # Validasi data kosong
    if not data or not data[0]:
        raise ValueError("Data tidak boleh kosong")

    jumlah_kriteria = len(data[0])

    # Validasi jumlah kolom konsisten
    for i, row in enumerate(data):
        if len(row) != jumlah_kriteria:
            raise ValueError(f"Jumlah kriteria tidak konsisten di baris {i}")

    # Validasi bobot
    if len(bobot) != jumlah_kriteria:
        raise ValueError("Jumlah bobot harus sama dengan jumlah kriteria")

    total_bobot = sum(bobot)
    if abs(total_bobot - 1) > 0.0001:
        raise ValueError(f"Total bobot harus = 1 (sekarang {total_bobot})")

    # Validasi tipe
    if len(tipe) != jumlah_kriteria:
        raise ValueError("Jumlah tipe harus sama dengan jumlah kriteria")

    for i, t in enumerate(tipe):
        if t not in ["benefit", "cost"]:
            raise ValueError(f"Tipe tidak valid di index {i}: {t}")

def hitung_edas(data, bobot, tipe):
	validasi_input(data, bobot, tipe)
	avg = hitung_rata_rata(data)
	pda, nda = hitung_pda_nda(data, avg, tipe)
	sp, sn = hitung_sp_sn(pda, nda, bobot)
	nsp, nsn = hitung_normalisasi(sp, sn)
	as_score = hitung_as(nsp, nsn)
	ranking = hitung_ranking(as_score)

	return {
		"average": avg,
		"pda": pda,
		"nda": nda,
		"sp": sp,
		"sn": sn,
		"nsp": nsp,
		"nsn": nsn,
		"as": as_score,
		"ranking": ranking
	}