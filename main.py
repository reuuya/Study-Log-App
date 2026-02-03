import datetime
import json
import os

catatan = []
FILE_DATA = "catatan_belajar.json"

def simpan_data():
    """Menyimpan data catatan ke file JSON"""
    try:
        with open(FILE_DATA, "w", encoding="utf-8") as f:
            json.dump(catatan, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ Gagal menyimpan data: {e}")

def muat_data():
    """Memuat data catatan dari file JSON"""
    global catatan
    try:
        if os.path.exists(FILE_DATA):
            with open(FILE_DATA, "r", encoding="utf-8") as f:
                catatan = json.load(f)
        else:
            catatan = []
    except Exception as e:
        print(f"❌ Gagal memuat data: {e}")
        catatan = []

def tambah_catatan():
    print("\n" + "="*40)
    print("      TAMBAH CATATAN BELAJAR")
    print("="*40)
    mapel = input("Mapel: ").strip()
    topik = input("Topik: ").strip()

    while True:
        durasi_input = input("Durasi belajar (menit): ").strip()
        try:
            durasi = int(durasi_input)
            if durasi <= 0:
                print("❌ Masukkan angka durasi lebih dari 0.")
                continue
            break
        except ValueError:
            print("❌ Durasi harus berupa angka (contoh: 30). Coba lagi.")

    catatan_baru = {
        "mapel": mapel,
        "topik": topik,
        "durasi_menit": durasi,
        "tanggal": datetime.date.today().isoformat(),
    }
    catatan.append(catatan_baru)
    simpan_data()
    print("✓ Catatan berhasil disimpan!")
    print("="*40 + "\n")

def ringkasan_mingguan():
    print("\n" + "="*40)
    print("      RINGKASAN MINGGUAN BELAJAR")
    print("="*40)
    if not catatan:
        print("Belum ada catatan belajar.")
        print("="*40)
        input("Tekan Enter untuk lanjut...")
        return

    today = datetime.date.today()
    week_start = today - datetime.timedelta(days=6)

    minggu = []
    for c in catatan:
        t = c.get('tanggal')
        try:
            d = datetime.date.fromisoformat(t) if t else today
        except Exception:
            d = today
        if week_start <= d <= today:
            minggu.append((d, c))

    if not minggu:
        print("Tidak ada catatan dalam 7 hari terakhir.")
        print("="*40)
        input("Tekan Enter untuk lanjut...")
        return

    total_menit = sum(c.get('durasi_menit', 0) for _, c in minggu)
    per_mapel = {}
    for _, c in minggu:
        m = c.get('mapel', '---')
        per_mapel[m] = per_mapel.get(m, 0) + c.get('durasi_menit', 0)

    jam = total_menit // 60
    sisa_menit = total_menit % 60
    print(f"\nTotal (7 hari): {total_menit} menit ({jam} jam {sisa_menit} menit)")
    print("-" * 40)
    print("Waktu per mapel:")
    for m, menit in per_mapel.items():
        j = menit // 60
        mm = menit % 60
        print(f"  • {m}: {menit} menit ({j} jam {mm} menit)")
    print("="*40)
    input("Tekan Enter untuk lanjut...")

def lihat_catatan():
    print("\n" + "="*40)
    print("      DAFTAR CATATAN BELAJAR")
    print("="*40)
    if not catatan:
        print("Belum ada catatan belajar.")
        print("="*40 + "\n")
        return

    for i, c in enumerate(catatan, start=1):
        print(f"{i}. {c['mapel']}")
        print(f"   Topik: {c['topik']}")
        print(f"   Durasi: {c['durasi_menit']} menit")
        print(f"   Tanggal: {c['tanggal']}")
        print("-" * 40)
    
    # Opsi untuk menghapus catatan
    while True:
        pilih = input("Hapus catatan? (y/n): ").strip().lower()
        if pilih == 'y':
            while True:
                try:
                    nomor = int(input("Nomor catatan yang dihapus: "))
                    if 1 <= nomor <= len(catatan):
                        catatan.pop(nomor - 1)
                        simpan_data()
                        print("✓ Catatan berhasil dihapus!\n")
                        break
                    else:
                        print(f"❌ Nomor harus antara 1-{len(catatan)}")
                except ValueError:
                    print("❌ Masukkan nomor yang valid")
        else:
            break
    print()

def total_waktu():
    total = sum(c.get('durasi_menit', 0) for c in catatan)
    jam = total // 60
    sisa_menit = total % 60
    print("\n" + "="*40)
    print(f"Total waktu belajar: {total} menit")
    print(f"({jam} jam {sisa_menit} menit)")
    print("="*40)
    input("Tekan Enter untuk lanjut...")
    print()

def menu():
    print("\n╔════════════════════════════════════════╗")
    print("║      STUDY LOG APP - MENU UTAMA        ║")
    print("╠════════════════════════════════════════╣")
    print("║ 1. Tambah catatan belajar              ║")
    print("║ 2. Lihat catatan belajar               ║")
    print("║ 3. Total waktu belajar                 ║")
    print("║ 4. Ringkasan mingguan                  ║")
    print("║ 5. Keluar                              ║")
    print("╚════════════════════════════════════════╝")

if __name__ == "__main__":
    muat_data()
    
    while True:
        menu()
        pilihan = input("\nPilih menu (1-5): ").strip()

        if pilihan == "1":
            tambah_catatan()
        elif pilihan == "2":
            lihat_catatan()
        elif pilihan == "3":
            total_waktu()
        elif pilihan == "4":
            ringkasan_mingguan()
        elif pilihan == "5":
            simpan_data()
            print("\n✓ Terima kasih telah menggunakan Study Log App. Selamat tinggal!\n")
            break
        else:
            print("❌ Pilihan tidak valid. Silakan masukkan angka 1-5.\n")