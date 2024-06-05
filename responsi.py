from prettytable import PrettyTable

class Node:
    def __init__(self, id, name, age, height, weight):
        self.id = id
        self.name = name
        self.age = age
        self.height = height
        self.weight = weight
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, id, name, age, height, weight):
        new_node = Node(id, name, age, height, weight)
        if self.root is None:
            self.root = new_node
        else:
            self.masukkan_rekursif(self.root, new_node)

    def masukkan_rekursif(self, current_node, new_node):
        if new_node.id < current_node.id:
            if current_node.left is None:
                current_node.left = new_node
            else:
                self.masukkan_rekursif(current_node.left, new_node)
        elif new_node.id > current_node.id:
            if current_node.right is None:
                current_node.right = new_node
            else:
                self.masukkan_rekursif(current_node.right, new_node)

    def in_order_traversal(self):
        result = []
        self.agar_traversal_bersifat_rekursif(self.root, result)
        return result

    def agar_traversal_bersifat_rekursif(self, current_node, result):
        if current_node is not None:
            self.agar_traversal_bersifat_rekursif(current_node.left, result)
            result.append({
                'id': current_node.id,
                'name': current_node.name,
                'age': current_node.age,
                'height': current_node.height,
                'weight': current_node.weight
            })
            self.agar_traversal_bersifat_rekursif(current_node.right, result)

    def urutkan_berdasarkan_usia(self):
        nodes = self.in_order_traversal()
        return sorted(nodes, key=lambda x: x['age'])

    def filter_menurut_tinggi(self, height):
        nodes = self.in_order_traversal()
        return [node for node in nodes if node['height'] == height]

    def filter_menurut_berat(self, weight):
        nodes = self.in_order_traversal()
        return [node for node in nodes if node['weight'] == weight]

# Data berdasarkan tbl di soal responsinyaa
data = [
    (51, "Monsieur", 21, 175, 66),
    (32, "Allan", 25, 188, 74),
    (74, "Oliver", 17, 160, 59),
    (23, "Andre", 19, 173, 69),
    (42, "Cooper", 23, 190, 73),
    (67, "Alex", 20, 157, 57),
    (82, "Leonardo", 24, 162, 56),
    (11, "James", 18, 173, 63),
    (35, "Robert", 22, 185, 72),
    (45, "Evan", 26, 168, 65)
]


bst = BST()


for item in data:
    bst.insert(*item)

def Nampilin_menu():
    table = PrettyTable()
    table.field_names = ["No", "Menu"]
    table.add_row(["1", "Tampilkan seluruh data secara urut berdasarkan usia"])
    table.add_row(["2", "Tampilkan seluruh data dengan tinggi badan tertentu"])
    table.add_row(["3", "Tampilkan seluruh data dengan berat badan tertentu"])
    table.add_row(["0", "Keluar"])

    print(table)

    try:
        choice = int(input("Pilih menu: "))
    except ValueError:
        choice = None
    return choice

def nampilin_data(data):
    if not data:
        print("Maap Tidak ada data yang ditemukan.")
    else:
        table = PrettyTable()
        table.field_names = ["ID", "Nama", "Usia", "Tinggi (cm)", "Berat (kg)"]
        for entry in data:
            table.add_row([entry['id'], entry['name'], entry['age'], entry['height'], entry['weight']])
        print(table)

def main():
    while True:
        choice = Nampilin_menu()
        if choice == 1:
            sorted_data = bst.urutkan_berdasarkan_usia()
            print("Data urut berdasarkan usia:")
            nampilin_data(sorted_data)
        elif choice == 2:
            try:
                height = int(input("Masukkan tinggi badan yang ingin dicari: "))
                filtered_data = bst.filter_menurut_tinggi(height)
                if filtered_data:
                    print(f"Data dengan tinggi badan {height} cm:")
                    nampilin_data(filtered_data)
                else:
                    print(f"Tidak ada data dengan tinggi badan {height} cm.")
            except ValueError:
                print("Input tidak valid. Silakan masukkan angka.")
        elif choice == 3:
            try:
                weight = int(input("Masukkan berat badan yang ingin dicari: "))
                filtered_data = bst.filter_menurut_berat(weight)
                if filtered_data:
                    print(f"Data dengan berat badan {weight} kg:")
                    nampilin_data(filtered_data)
                else:
                    print(f"Tidak ada data dengan berat badan {weight} kg.")
            except ValueError:
                print("Input tidak valid. Silakan masukkan angka.")
        elif choice == 0:
            print("Anda Sudah Keluar dari program.")
            break
        else:
            print("Maaf Pilihan Anda tidak valid,silakan coba lagi.")

if __name__ == "__main__":
    main()
