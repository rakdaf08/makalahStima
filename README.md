# Basketball A\* Pathfinding Simulation

Simulasi permainan basket yang menggunakan algoritma A\* untuk menentukan jalur optimal pemain menuju ring basket.

## Deskripsi Program

Program ini mensimulasikan permainan basket sederhana dengan:

- **Pemain Penyerang (A)**: Pemain yang berusaha mencapai ring
- **Pemain dengan Bola (B)**: Pemain yang membawa bola
- **Pemain Bertahan (D)**: Pemain yang menghalangi jalur
- **Ring Basket (R)**: Target yang harus dicapai

Program menggunakan algoritma A\* untuk menghitung cost optimal setiap pemain menuju ring dan menentukan strategi passing terbaik.

## Struktur File

```
src/
├── main.py          # File utama untuk menjalankan program
├── simulation.py    # Logic simulasi dan tampilan
├── logic.py         # Game logic dan pergerakan pemain
├── astar.py         # Implementasi algoritma A*
├── utils.py         # Utility functions
└── config.py        # Konfigurasi game (grid awal, simbol, dll)
```

## Cara Menjalankan

1. **Pastikan Python terinstall** (Python 3.7+)

2. **Navigasi ke folder src**:

   ```bash
   cd src
   ```

3. **Jalankan program**:

   ```bash
   python main.py
   ```

4. **Ikuti instruksi di layar**:
   - Program akan menampilkan legenda simbol
   - Tekan Enter untuk memulai simulasi
   - Simulasi akan berjalan otomatis dengan delay 2 detik per tick

## Fitur Program

### Analisis A\* Cost

- Menampilkan cost setiap pemain menuju ring target
- Cost dihitung menggunakan algoritma A\* dengan heuristik Manhattan distance
- Cost final = cost A\* + current tick

### Strategi Passing

- Program menentukan apakah pemain harus mempertahankan bola atau passing
- Keputusan berdasarkan pemain dengan cost terendah
- Menampilkan semua opsi passing dengan cost masing-masing

### Pergerakan Otomatis

- Pemain penyerang bergerak 2 langkah per tick menuju ring
- Pemain bertahan bergerak ke kanan (simulasi defensive strategy)
- Game berakhir ketika pemain dengan bola mencapai ring (cost ≤ 1)

## Simbol Game

| Simbol | Deskripsi            |
| ------ | -------------------- |
| 🏀 B   | Pemain dengan bola   |
| 🔵 A   | Pemain penyerang     |
| 🔴 D   | Pemain bertahan      |
| 🎯 R   | Ring basket (target) |
| . .    | Area kosong          |

## Output Program

Program menampilkan:

1. **Grid permainan** dengan posisi semua pemain
2. **Analisis A\* Cost** untuk setiap pemain
3. **Status game** (goal scored atau time limit)

## Contoh Output

```
📊 ANALISIS A* COST:

💰 Cost tiap pemain penyerang ke target ring - State 1:
   🔵 Baris 1, Kolom 2: cost 8
   🏀 Baris 2, Kolom 2: cost 9
   🔵 Baris 3, Kolom 3: cost 8

```

## Requirements

- Python 3.7+
- Modul bawaan Python (typing, heapq, time)

Tidak ada dependencies eksternal yang
