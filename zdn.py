import streamlit as st
import sqlite3
import random
from streamlit_option_menu import option_menu

# Ini sial isasi koneksi ke database Via sqlite
conn = sqlite3.connect('tugas_final.db')
c = conn.cursor()

# Membuat tabel jika belum ada ato sblm di query di buat sesuai diagram jenjang 
c.execute('''CREATE TABLE IF NOT EXISTS stock
             (sku TEXT PRIMARY KEY, name TEXT, price REAL, quantity INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS transactions
             (id INTEGER PRIMARY KEY AUTOINCREMENT, customer_name TEXT, sku TEXT, quantity INTEGER, subtotal REAL)''')
conn.commit()

def membuat_unique_id():
    while True:
        new_id = random.randint(1000, 9999)
        c.execute("SELECT id FROM transactions WHERE id=?", (new_id,))
        if c.fetchone() is None:
            return new_id

def input_stock_data():
    st.subheader("Input Data Stok Barang")
    sku = st.text_input("Masukkan No. SKU (4 digit angka): ")
    if len(sku) == 4 and sku.isdigit():
        c.execute("SELECT * FROM stock WHERE sku=?", (sku,))
        existing_item = c.fetchone()
        if existing_item is None:
            name = st.text_input("Masukkan nama barang: ")
            price = st.number_input("Masukkan harga satuan: ", min_value=0.0, format="%.2f")
            quantity = st.number_input("Masukkan jumlah stok: ", min_value=0, step=1)
            if st.button("Tambah Stok"):
                c.execute("INSERT INTO stock (sku, name, price, quantity) VALUES (?, ?, ?, ?)", (sku, name, price, quantity))
                conn.commit()
                st.success(f"Data stok untuk {name} telah ditambahkan dengan No. SKU {sku}.")
                st.balloons()
        else:
            st.warning(f"No. SKU {sku} sudah tersimpan di dalam data stok.")
    else:
        st.warning("No. SKU harus terdiri dari 4 digit angka.")

def restock_item():
    st.subheader("Restok Barang")
    sku = st.text_input("Masukkan No. SKU barang yang akan direstok: ")
    c.execute("SELECT * FROM stock WHERE sku=?", (sku,))
    item = c.fetchone()
    if item:
        additional_quantity = st.number_input("Masukkan jumlah tambahan stok: ", min_value=0, step=1)
        if st.button("Tambah Stok"):
            new_quantity = item[3] + additional_quantity
            c.execute("UPDATE stock SET quantity=? WHERE sku=?", (new_quantity, sku))
            conn.commit()
            st.success(f"Stok untuk {item[1]} telah ditambahkan sebanyak {additional_quantity}. Total stok sekarang {new_quantity}.")
            st.snow()
    else:
        st.warning(f"Barang dengan No. SKU {sku} tidak ditemukan. Silakan input data stok barang terlebih dahulu.")

def lihat_semua_items():
    st.subheader("Lihat Semua Barang")
    c.execute("SELECT * FROM stock")
    items = c.fetchall()
    if not items:
        st.warning("Belum ada data stok barang.")
    else:
        st.write("===== DATA SEMUA BARANG =====")
        data = [{"SKU": item[0], "Nama": item[1], "Harga": f"{int(item[2]) if item[2].is_integer() else item[2]:,.0f}", "Stok": item[3]} for item in items]
        st.table(data)

def hapus_items():
    st.subheader("Hapus Barang dari Stok")
    c.execute("SELECT * FROM stock")
    items = c.fetchall()
    if not items:
        st.warning("Belum ada data stok barang.")
    else:
        st.write("===== PILIH BARANG YANG AKAN DIHAPUS =====")
        delete_skus = []
        for item in items:
            if st.checkbox(f"SKU: {item[0]}, Nama: {item[1]}, Harga: {item[2]}, Stok: {item[3]}"):
                delete_skus.append(item[0])
        
        if st.button("Hapus Barang"):
            if delete_skus:
                for sku in delete_skus:
                    c.execute("DELETE FROM stock WHERE sku=?", (sku,))
                conn.commit()
                st.success(f"Barang dengan SKU {', '.join(delete_skus)} telah dihapus.")
                st.snow()
            else:
                st.warning("Tidak ada barang yang dipilih untuk dihapus.")

def input_transaksi_baru():
    st.subheader("Input Data Transaksi Baru")
    customer_name = st.text_input("Masukkan nama konsumen: ")

    if 'current_transactions' not in st.session_state:
        st.session_state.current_transactions = []

    sku = st.text_input("Masukkan No. SKU barang yang dibeli: ")
    c.execute("SELECT * FROM stock WHERE sku=?", (sku,))
    item = c.fetchone()

    if item is None:
        st.warning("No. SKU yang diinputkan belum terdaftar.")
    else:
        quantity_bought = st.number_input("Masukkan jumlah barang yang dibeli: ", min_value=1, step=1)

        if item[3] >= quantity_bought:
            subtotal = item[2] * quantity_bought
            if st.button("Tambah ke Transaksi"):
                st.session_state.current_transactions.append({
                    "customer_name": customer_name,
                    "sku": sku,
                    "name": item[1],
                    "price": item[2],
                    "quantity": quantity_bought,
                    "subtotal": subtotal
                })
                st.success(f"{item[1]} ditambahkan ke transaksi.")
        else:
            st.warning("Jumlah Stok No.SKU yang Anda beli tidak mencukupi.")

    if st.session_state.current_transactions:
        st.write("### Daftar Pembelian:")
        total_amount = 0
        for idx, txn in enumerate(st.session_state.current_transactions):
            st.write(f"{idx+1}. {txn['name']} - {txn['quantity']} x {txn['price']} = {txn['subtotal']}")
            total_amount += txn['subtotal']
        
        st.write(f"**Total: {total_amount}**")
        
        if st.button("Selesaikan Transaksi"):
            txn_id = membuat_unique_id()
            for txn in st.session_state.current_transactions:
                c.execute("INSERT INTO transactions (id, customer_name, sku, quantity, subtotal) VALUES (?, ?, ?, ?, ?)",
                          (txn_id, txn["customer_name"], txn["sku"], txn["quantity"], txn["subtotal"]))
                c.execute("UPDATE stock SET quantity = quantity - ? WHERE sku = ?", (txn["quantity"], txn["sku"]))
            conn.commit()
            st.success(f"Transaksi berhasil disimpan dengan ID {txn_id}")
            st.session_state.current_transactions = []  # Clear the current transaction list


def lihat_semua_transaksi():
    st.subheader("Lihat Data Seluruh Transaksi Konsumen")
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    if not transactions:
        st.warning("Belum ada transaksi.")
    else:
        st.write("===== DATA SEMUA TRANSAKSI =====")
        data = [{"ID": txn[0], "Nama Konsumen": txn[1], "SKU": txn[2], "Jumlah": txn[3], "Subtotal": txn[4]} for txn in transactions]
        st.table(data)

def lihat_transaksi_berdasarkan_subtotal():
    st.subheader("Lihat Data Transaksi Berdasarkan Subtotal")
    c.execute("SELECT * FROM transactions ORDER BY subtotal DESC")
    transactions = c.fetchall()
    if not transactions:
        st.warning("Belum ada transaksi.")
    else:
        st.write("===== DATA TRANSAKSI BERDASARKAN SUBTOTAL =====")
        data = [{"ID": txn[0], "Nama Konsumen": txn[1], "SKU": txn[2], "Jumlah": txn[3], "Subtotal": f"{txn[4]:,.0f}"} for txn in transactions]
        st.table(data)

def hapus_transaksi():
    st.subheader("Hapus Data Transaksi Konsumen")
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    if not transactions:
        st.warning("Belum ada transaksi.")
    else:
        st.write("===== PILIH TRANSAKSI YANG AKAN DIHAPUS =====")
        delete_ids = []
        for txn in transactions:
            if st.checkbox(f"ID: {txn[0]}, Nama Konsumen: {txn[1]}, SKU: {txn[2]}, Jumlah: {txn[3]}, Subtotal: {txn[4]}"):
                delete_ids.append(txn[0])
        
        if st.button("Hapus Transaksi"):
            if delete_ids:
                for id in delete_ids:
                    c.execute("DELETE FROM transactions WHERE id=?", (id,))
                conn.commit()
                st.success(f"Data transaksi dengan ID {', '.join(map(str, delete_ids))} telah dihapus.")
            else:
                st.warning("Tidak ada transaksi yang dipilih untuk dihapus.")
                st.snow()

def tentang():
    st.subheader("Tentang Aplikasi")
    
    html_content = """
    <style>
        .frosted-glass {
            background: rgba(255, 255, 255, 0.6); /* White with 60% opacity */
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px); /* Frosted glass effect */
            -webkit-backdrop-filter: blur(10px); /* Safari support */
        }
        .frosted-glass p, .frosted-glass a {
            color: #000; /* Ensure text is readable on the frosted background */
        }
        .marquee {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: blue;
            padding: 10px;
            box-shadow: 0 -4px 8px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px); /* Frosted glass effect */
            -webkit-backdrop-filter: blur(10px); /* Safari support */
            font-size: 20px;
            text-align: center;
            overflow: hidden;
        }
        .marquee-content {
            display: inline-block;
            white-space: nowrap;
            animation: marquee 15s linear infinite;
        }
        @keyframes marquee {
            from { transform: translateX(100%); }
            to { transform: translateX(-100%); }
        }
    </style>
    <div class="frosted-glass">
        <p>Aplikasi sederhana ini dibuat untuk mengelola data stok barang dan transaksi konsumen, dengan Framework berbasis Python <a href="https://streamlit.io" target="_blank">Streamlit.io</a>.</p>
        <p><strong>Pembuat:</strong> Zidan Alfian M_5230411107</p>
        <p><strong>Kunjungi saya di:</strong></p>
        <a href="https://github.com/kangzid/struktur_data_final" style="text-decoration: none;">
            <img src="https://img.shields.io/badge/GitHub-Profile-blue?logo=github" alt="GitHub">
        </a>
        <a href="https://www.instagram.com/kangz.id/" style="text-decoration: none;">
            <img src="https://img.shields.io/badge/Instagram-Profile-red?logo=instagram" alt="Instagram">
        </a>
        <a href="https://www.linkedin.com/in/zalfyan-8263ba281" style="text-decoration: none;">
            <img src="https://img.shields.io/badge/LinkedIn-Profile-blue?logo=linkedin" alt="LinkedIn">
        </a>
    </div>
    <div class="marquee">
        <div class="marquee-content">Universitas Teknologi Yogyakarta | Universitas Teknologi Yogyakarta | Universitas Teknologi Yogyakarta | </div>
    </div>
    """
    
    st.markdown(html_content, unsafe_allow_html=True)
#Fungsi utama untuk merender aplikasi
def main():
    with st.sidebar:
        menu = option_menu("Sistem Kelola", ["Kelola Stok Barang", "Kelola Transaksi Konsumen", "Tentang"],
                           icons=["boxes", "cash-stack", "globe"], menu_icon="cast", default_index=0)
    
    if menu == "Kelola Stok Barang":
        submenu = option_menu("Kelola Stok Barang", ["Input Data Stok Barang", "Restok Barang", "Lihat Semua Barang", "Hapus Barang"],
                              icons=["plus-circle", "arrow-up-circle", "eye", "trash"], menu_icon="cast", default_index=0,
                              orientation="horizontal")
        if submenu == "Input Data Stok Barang":
            input_stock_data()
        elif submenu == "Restok Barang":
            restock_item()
        elif submenu == "Lihat Semua Barang":
            lihat_semua_items()
        elif submenu == "Hapus Barang":
            hapus_items()
    
    elif menu == "Kelola Transaksi Konsumen":
        submenu = option_menu("Kelola Transaksi Konsumen", ["Input Data Transaksi Baru", "Lihat Data Seluruh Transaksi Konsumen", "Lihat Data Transaksi Berdasarkan Subtotal", "Hapus Transaksi Konsumen"],
                              icons=["file-plus", "list", "filter", "trash"], menu_icon="cast", default_index=0,
                              orientation="horizontal")
        if submenu == "Input Data Transaksi Baru":
            input_transaksi_baru()
        elif submenu == "Lihat Data Seluruh Transaksi Konsumen":
            lihat_semua_transaksi()
        elif submenu == "Lihat Data Transaksi Berdasarkan Subtotal":
            lihat_transaksi_berdasarkan_subtotal()
        elif submenu == "Hapus Transaksi Konsumen":
            hapus_transaksi()
    
    elif menu == "Tentang":
        tentang()

if __name__ == "__main__":
    main()