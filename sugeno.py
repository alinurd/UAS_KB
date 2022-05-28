#Nama   : Ali Nurdin
#NIM    : 191011401314
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : permintaan gaji 



def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class pengajuan():
    minimum = 2100
    maximum = 3500

    def turun(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def naik(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)

class uangperusaahaan():
    minimum = 100
    medium = 300
    maximum = 500

    def sedikit(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def cukup(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def banyak(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.medium:
            return 0
        else:
            return up(x, self.medium, self.maximum)

class permintaan():
    minimum = 3000000
    maximum = 8000000
    
    def kurang(self, α):
        return self.maximum - α * (self.maximum-self.minimum)

    def tambah(self, α):
        return α *(self.maximum - self.minimum) + self.minimum

    # 2 pengajuan 3 uangperusaahaan
    def inferensi(self, jumlah_pengajuan, jumlah_uangperusaahaan):
        pmt = pengajuan()
        psd = uangperusaahaan()
        result = []
        # [R1] JIKA pengajuan TURUN, dan uangperusaahaan BANYAK, 
        #     MAKA Produksi Barang BERKURANG.
        α1 = min(pmt.turun(jumlah_pengajuan), psd.banyak(jumlah_uangperusaahaan))
        z1 = self.kurang(α1)
        result.append((α1, z1))
        # [R2] JIKA pengajuan TURUN, dan uangperusaahaan SEDIKIT, 
        #     MAKA Produksi Barang BERKURANG.
        α2 = min(pmt.turun(jumlah_pengajuan), psd.sedikit(jumlah_uangperusaahaan))
        z2 = self.kurang(α2)
        result.append((α2, z2))
        # [R3] JIKA pengajuan NAIK, dan uangperusaahaan BANYAK, 
        #     MAKA Produksi Barang BERTAMBAH.
        α3 = min(pmt.naik(jumlah_pengajuan), psd.banyak(jumlah_uangperusaahaan))
        z3 = self.tambah(α3)
        result.append((α3, z3))
        # [R4] JIKA pengajuan NAIK, dan uangperusaahaan SEDIKIT,
        #     MAKA Produksi Barang BERTAMBAH.
        α4 = min(pmt.naik(jumlah_pengajuan), psd.sedikit(jumlah_uangperusaahaan))
        z4 = self.tambah(α4)
        result.append((α4, z4))

        # [R5] JIKA pengajuan NAIK, dan uangperusaahaan CUKUP,
        #     MAKA Produksi Barang BERKURANG.
        α5 = min(pmt.naik(jumlah_pengajuan), psd.cukup(jumlah_uangperusaahaan))
        z5 = self.kurang(α5)
        result.append((α5, z5))

        # [R6] JIKA pengajuan NAIK, dan uangperusaahaan CUKUP,
        #     MAKA Produksi Barang BERKURANG.
        α6 = min(pmt.turun(jumlah_pengajuan), psd.cukup(jumlah_uangperusaahaan))
        z6 = self.tambah(α6)
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_permintaan, jumlah_uangperusaahaan):
        inferensi_values = self.inferensi(jumlah_permintaan, jumlah_uangperusaahaan)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])