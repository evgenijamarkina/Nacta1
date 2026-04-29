python
Копировать
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 Book Tracker")
        self.books = []
        self.filename = "books.json"

        # --- Создание виджетов ---
        # Заголовки полей
        tk.Label(root, text="Название книги:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        tk.Label(root, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        tk.Label(root, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        tk.Label(root, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Поля ввода
        self.title_entry = tk.Entry(root)
        self.author_entry = tk.Entry(root)
        self.genre_entry = tk.Entry(root)
        self.pages_entry = tk.Entry(root)

        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.author_entry.grid(row=1, column=1, padx=5, pady=5)
        self.genre_entry.grid(row=2, column=1, padx=5, pady=5)
        self.pages_entry.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.add_button = tk.Button(root, text="➕ Добавить книгу", command=self.add_book)
        self.add_button.grid(row=4, columnspan=2, pady=10)

        # Таблица для вывода данных
        self.columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")
        
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
        
        self.tree.grid(row=5, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, sticky="e")
        tk.Label(root, text="Фильтр по страницам (больше):").grid(row=7, column=0, sticky="e")

        self.filter_genre_entry = tk.Entry(root)
        self.filter_pages_entry = tk.Entry(root)

        self.filter_genre_entry.grid(row=6, column=1)
        self.filter_pages_entry.grid(row=7, column=1)

        # Кнопка фильтрации
        tk.Button(root, text="🔎 Фильтровать", command=self.apply_filter).grid(row=8, columnspan=2)

        # Кнопки для JSON
        tk.Button(root, text="💾 Сохранить в JSON", command=self.save_to_json).grid(row=9, columnspan=2)
        
         # Загрузка данных при запуске (без кнопки)
self.load_from_json()

def add_book(self):
         title = self.title_entry.get().strip()
         author = self.author_entry.get().strip()
         genre = self.genre_entry.get().strip()
         pages = self.pages_entry.get().strip()

         # Проверка на пустые поля
         if not title or not author or not genre or not pages:
             messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
             return

         # Валидация количества страниц (должно быть целым числом > 0)
         if not pages.isdigit() or int(pages) <= 0:
             messagebox.showerror("Ошибка", "Количество страниц должно быть положительным целым числом!")
             return

         # Добавление книги в список и таблицу
         book_data = {
             "title": title,
             "author": author,
             "genre": genre,
             "pages": int(pages)
         }
         
         self.books.append(book_data)
         
         # Очистка полей ввода и обновление таблицы
         self.clear_entries()
         self.update_table()


    def clear_entries(self):
        

for entry in [self.title_entry, self.author_entry,
                      self.genre_entry, self.pages_entry]:
             entry.delete(0, tk.END)

    def update_table(self):
         # Очистка текущей таблицы и заполнение её данными из списка self.books
         for i in self.tree.get_children():
             self.tree.delete(i)
         for book in self.books:
             self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def apply_filter(self):
         genre_filter = self.filter_genre_entry.get().lower()
         pages_filter = self.filter_pages_entry.get()
         
         filtered_books = self.books.copy()
         
         if genre_filter:
             filtered_books = [b for b in filtered_books if genre_filter in b["genre"].lower()]
             
         if pages_filter.isdigit():
             filtered_books = [b for b in filtered_books if b["pages"] > int(pages_filter)]
             
         # Обновление таблицы с отфильтрованными данными
         for i in self.tree.get_children():
             self.tree.delete(i)
         for book in filtered_books:
             self.tree.insert("", "end", values=(book["title"], book["author"], book["genre"], book["pages"]))

    def save_to_json(self):
         try:
             with open(self.filename, 'w', encoding='utf-8') as f:
                 json.dump(self.books, f, ensure_ascii=False, indent=4)
             messagebox.showinfo("Успех", f"Данные сохранены в {self.filename}")
         except Exception as e:
             messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")

    def load_from_json(self):
         try:
             if os.path.exists(self.filename):
                 with open(self.filename, 'r', encoding='utf-8') as f:
                     data = json.load(f)
                     if isinstance(data, list):
                         self.books = data
                         self.update_table()
                     else:
                         messagebox.showwarning("Формат", "Файл JSON имеет неверный формат.")
             else:
                 pass # Файл будет создан при первом сохранении.
         except Exception as e:
             messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()
