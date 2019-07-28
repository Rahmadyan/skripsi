from datetime import datetime
import re

def convert(t):
    t = t.lower()
    t = t.rsplit(' ')[0:6]
    t = [re.sub(r"[-()\"#/@;<>{}'`+=~|.!?,]", "", file) for file in t]

    hasil_hari = []
    for i,x in enumerate(t):

        if 'minggu' in x:
            t[i] = x.replace('minggu','sunday')
        elif 'senin' in x:
            t[i] = x.replace('senin','monday')
        elif 'selasa' in x:
            t[i] = x.replace('selasa', 'tuesday')
        elif 'rabu' in x:
            t[i] = x.replace('rabu', 'wednesday')
        elif 'kamis' in x:
            t[i] = x.replace('kamis', 'thursday')
        elif 'jumat' in x:
            t[i] = x.replace('jumat', 'friday')
        elif 'sabtu' in x:
            t[i] = x.replace('sabtu', 'saturday')
        hasil_hari.append(t[i])

    hari_bulan = []
    for a,b in enumerate(hasil_hari):
        if 'januari' in b:
            hasil_hari[a] = b.replace('januari','january')
        elif 'februari' in b:
            hasil_hari[a] = b.replace('februari','february')
        elif 'maret' in b:
            hasil_hari[a] = b.replace('maret','march')
        elif 'april' in b:
            hasil_hari[a] = b.replace('april','april')
        elif 'mei' in b:
            hasil_hari[a] = b.replace('mei','may')
        elif 'juni' in b:
            hasil_hari[a] = b.replace('juni','june')
        elif 'juli' in b:
            hasil_hari[a] = b.replace('juli','july')
        elif 'agustus' in b:
            hasil_hari[a] = b.replace('agustus','august')
        elif 'september' in b:
            hasil_hari[a] = b.replace('september','september')
        elif 'oktober' in b:
            hasil_hari[a] = b.replace('oktober','october')
        elif 'november' in b:
            hasil_hari[a] = b.replace('november','november')
        elif 'desember' in b:
            hasil_hari[a] = b.replace('desember','december')
        hari_bulan.append(hasil_hari[a])

    hari_bulan = ' '.join(hari_bulan)
    time = datetime.strptime(hari_bulan, "%A %d %B %Y %H:%M")
    return time
# a = "rabu, 22 desember 2019 - 15:04 WIB"
# print(convert(a))
