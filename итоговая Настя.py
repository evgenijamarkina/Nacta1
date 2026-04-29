import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
DATA_FILE = "books.json"
class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.root.geometry("700x500")
        self.books = [] 
        self.load_data() 
        self.create_widgets()
        self.update_treeview()
    def create_widgets(self):
               input_frame = ttk.LabelFrame(self.root, text="Добавить новую книгу", padding="10")
        input_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(input_frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(input_frame, textvariable=self.title_var, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(input_frame, text="Автор:").grid(row=1, column=0, sticky="w")
        self.author_var = tk.StringVar()
        self.author_entry = ttk.Entry(input_frame, textvariable=self.author_var, width=30)
        self.author_entry.grid(row=1, column=1, padx=5, pady=2)
        ttk.Label(input_frame, text="Жанр:").grid(row=2, column=0, sticky="w")
        self.genre_var = tk.StringVar()
        self.genre_entry = ttk.Entry(input_frame, textvariable=self.genre_var, width=30)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=2)
        ttk.Label(input_frame, text="Страниц:").grid(row=3, column=0, sticky="w")
        self.pages_var = tk.StringVar()
        self.pages_entry = ttk.Entry(input_frame, textvariable=self.pages_var, width=10)
        self.pages_entry.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        self.add_btn = ttk.Button(input_frame, text="Добавить книгу", command=self.add_book)
        self.add_btn.grid(row=3, column=1, padx=50, pady=2, sticky="e")
        filter_frame = ttk.LabelFrame(self.root, text="Фильтр", padding="10")
        filter_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, sticky="w")
        self.filter_genre_var = tk.StringVar()
        self.filter_genre_entry = ttk.Entry(filter_frame, textvariable=self.filter_genre_var, width=20)
        self.filter_genre_entry.grid(row=0, column=1, padx=5, pady=2)
        ttk.Label(filter_frame, text="Страниц >").grid(row=0, column=2, padx=(20, 0), sticky="e")
        self.filter_pages_var = tk.StringVar()
        self.filter_pages_entry = ttk.Entry(filter_frame, textvariable=self.filter_pages_var, width=8)
        self.filter_pages_entry.grid(row=0, column=3, padx=5, pady=2)
        self.filter_btn = ttk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.grid(row=0, column=4, padx=(10, 0))
     columns = ("#1", "#2", "#3", "#4", "#5")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
                self.tree.heading("#1", text="ID", anchor="w")
        self.tree.heading("#2", text="Название", anchor="w")
        self.tree.heading("#3", text="Автор", anchor="w")
        self.tree.heading("#4", text="Жанр", anchor="w")
         self.tree.heading("#5", text="Страниц", anchor="w")
                 self.tree.column("#1", width=30)
         self.tree.column("#2", width=200)
         self.tree.column("#3", width=150)
         self.tree.column("#4", width=150)
         self.tree.column("#5", width=80)
        
         self.tree.pack(fill="both", expand=True, padx=10, pady=5)
    def add_book(self):
        """Добавляет книгу после проверки ввода."""
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
         genre = self.genre_var.get().strip()
         pages_str = self.pages_var.get().strip()
         if not title or not author or not genre or not pages_str:
             messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
             return
         try:
             pages = int(pages_str)
             if pages <= 0:
                 raise ValueError
         except ValueError:
             messagebox.showerror("Ошибка", "Количество страниц должно быть положительным числом!")
             return
         new_book = {
             "id": len(self.books) + 1,
             "title": title,
             "author": author,
             "genre": genre,
             "pages": pages
         }
         self.books.append(new_book)
         self.save_data()
         self.update_treeview()
            self.clear_entries()
         self.title_entry.focus()

    def clear_entries(self):
         """Очищает поля ввода."""
         self.title_var.set("")
         self.author_var.set("")
          self.genre_var.set("")
          self.pages_var.set("")

    def save_data(self):
          """Сохраняет список книг в JSON-файл."""
          with open(DATA_FILE, 'w', encoding='utf-8') as f:
              json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
          """Загружает данные из JSON-файла при запуске."""
          if os.path.exists(DATA_FILE):
              with open(DATA_FILE, 'r', encoding='utf-8') as f:
                  try:
                      self.books = json.load(f)
                                          for i, book in enumerate(self.books):
                          book["id"] = i + 1
                  except json.JSONDecodeError:
                      self.books = []
          else:
              self.books = []

    def update_treeview(self):
          """Обновляет данные в таблице."""
          for i in self.tree.get_children():
              self.tree.delete(i)
          for book in self.books:
              self.tree.insert("", "end", values=(book["id"], book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
          """Применяет фильтр по жанру и количеству страниц."""
          filter_genre = self.filter_genre_var.get().lower()
          filter_pages_str = self.filter_pages_var.get()
          
          filtered_books = self.books.copy()
                    if filter_genre:
              filtered_books = [b for b in filtered_books if filter_genre in b["genre"].lower()]
                           if filter_pages_str:
              try:
                  filter_pages = int(filter_pages_str)
                  filtered_books = [b for b in filtered_books if b["pages"] > filter_pages]
              except ValueError:
                  messagebox.showerror("Ошибка", "В фильтре страниц введите целое число!")
                  return
          for i in self.tree.get_children():
              self.tree.delete(i)
          for book in filtered_books:
              self.tree.insert("", "end", values=(book["id"], book["title"], book["author"], book["genre"], book["pages"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
