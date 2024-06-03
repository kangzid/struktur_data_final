class TreeNode:
    def __init__(self, sku, name, price, quantity):
        self.sku = sku
        self.name = name
        self.price = price
        self.quantity = quantity
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, sku, name, price, quantity):
        if self.root is None:
            self.root = TreeNode(sku, name, price, quantity)
        else:
            self._insert(self.root, sku, name, price, quantity)

    def _insert(self, node, sku, name, price, quantity):
        if sku < node.sku:
            if node.left is None:
                node.left = TreeNode(sku, name, price, quantity)
            else:
                self._insert(node.left, sku, name, price, quantity)
        elif sku > node.sku:
            if node.right is None:
                node.right = TreeNode(sku, name, price, quantity)
            else:
                self._insert(node.right, sku, name, price, quantity)
        else:
            print(f"No. SKU {sku} sudah tersimpan di dalam BST.")

    def find(self, sku):
        return self._find(self.root, sku)

    def _find(self, node, sku):
        if node is None:
            return None
        if sku < node.sku:
            return self._find(node.left, sku)
        elif sku > node.sku:
            return self._find(node.right, sku)
        else:
            return node

    def inorder(self):
        elements = []
        self._inorder(self.root, elements)
        return elements

    def _inorder(self, node, elements):
        if node:
            self._inorder(node.left, elements)
            elements.append(node)
            self._inorder(node.right, elements)

# Inisialisasi BST untuk menyimpan data stok barang
stock_bst = BST()
transactions = []

def main_menu():
    while True:
        print("===== MENU UTAMA =====")
        print("1) Kelola Stok Barang")
        print("2) Kelola Transaksi Konsumen")
        print("0) Exit Program")
        choice = input("Pilih menu: ")

        if choice == '1':
            manage_stock_menu()
        elif choice == '2':
            manage_transactions_menu()
        elif choice == '0':
            print("Terima kasih! Program berhenti.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

def manage_stock_menu():
    while True:
        print("===== KELOLA STOK BARANG =====")
        print("1.1) Input Data Stok Barang")
        print("1.2) Restok Barang")
        print("1.3) Lihat Semua Barang")
        print("9) Kembali ke MENU UTAMA")
        choice = input("Pilih sub menu: ")

        if choice == '1.1':
            input_stock_data()
        elif choice == '1.2':
            restock_item()
        elif choice == '1.3':
            view_all_items()
        elif choice == '9':
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

def input_stock_data():
    sku = input("Masukkan No. SKU (4 digit angka): ")
    if len(sku) != 4 or not sku.isdigit():
        print("No. SKU harus terdiri dari 4 digit angka.")
        return

    if stock_bst.find(sku) is not None:
        print(f"No. SKU {sku} sudah tersimpan di dalam BST.")
        return

    name = input("Masukkan nama barang: ")
    price = float(input("Masukkan harga satuan: "))
    quantity = int(input("Masukkan jumlah stok: "))
    stock_bst.insert(sku, name, price, quantity)
    print(f"Data stok untuk {name} telah ditambahkan dengan No. SKU {sku}.")

def restock_item():
    sku = input("Masukkan No. SKU barang yang akan direstok: ")
    item = stock_bst.find(sku)
    if item:
        additional_quantity = int(input("Masukkan jumlah tambahan stok: "))
        item.quantity += additional_quantity
        print(f"Stok untuk {item.name} telah ditambahkan sebanyak {additional_quantity}. Total stok sekarang {item.quantity}.")
    else:
        print(f"Barang dengan No. SKU {sku} tidak ditemukan. Silakan input data stok barang terlebih dahulu.")

def view_all_items():
    items = stock_bst.inorder()
    if not items:
        print("Belum ada data stok barang.")
    else:
        print("===== DATA SEMUA BARANG =====")
        print("{:<10} {:<20} {:<10} {:<10}".format("SKU", "Nama", "Harga", "Stok"))
        print("-" * 50)
        for item in items:
            print("{:<10} {:<20} {:<10} {:<10}".format(item.sku, item.name, item.price, item.quantity))
    input("Tekan Enter untuk kembali ke Sub Menu Kelola Stok Barang...")

def manage_transactions_menu():
    while True:
        print("===== KELOLA TRANSAKSI KONSUMEN =====")
        print("2.1) Input Data Transaksi Baru")
        print("2.2) Lihat Data Seluruh Transaksi Konsumen")
        print("2.3) Lihat Data Transaksi Berdasarkan Subtotal")
        print("9) Kembali ke MENU UTAMA")
        choice = input("Pilih sub menu: ")

        if choice == '2.1':
            input_new_transaction()
        elif choice == '2.2':
            view_all_transactions()
        elif choice == '2.3':
            view_transactions_by_subtotal()
        elif choice == '9':
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

def input_new_transaction():
    customer_name = input("Masukkan nama konsumen: ")
    
    while True:
        sku = input("Masukkan No. SKU barang yang dibeli: ")
        item = stock_bst.find(sku)
        
        if item is None:
            print("No. SKU yang diinputkan belum terdaftar.")
            continue_transaction = input("Apakah ingin melanjutkan transaksi (Y/N)? ").upper()
            if continue_transaction == 'N':
                return
        else:
            break
    
    while True:
        quantity_bought = int(input("Masukkan jumlah barang yang dibeli: "))
        
        if item.quantity >= quantity_bought:
            item.quantity -= quantity_bought
            subtotal = item.price * quantity_bought
            transaction = {
                'customer_name': customer_name,
                'sku': sku,
                'quantity': quantity_bought,
                'subtotal': subtotal
            }
            transactions.append(transaction)
            print("Data Transaksi Konsumen Berhasil Diinputkan")
            
            add_more = input("Apakah ingin menambahkan data pembelian untuk konsumen ini (Y/N)? ").upper()
            if add_more == 'N':
                return
        else:
            print("Jumlah Stok No.SKU yang Anda beli tidak mencukupi.")
            continue_transaction = input("Apakah ingin melanjutkan transaksi (Y/N)? ").upper()
            if continue_transaction == 'N':
                return

def view_all_transactions():
    if not transactions:
        print("Belum ada transaksi.")
    else:
        for idx, transaction in enumerate(transactions):
            print(f"Transaksi {idx+1}: {transaction['customer_name']}, SKU: {transaction['sku']}, Jumlah Beli: {transaction['quantity']}, Subtotal: {transaction['subtotal']}")
    
    input("Tekan Enter untuk kembali ke Sub Menu Kelola Transaksi Konsumen...")

def view_transactions_by_subtotal():
    if not transactions:
        print("Belum ada transaksi.")
    else:
        sorted_transactions = quicksort(transactions)
        for idx, transaction in enumerate(sorted_transactions):
            print(f"Transaksi {idx+1}: {transaction['customer_name']}, SKU: {transaction['sku']}, Jumlah Beli: {transaction['quantity']}, Subtotal: {transaction['subtotal']}")
    
    input("Tekan Enter untuk kembali ke Sub Menu Kelola Transaksi Konsumen...")

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]['subtotal']
    left = [x for x in arr if x['subtotal'] > pivot]
    middle = [x for x in arr if x['subtotal'] == pivot]
    right = [x for x in arr if x['subtotal'] < pivot]
    return quicksort(left) + middle + quicksort(right)

if __name__ == "__main__":
    main_menu()
